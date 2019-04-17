# -*- coding: utf-8 -*-
"""
@author: linus
"""

import time
#import smbus2 as smbus #debug from windows
import smbus
import signal
import sys

#a raspberry pi relais-shield

#globals
bus = smbus.SMBus(1) 
DEVICE_ADDRESS = 0x20 #7 bit address (will be left shifted to add the read write
DEVICE_REG_MODE1 = 0x06
DEVICE_REG_DATA = 0xff

#port1: mainpump
mainpump_on = [240,242,244,246,248,250,252,254]
mainpump_off = [241,243,245,247,249,251,253,255]

#port3: heatpump -> broken !
heatpump_on = [240,241,242,243,248,249,250,251]
heatpump_off = [244,245,246,247,252,253,254,255]

#port2: light
light_on = [240,241,244,245,248,249,252,253]
light_off = [242,243,246,247,250,251,254,255]

#port4: ezo pumps
ezo_on = [240,241,242,243,244,245,246,247]
ezo_off = [248,249,250,251,252,253,254,255]


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
        DEVICE_REG_DATA &= ~(0x1<<2) 
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

    if onoff == False:
        DEVICE_REG_DATA |= (0x1<<2)
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
        DEVICE_REG_DATA &= ~(0x1<<1) 
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

    if onoff == False:
        DEVICE_REG_DATA |= (0x1<<1)
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

def set_ezo(onoff):
    global bus
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_DATA

    if onoff == True:
        DEVICE_REG_DATA &= ~(0x1<<3) 
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

    if onoff == False:
        DEVICE_REG_DATA |= (0x1<<3)
        bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)

def is_ezo():
    global ezo_on
    global ezo_off
    
    bytedata = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
    if bytedata in ezo_on:
        onoff = True
    if bytedata in ezo_off:
        onoff = False
    return onoff