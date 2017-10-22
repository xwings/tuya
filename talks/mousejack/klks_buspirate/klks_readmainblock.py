import sys
import struct
from klks_commoncode import bpnrf24lReader

nrf_reader = bpnrf24lReader()
nrf_reader.connect("/dev/ttyUSB0")

nrf_reader.parse_fsr()
if nrf_reader.is_chip_protected():
    print "The firmware has the FSR_RDISMB bit enabled, reading of the mainblock is disabled"
    nrf_reader.disconnect()
    sys.exit()

print "=== Dumping Mainblock ==="

data = nrf_reader.dump_mainblock()

with open("mainblock.hex", "wb") as f:
    f.write(data)

nrf_reader.disconnect()