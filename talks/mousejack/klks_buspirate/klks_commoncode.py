import sys
import struct
from pyBusPirateLite.SPI import *

class bpnrf24lReader:
    def __init__(self):
        self.status_byte = PinCfg.POWER | PinCfg.CS
        self.spi = None

        # SPI Commands
        self.SPI_WREN        = 0x06             #Set flash write enable,FSR.WEN
        self.SPI_WRDIS       = 0x04            #Reset flash write enable, FSR.WEN
        self.SPI_RDSR        = 0x05             #Read Flash Status Register (FSR)
        self.SPI_WRSR        = 0x01
        self.SPI_READ        = 0x03
        self.SPI_PROGRAM     = 0x02
        self.SPI_ERASEPAGE   = 0x52
        self.SPI_ERASEALL    = 0x62
        self.SPI_RDFPCR      = 0x89
        self.SPI_RDISIP      = 0x84
        self.SPI_RDISMB      = 0x85
        self.SPI_ENDEBUG     = 0x86

        #FSR Bits
        self.FSR_RESERVED = 0
        self.FSR_RDISIP   = 1
        self.FSR_RDISMB   = 2
        self.FSR_INFEN    = 3
        self.FSR_RDYN     = 4
        self.FSR_WEN      = 5
        self.FSR_STP      = 6
        self.FSR_DBG      = 7

    def connect(self, usb_port):
        self.spi = SPI(usb_port, 115200)

        print "Entering binmode: ",
        if self.spi.BBmode():
            print "OK."
        else:
            print "failed."
            sys.exit()

        print "Entering raw SPI mode: ",
        if self.spi.enter_SPI():
            print "OK."
        else:
            print "failed."
            sys.exit()

        print "Configuring SPI."
        if not self.spi.cfg_pins(self.status_byte):
            print "Failed to set SPI peripherals."
            sys.exit()
        if not self.spi.set_speed(SPISpeed._2_6MHZ):
            print "Failed to set SPI Speed."
            sys.exit()
        if not self.spi.cfg_spi(SPICfg.CLK_EDGE | SPICfg.OUT_TYPE):
            print "Failed to set SPI configuration.";
            sys.exit()
        self.spi.timeout(0.2)

        #Bring PROG to High
        self.status_byte |= PinCfg.AUX
        if not self.spi.cfg_pins(self.status_byte):
            print "Failed to set PROG pin to HIGH"
            sys.exit()

    def disconnect(self):
        #Cleanup
        print "Reset Bus Pirate to user terminal: ",
        if self.spi.resetBP():
            print "OK."
        else:
            print "failed."
            sys.exit()

    def set_CS(self, status_flip, onfail_exit = False):
        if status_flip:
            self.status_byte &= ~PinCfg.CS;
        else:
            self.status_byte |= PinCfg.CS;

        if not self.spi.cfg_pins(self.status_byte):
            print "send_spi_command : Failed to enable writing."
            if onfail_exit: sys.exit()

    def send_spi_command(self, data=[]):
        return self.spi.bulk_trans(len(data), data)

    def is_bit_set(self, check, bit):
        return (check & (1 << bit) != 0)

    def set_bit(self, check, bit):
        return check | (1 << bit)

    def unset_bit(self, check, bit):
        return check & ~(1 << bit)

    def get_fsr(self):
        self.set_CS(True, True)
        ret = self.send_spi_command([self.SPI_RDSR, 0x00])[1]
        #print "get_fsr() returned : " + repr(ret)
        self.set_CS(False, True)
        return ord(ret)

    def parse_fsr(self, fsr=None):
        fsr_string = ["FSR_RESERVED", "FSR_RDISIP", "FSR_RDISMB", "FSR_INFEN", "FSR_RDYN", "FSR_WEN", "FSR_STP", "FSR_DBG"]
        print "=== Parsing FSR START ==="
        if not fsr:
            fsr = self.get_fsr()
        #print repr(fsr)
        for i in xrange(8):
            if self.is_bit_set(fsr, i):
                print "%s bit is set" % (fsr_string[i])
        print "=== Parsing FSR END ==="
        return fsr

    def enable_read_infopage(self, disable_infopage = False):
        fsr = self.get_fsr()

        if disable_infopage:
            fsr = self.unset_bit(fsr, self.FSR_INFEN)
        else:
            fsr = self.set_bit(fsr, self.FSR_INFEN)

        self.set_CS(True, True)    
        if not self.send_spi_command([self.SPI_WRSR, fsr]):
            print "enable_write() failed"
            sys.exit()
        self.set_CS(False, True)

    def enable_write(self):
        self.set_CS(True, True)
        if not self.send_spi_command([self.SPI_WREN,]):
            print "enable_write() failed"
            sys.exit()
        self.set_CS(False, True)

    def erase_chip(self):
        print "Erasing Mainblock..."
        #Enable writing of chip
        self.enable_write()
        ret = self.get_fsr()

        if ret != 0x20 and ret != 0x24:
            print "Incorrect status, 0x%x returned, erase_chip probably failed. Check your connections." % (ret)

        self.set_CS(True, True)
        self.send_spi_command([self.SPI_ERASEALL])
        self.set_CS(False, True)

        while True:
            ret = self.get_fsr()
            if ret == 0x00 or ret == 0x08:  #FSR_INFEN may be flagged
                break

    def erase_page(self, page): #Each page is 512 bytes and contain 8 blocks
        print "Erasing Page : %d" % (page)
        self.enable_write()

        ret = self.get_fsr()
        if ret != 0x20 and ret != 0x28 and ret != 0x2C:
            print "Incorrect status, 0x%x returned, erase_page probably failed. Check your connections." % (ret)

        self.set_CS(True, True)
        self.send_spi_command([self.SPI_ERASEPAGE,] + map(ord, list(struct.pack(">B",page))) )
        self.set_CS(False, True)

        while True:
            ret = self.get_fsr()
            if ret == 0x00 or ret == 0x08:  #FSR_INFEN may be flagged
                break

    def program_data(self, rom_data, start_address = 0):
        print "=== PROGRAM CHIP START ==="
        split_length = 4

        #pad rom data to be % split_length == 0
        if len(rom_data) % split_length != 0:
            rom_data = rom_data + ("\xFF" * (split_length-len(rom_data) % split_length))

        self.enable_write()
        ret = self.get_fsr()
        if ret != 0x20 and ret != 0x28:  #FSR_INFEN may be flagged
            print "Incorrect status, 0x%x returned, program_data probably failed. Check your connections." % (ret)
        
        rom_data_split = [rom_data[i:i+split_length] for i in range(0, len(rom_data), split_length)]

        pAddress = start_address
        for d in rom_data_split:
            self.enable_write() #Enable writing

            #Program bytes
            print "%.4X : %s" % (pAddress, repr(map(ord,list(d))))
            self.set_CS(True, True)
            self.send_spi_command([self.SPI_PROGRAM,] + map(ord, list(struct.pack(">H",pAddress)) + list(d)))
            self.set_CS(False, True)

            pAddress += split_length

        print "=== PROGRAM CHIP END ==="

    def can_read_infopage(self):
        fsr = self.get_fsr()
        if self.is_bit_set(fsr, self.FSR_RDISIP):
            return False
        return True

    def is_chip_protected(self):
        #This check can be used to see if we can read data from MB and write to IP
        fsr = self.get_fsr()
        if self.is_bit_set(fsr, self.FSR_RDISMB):
            return True
        return False

    def dump_rom(self, max_size):
        return_data = ""
        for pAddress in xrange(max_size/4):
            spi_read_cmd = [self.SPI_READ,] + map(ord, list(struct.pack(">H",pAddress*4))) + [0, 0, 0, 0]
            #print "Sending SPI command: " + repr(spi_read_cmd)

            self.set_CS(True, True)
            ret = self.send_spi_command(spi_read_cmd)
            self.set_CS(False, True)

            print "%.4X : %s" % (pAddress*4, repr(map(ord,list(ret[3:]))))
            return_data += "".join(ret[3:])
        return return_data

    def dump_infopage(self):
        if not self.can_read_infopage(): return None
        return_data = ""
        self.enable_read_infopage()
        return_data = self.dump_rom(512)
        self.enable_read_infopage(disable_infopage=True)
        return return_data

    def dump_mainblock(self, is_16kb = False):
        if self.is_chip_protected(): return None

        read_size = 0x8000
        if is_16kb:
            read_size = 0x4000

        return_data = ""
        return_data = self.dump_rom(read_size)
        return return_data