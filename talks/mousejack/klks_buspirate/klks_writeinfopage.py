import sys
import struct
from klks_commoncode import bpnrf24lReader

input_file = "infopage_edited.hex"

with open(input_file, "rb") as f:
    rom_data = f.read()

nrf_reader = bpnrf24lReader()
nrf_reader.connect("/dev/ttyUSB0")

#Dump infopage
if nrf_reader.is_chip_protected():
    print "Chip is protected, full erase needed..."
    nrf_reader.erase_chip()

nrf_reader.enable_read_infopage()   #We are now reading/writing to the infopage and not mainblock
nrf_reader.erase_page(0)            #Do not use erase_chip method, that will erase the mainblock

print "=== Program Infopage ==="
nrf_reader.program_data(rom_data)

print "=== Dumping Infopage ==="
data = nrf_reader.dump_infopage()

if data != rom_data:
    print "Flashing didnt flash properly..."

nrf_reader.disconnect()