# -*- coding: utf-8 -*-
"""
@author: linus
"""
#a raspberry pi relais-shield
debugmainpump = False

def set_mainpump(onoff):
    global debugmainpump
    debugmainpump = onoff
    #set on/off!
    print(onoff)

def is_mainpump():
    global debugmainpump
    onoff = debugmainpump #>is on/off?
    return onoff

def set_heatpump(onoff):
    #set on/off!
    print(onoff)

def is_heatpump():
    #>is on/off?
    return True

def set_light(onoff):
    #set on/off!
    print(onoff)

def is_light():
    #>is on/off?
    return True