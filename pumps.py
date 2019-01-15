# -*- coding: utf-8 -*-
"""
@author: linus
"""
#ezo pumps from atlas scientific - on - tentacle 3 shield

#adresses:
#EZO PMP: 103 (0x67) (default)
#EZO PMP: 104 -> not default needed to be set

##pump can liquids (ml of can)
ph_can = 25000 #fixed value here
cl_can = 25000 #fixed value here

def set_ph(value):
    #set ml/min flow value
    print(value)

def get_ph():
    #get ml/min flow value
    value = 20
    return value

def get_ph_fill():
    #get pumped liquds ml from pump
    ph_pumped = 200 #>from pump

    return  ph_can - ph_pumped

def set_ph_fill(value):
    #set ml filling value

    #set pump to zero with command:
    #http://127.0.0.1:5000/phnewcan?missing=0
    print(value)

def set_cl(value):
    #set ml/min flow value
    print(value)

def get_cl():
    #get ml/min flow value
    value = 20
    return value

def get_cl_fill():
    #get pumped liquds ml from pump
    cl_pumped = 300 #>from pump

    return  cl_can - cl_pumped

def set_cl_fill(value):
    #set ml filling value

    #set pump to zero with command:
    #http://127.0.0.1:5000/clnewcan?missing=0
    print(value)