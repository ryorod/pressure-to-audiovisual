#!/usr/bin/python

import spidev
import time
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

#Define Variables
delay = 0.05
pad_channel_1 = 0
pad_channel_2 = 1

#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000

def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

if __name__ == "__main__":
    try:
        while True:
            pad_value_1 = readadc(pad_channel_1)
            pad_value_2 = readadc(pad_channel_2)
            print("---------------------------------------")
            print("Pressure Pad Value: %d %d" % (pad_value_1, pad_value_2))
            parser = argparse.ArgumentParser()
            parser.add_argument("--ip", default="192.168.11.5",
                                help="The ip of the OSC server")
            parser.add_argument("--port", type=int, default=8000,
                                help="The port the OSC server is listening on")
            args = parser.parse_args()

            client = udp_client.SimpleUDPClient(args.ip, args.port)
            
            client.send_message("/pressure", "%d %d" % (pad_value_1, pad_value_2))
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
