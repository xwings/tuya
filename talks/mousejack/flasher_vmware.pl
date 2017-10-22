#!/usr/bin/perl -w

# Simple perl script to drive the Bus Pirate and unbrick your CrazyRadio dongle.
# Adapted (sorta) from the Bus Pirate example script and mbed NRF24LU1+ flasher projects:
#  http://code.google.com/p/the-bus-pirate/source/browse/trunk/scripts/SPIeeprom.pl
#  http://mbed.org/users/mux/code/nrflash
#
# This script uses the aux output on the Bus Pirate as the PROG pin on the CrazyRadio's NRF24LU1+ chip.
#
# Electrical connections are as follows:
#
#  Bus Pirate       CrazyRadio
#  ===========================
#  MOSI ()      ->  MOSI  (6)
#  MISO ()      ->  MISO  (8)
#  SCK  ()      ->  SCK   (4)
#  CS   ()      ->  CS    (10)
#  AUX  ()      ->  PROG  (2)
#  3V3  ()      ->  3V3   (5)
#  GND  ()      ->  GND   (9)

use strict;
use feature 'say';
use Getopt::Long;
use Device::SerialPort;
use Time::HiRes qw/usleep/;

use constant {
    WREN        => "\x06",
    WRDIS       => "\x04",
    RDSR        => "\x05",
    WRSR        => "\x01",
    READ        => "\x03",
    PROGRAM     => "\x02",
    ERASE_PAGE  => "\x52",
    ERASE_ALL   => "\x62",
    RDFPCR      => "\x89",
    RDISMB      => "\x85",
    ENDEBUG     => "\x86",
    RDYN        => "\x10",
    FLASH_LEN   => 32768,

    BP_CS       => "\x01",
    BP_AUX      => "\x02",
    BP_PULLUP   => "\x04",
    BP_POWER    => "\x08",
};

my %opts;
my $port;
my $time = 500;
my $status_byte;
my $return;

if (!&GetOptions(\%opts,
    'input=s',
    'device=s',
) || ( !$opts{input} && !$opts{device} ) ) {
    die "Please specify both -input <input_file.bin> and -device <Bus Pirate devnode>";
}

$port = new Device::SerialPort( $opts{device} );

# Setup serial

$port->baudrate(115200);
$port->parity("none");
$port->databits(8);
$port->stopbits(1);
$port->buffers(1,1);
$port->write_settings || undef $port;

die "Unable to write settings to serial port." unless $port;

# Setup BP
say "Entering raw bitbang mode...";
    while ( ( $port->read( 5 ) ne "BBIO1" ) && --$time ) {
    $port->write( "\x00" );
    usleep( 40000 );
}
die "Unable to enter raw bitbang mode!" unless $time;

say "Entering binary SPI mode...";
$port->write( "\x01" );
usleep( 40000 );
$return = $port->read(4);
die "Unable to enter binary SPI mode: $return" unless ( $return eq "SPI1" );

$status_byte = "\x49";                      # Write a known status: PWR, /PULLUP, /AUX, CS
                                            # ...no Bus Pirate command lets us read this register, we have to keep state ourselves
say "Configuring peripherals...";
$port->write( $status_byte );
usleep( 40000 );
$return = $port->read(1);
die "Unable to configure peripherals: $return" unless ( $return eq "\x01" );

say "Configuring SPI...";
$port->write( "\x65" );                     # Configure BP SPI speed
usleep( 40000 );
$return = $port->read(1);
die "Unable to configure SPI: $return" unless ( $return eq "\x01" );

$port->write( "\x8A" );                     # Configure BP SPI options (CPOL=0, CPHA=0)
usleep( 40000 );
$return = $port->read(1);
die "Unable to configure SPI: $return" unless ( $return eq "\x01" );
usleep( 40000 );


# Set up device SPI
$status_byte |=  BP_AUX;                    # PROG high

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );


# === Enable writing ===
say "Enabling programming...";

$status_byte &= ~BP_CS;                     # CS low

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

$port->write( "\x10" );                     # Bulk SPI transfer: 1 byte
usleep ( 20000 );
die "Failed bulk read/write." if ( $port->read( 1 ) ne "\x01" );

$port->write( WREN );                       # Bulk 0: command
usleep( 40000 );

$port->read( 1 );                           # Dummy (command)

$status_byte |=  BP_CS;                     # CS high

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );


# === Check status byte ===
say "Reading status byte...";

$status_byte &= ~BP_CS;                     # CS low

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

$port->write( "\x11" );                     # Bulk SPI transfer: 2 bytes
usleep ( 20000 );
die "Failed bulk read/write." if ( $port->read( 1 ) ne "\x01" );

$port->write( RDSR );                       # Bulk 0: command
$port->write( "\x00" );                     # Bulk 1: dummy

usleep( 40000 );

$return = $port->read( 1 );                 # Dummy (command)
$return = $port->read( 1 );                 # Read reply

say "Status: " . _pretty_hex( $return );
warn "Status isn't 0x20, write to device probably failed.  Check your connections." unless ( $return eq "\x20" );

$status_byte |=  BP_CS;                     # CS high

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );


# === Erase chip ===
say "Erasing chip...";

