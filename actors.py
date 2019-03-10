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
mainpump_on = [248,250,252,254]
mainpump_off = [249,251,253,255]
heatpump_on = [249,252,253]
heatpump_off = [251,254,255]
light_on = [249,250,251]
light_off = [253,254,255]

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
    global mainpump_on
    global mainpump_off

    bytedata = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
    if bytedata in mainpump_on:
        onoff = True
    if bytedata in mainpump_off:
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
    global heatpump_on
    global heatpump_off
    
    bytedata = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
    if bytedata in heatpump_on:
        onoff = True
    if bytedata in heatpump_off:
        onoff = False
    return onoff

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
    global light_on
    global light_off
    
    bytedata = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
    if bytedata in light_on:
        onoff = True
    if bytedata in light_off:
        onoff = False
    return onoff