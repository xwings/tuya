import struct
from klks_commoncode import bpnrf24lReader

nrf_reader = bpnrf24lReader()
nrf_reader.connect("/dev/ttyUSB0")

if not nrf_reader.can_read_infopage():
    print "The firmware has the FSR_RDISIP, reading of the infopage is disabled"
    nrf_reader.disconnect()
    sys.exit()

#Dump infopage
nrf_reader.enable_read_infopage()
nrf_reader.parse_fsr()
print "=== Dumping Infopage ==="

data = nrf_reader.dump_infopage()

with open("infopage2.hex", "wb") as f:
    f.write(data)

nrf_reader.parse_fsr()
nrf_reader.disconnect()