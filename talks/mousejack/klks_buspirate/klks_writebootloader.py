from klks_commoncode import bpnrf24lReader

input_file = "7800_bootloader.hex"
#input_file = "test"

with open(input_file, "rb") as f:
    rom_data = f.read()

nrf_reader = bpnrf24lReader()
nrf_reader.connect("/dev/ttyUSB0")

#nrf_reader.erase_chip()
#If this is not a new chip, erase the needed page *TODO*
nrf_reader.program_data(rom_data, start_address=0x7800)

nrf_reader.disconnect()