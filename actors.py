# -*- coding: utf-8 -*-
"""
@author: linus
"""

import time
import smbus
import signal
import sys

#a raspberry pi relais-shield

#globals
bus = smbus.SMBus(1) 
DEVICE_ADDRESS = 0x20 #7 bit address (will be left shifted to add the read write
DEVICE_REG_MODE1 = 0x06
DEVICE_REG_DATA = 0xff

def set_mainpump(onoff):
    global bus
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_DATA

    if onoff == True:
        DEVICE_REG_DATA &= ~(0x1<<0) 
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

    if onoff == False:
        DEVICE_REG_DATA |= (0x1<<0)
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

def is_mainpump():
    bytedata = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
    if bytedata == 254:
        onoff = True
    if bytedata == 255:
        onoff = False
    return onoff

def set_heatpump(onoff):
    global bus
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_DATA

    if onoff == True:
        DEVICE_REG_DATA &= ~(0x1<<1) 
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

    if onoff == False:
        DEVICE_REG_DATA |= (0x1<<1)
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

def is_heatpump():
    # bytedata = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
    # if bytedata == 254:
    #     onoff = True
    # if bytedata == 255:
    #     onoff = False
    return True

def set_light(onoff):
    global bus
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_DATA

    if onoff == True:
        DEVICE_REG_DATA &= ~(0x1<<2) 
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

    if onoff == False:
        DEVICE_REG_DATA |= (0x1<<2)
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

def is_light():
    # bytedata = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
    # if bytedata == 254:
    #     onoff = True
    # if bytedata == 255:
    #     onoff = False
    return True