$status_byte &= ~BP_CS;                     # CS low

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

$port->write( "\x10" );                     # Bulk SPI transfer: 1 byte
usleep ( 20000 );
die "Failed bulk read/write." if ( $port->read( 1 ) ne "\x01" );

$port->write( ERASE_ALL );                  # Bulk 0: command
usleep( 40000 );

$port->read( 1 );                           # Dummy (command)

$status_byte |=  BP_CS;                     # CS high

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

# Spin until device is finished erasing
do {
    $status_byte &= ~BP_CS;                 # CS low

    $port->write( $status_byte );           # Write status
    usleep ( 200000 );
    die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

    $port->write( "\x11" );                 # Bulk SPI transfer: 2 bytes
    usleep ( 20000 );
    die "Failed bulk read/write." if ( $port->read( 1 ) ne "\x01" );

    $port->write( RDSR );                   # Bulk 0: command
    $port->write( "\x00" );                 # Bulk 1: dummy

    usleep( 40000 );

    $return = $port->read( 1 );             # Dummy (command)
    $return = $port->read( 1 );             # Read reply

    $status_byte |=  BP_CS;                 # CS high

    $port->write( $status_byte );           # Write status
    usleep ( 200000 );
    die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );
} while ( $return ne "\x00" );


# === Set write enable again ===
say "Enabling programming...";

$status_byte &= ~BP_CS;                     # CS low

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

$port->write( "\x10" );                     # Bulk SPI transfer: 1 byte
usleep ( 20000 );
die "Failed bulk read/write." if ( $port->read( 1 ) ne "\x01" );

$port->write( WREN );                       # Bulk 0: command
usleep( 40000 );

$port->read( 1 );                           # Dummy (command)

$status_byte |=  BP_CS;                     # CS high

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );


# === Check status byte ===
say "Reading status byte...";

$status_byte &= ~BP_CS;                     # CS low

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

$port->write( "\x11" );                     # Bulk SPI transfer: 2 bytes
usleep ( 20000 );
die "Failed bulk read/write." if ( $port->read( 1 ) ne "\x01" );

$port->write( RDSR );                       # Bulk 0: command
$port->write( "\x00" );                     # Bulk 1: dummy

usleep( 40000 );

$return = $port->read( 1 );                 # Dummy (command)
$return = $port->read( 1 );                 # Read reply

say "Status: " . _pretty_hex( $return );
warn "Status isn't 0x20, write to device probably failed.  Check your connections." unless ( $return eq "\x20" );

$status_byte |=  BP_CS;                     # CS high

$port->write( $status_byte );               # Write status
usleep ( 200000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );


# === Program device ===
say "Programming device...";

open INPUT, "<", $opts{input};              # Open binary file
binmode( INPUT );                           # Switch to binary mode

$/ = \2;                                    # Set record size (1 bytes)
$| = 1;                                     # Set autoflush off

my $addr = 0;

while ( <INPUT> ) {
    my $data = $_;

    # === Enable writing ===
    $status_byte &= ~BP_CS;                 # CS low

    $port->write( $status_byte );           # Write status
    usleep ( 20000 );
    die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

    $port->write( "\x10" );                 # Bulk SPI transfer: 1 byte
    usleep ( 20000 );
    die "Failed bulk read/write." if ( $port->read( 1 ) ne "\x01" );

    $port->write( WREN );                   # Bulk 0: command
    usleep( 40000 );

    $port->read( 1 );                       # Dummy (command)

    $status_byte |=  BP_CS;                 # CS high

    $port->write( $status_byte );           # Write status
    usleep ( 20000 );
    die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );


    # === Program 2 bytes ===
    $status_byte &= ~BP_CS;                 # CS low

    $port->write( $status_byte );           # Write status
    usleep ( 20000 );
    die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

    $port->write( "\x14" );                 # Bulk SPI transfer: 5 bytes
    usleep ( 20000 );
    die "Failed bulk read/write." if ( $port->read( 1 ) ne "\x01" );

    $port->write( PROGRAM );                # Bulk 0: command
    $port->write( pack( "S>", $addr ) );    # Bulk 1, 2: address
    $port->write( $data );                  # Bulk 3, 4: data

    say unpack("H*", pack( "S>", $addr) ) . " : " . unpack("H*", $data);

    usleep( 50000 );

    $port->read( 5 );                       # Dummy (data)

    $status_byte |=  BP_CS;                 # CS high

    $port->write( $status_byte );           # Write status
    usleep ( 30000 );
    die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

    $addr += 2;
}

print STDOUT "\n";

# TODO: verify!

# tear down device
say "Cleaning up...";

$status_byte &= ~BP_AUX;                    # PROG low

$port->write( $status_byte );               # Write status
usleep( 40000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

$status_byte &= ~BP_POWER;                  # POWER low

$port->write( $status_byte );               # Write status
usleep( 40000 );
die "Unable to set status." if ( $port->read( 1 ) ne "\x01" );

0;


# Helper functions
sub _pretty_hex {
    my $return = shift;

    $return = unpack( "H*", $return );
    ($return = $return) =~ s/(....)/$1 /g;
    ($return = $return) =~ s/(?=.{41})(.{40})/$1\n/g;

    return $return;
}
