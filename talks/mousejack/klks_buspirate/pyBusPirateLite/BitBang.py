#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2009-10-14.
Copyright 2009 Sean Nelson <audiohacked@gmail.com>

This file is part of pyBusPirate.

pyBusPirate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyBusPirate is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyBusPirate.  If not, see <http://www.gnu.org/licenses/>.
"""

import select
import serial
import sys
import time

"""
PICSPEED = 24MHZ / 16MIPS
"""

class PinCfg:
	POWER = 0x8
	PULLUPS = 0x4
	AUX = 0x2
	CS = 0x1

class BBIOPins:
	# Bits are assigned as such:
	MOSI = 0x01;
	CLK = 0x02;
	MISO = 0x04;
	CS = 0x08;
	AUX = 0x10;
	PULLUP = 0x20;
	POWER = 0x40;

class BBIO:
	def __init__(self, p="/dev/bus_pirate", s=115200, t=1):
		self.port = serial.Serial(p, s, timeout=t)
	
	def BBmode(self):
		if sys.platform == 'win32':
			# I haven't seen this problem on Windows, which is good,
			# because it doesn't appear to support select.select() 
			# for serial ports.  This seems to work instead:
			self.resetBP()
			self.port.write("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
			self.timeout(0.1)
			self.port.flushInput();
			self.reset()
		else:
			# Sometimes sending 20 zeroes in a row to a BP already in binary mode
			# leads to BP getting stuck in BitBang mode
			# (see forum: http://dangerousprototypes.com/forum/viewtopic.php?t=1440#msg13179 )
			# so if we detect a response (indicating we're in BitBang mode before the 20 zeroes)
			# stop sending zeroes and go on.
			self.port.flushInput();		
			for i in range(20):
				self.port.write("\x00");
				r,w,e = select.select([self.port], [], [], 0.01);
				if (r): break;

		if self.response(5) == "BBIO1": return 1
		else: return 0

	def reset(self):
		self.port.write("\x00")
		self.timeout(0.1)

	def enter_SPI(self):
		self.response(5)
		self.port.write("\x01")
		self.timeout(0.1)
		if self.response(4) == "SPI1": return 1
		else: return 0

	def enter_I2C(self):
		self.port.write("\x02")
		self.timeout(0.1)
		if self.response(4) == "I2C1": return 1
		else: return 0

	def enter_UART(self):
		self.port.write("\x03")
		self.timeout(0.1)
		if self.response(4) == "ART1": return 1
		else: return 0
		
	def enter_1wire(self):
		self.port.write("\x04")
		self.timeout(0.1)
		if self.response(4) == "1W01": return 1
		else: return 0
		
	def enter_rawwire(self):
		self.port.write("\x05")
		self.timeout(0.1)
		if self.response(4) == "RAW1": return 1
		else: return 0
		
	def resetBP(self):
		self.reset()
		self.port.write("\x0F")
		self.timeout(0.1)
		#self.port.read(2000)
		self.port.flushInput()
		return 1

	def raw_cfg_pins(self, config):
		self.port.write(chr(0x40 | config))
		self.timeout(0.1)
		return self.response(1)

	def raw_set_pins(self, pins):
		self.port.write(chr(0x80 | config))
		self.timeout(0.1)
		return self.response(1)

	def timeout(self, timeout=0.1):
		time.sleep(timeout);

	def response(self, byte_count=1, return_data=False):
		data = self.port.read(byte_count)
		if byte_count == 1 and return_data == False:
			if data == chr(0x01): return 1
			else: return 0
		else:
			return data

	""" Self-Test """
	def short_selftest(self):
		self.port.write("\x10")
		self.timeout(0.1)
		return self.response(1, True)

	def long_selftest(self):
		self.port.write("\x11")
		self.timeout(0.1)
		return self.response(1, True)

	""" PWM """
	def setup_PWM(self, prescaler, dutycycle, period):
		self.port.write("\x12")
		self.port.write(chr(prescaler))
		self.port.write(chr((dutycycle>>8)&0xFF))
		self.port.write(chr(dutycycle&0xFF))
		self.port.write(chr((period>>8)&0xFF))
		self.port.write(chr(period&0xFF))
		self.timeout(0.1)
		return self.response()

	def clear_PWM(self):
		self.port.write("\x13")
		self.timeout(0.1)
		return self.response()

	""" ADC """	
	def ADC_measure(self):
		self.port.write("\x14")
		self.timeout(0.1)
		return self.response(2, True)

	""" General Commands for Higher-Level Modes """
	def mode_string(self):
		self.port.write("\x01")
		self.timeout(0.1)
		return self.response()

	def bulk_trans(self, byte_count=1, byte_string=None):
		#print "bulk xfer : " + repr(byte_string)
		if byte_string == None: pass
		self.port.write(chr(0x10 | (byte_count-1)))
		self.timeout(0.1)
		for i in range(byte_count):
			self.port.write(chr(byte_string[i]))
			#self.timeout(0.1)
		data = self.response(byte_count+1, True)
		#print "bullk xfer resp : " + repr(data[1:])
		if data[0] != "\x01":
			print "Bulk data possibly failed"
		return data[1:]

	def cfg_pins(self, pins=0):
		#print "cfg_pins set to " + hex(int(0x40 | pins))
		self.port.write(chr(0x40 | pins))
		self.timeout(0.1)
		return self.response()

	def read_pins(self):
		self.port.write("\x50")
		self.timeout(0.1)
		return self.response(1, True)

	def set_speed(self, spi_speed=0):
		#print "set_speed set to " + hex(int(0x60 | spi_speed))
		self.port.write(chr(0x60 | spi_speed))
		self.timeout(0.1)
		return self.response()

	def read_speed(self):
		self.port.write("\x70")
		self.timeout(0.1);
		return self.response(1, True)

