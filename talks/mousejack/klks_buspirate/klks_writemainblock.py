from klks_commoncode import bpnrf24lReader

input_file = "/root/mousejack/bin/dongle.bin"
#input_file = "test"

with open(input_file, "rb") as f:
    rom_data = f.read()

if len(rom_data)/512 > 64:
	print "Rom data is > 32kb"
	sys.exit()

erase_count = len(rom_data) / 512
if len(rom_data) % 512 != 0 : erase_count += 1

nrf_reader = bpnrf24lReader()
nrf_reader.connect("/dev/ttyUSB0")

#nrf_reader.erase_chip()
for i in xrange(erase_count):
	nrf_reader.erase_page(i)

nrf_reader.program_data(rom_data)

nrf_reader.disconnect()