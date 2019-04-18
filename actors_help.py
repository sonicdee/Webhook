# -*- coding: utf-8 -*-
"""
@author: linus
"""

import time
#import smbus2 as smbus #debug from windows
import smbus
import signal
import sys

#globals
bus = smbus.SMBus(1) 
DEVICE_ADDRESS = 0x20 #7 bit address (will be left shifted to add the read write
DEVICE_REG_MODE1 = 0x06
DEVICE_REG_DATA = 0xff

bytedata = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)

print(bytedata)