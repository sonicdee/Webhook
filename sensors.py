# -*- coding: utf-8 -*-
"""
@author: linus
"""
#atlas scientifc probes - on - tentacle 3 shield

#adresses:
#EZO pH: 99 (0x63) (default)
#EZO ORP: 98 (0x62) (default)
#EZO RTD: 102 (0x66) (default)

import random

def ph():
    #>from sensor
    ph = random.randint(70,74)/10
    return ph

def orp():
    #>from sensor
    orp = random.randint(600,750)
    return orp

def temp():
    #>from sensor
    temp = random.randint(17,22)
    return temp

