# -*- coding: utf-8 -*-
"""
@author: linus
"""
#atlas scientifc probes - on - tentacle 3 shield

#adresses:
#EZO pH: 99 (0x63) (default)
#EZO ORP: 98 (0x62) (default)
#EZO RTD: 102 (0x66) (default)

import random #for testing purpose

#atlas scientific code
from atlas import AtlasI2C

def ph():
    #>from sensor
    phsens = AtlasI2C()
    phsens.set_i2c_address(99)
    ph = phsens.query("R")
    #ph = random.randint(72,75)/10
    ph = ph.replace('\x00','')
    return ph

def orp():
    #>from sensor
    orpsens = AtlasI2C()
    orpsens.set_i2c_address(98)
    orp = orpsens.query("R")
    #orp = random.randint(660,750)
    orp = orp.replace('\x00','')
    return orp

def temp():
    #>from sensor
    # tempsens = AtlasI2C()
    # tempsens.set_i2c_address(102)
    # temp = tempsens.query("R")
    temp = random.randint(17,22)
    # temp = temp.replace('\x00','')
    return temp

