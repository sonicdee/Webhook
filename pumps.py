# -*- coding: utf-8 -*-
"""
@author: linus
"""
#ezo pumps from atlas scientific - on - tentacle 3 shield

#adresses:
#EZO PMP: 103 (0x67) (default)
#EZO PMP: 104 -> not default needed to be set

import logging
from logging.handlers import TimedRotatingFileHandler

#atlas scientific code
from atlas import AtlasI2C

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('pumps.log', 
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.CRITICAL)

##pump can liquids (ml of can)
ph_can = 20000.00 #fixed value here
cl_can = 20000.00 #fixed value here

debugph = 0.0
debugcl = 0.0

debugphfill = 0.0
debugclfill = 0.0

#fixing values of the pump to a lower flow:
#my EZO PMP: 105ml/min = 6,3 l/h !
#Behncke SplashControl = 0,8 l/h -> 13ml/min
#Bayrohl Automatic     = 1,5 l/h -> 25ml/min
#Swimtec Dosph basic   = 1,6 l/h -> 26ml/min
limitflow = 25.0

def set_ph(value):
    #global debugph

    if float(value) > limitflow:
        value = limitflow
    
    logger.debug('set_ph ' + str(value))
    #set ml/min flow value
    print("set_ph: ", str(value))
    #debugph = value
    phpump = AtlasI2C()
    phpump.set_i2c_address(103)
    if float(value) == 0:
        value = phpump.query("X") #stop dispensing
    else:
        value = phpump.query("D," + str(value) +",1") #D = fixed volume on 1 minute
def get_ph():
    #global debugph
    #logger.debug('get_ph')
    
    #get ml/min flow value
    phpump = AtlasI2C()
    phpump.set_i2c_address(103)
    value = phpump.query("D,?").split(",")[1] # = ?D,5.00,1
    #value = debugph
    return value

def get_ph_fill():
    #global debugph
    #global debugphfill

    logger.debug('get_ph_fill')
    #get pumped liquds ml from pump
    #debugphfill = float(debugphfill) + float(debugph)
    #ph_pumped = debugphfill #>from pump
    phpump = AtlasI2C()
    phpump.set_i2c_address(103)
    ph_pumped = phpump.query("TV,?").split(",")[1].split("\x00")[0] #or "ATV,?"
    return  ph_can - float(ph_pumped)

def set_ph_fill():
    logger.debug('set_ph_fill to zero')
    #set ml filling value

    #set pump to zero with command:
    #http://127.0.0.1:5000/phnewcan?missing=0

    phpump = AtlasI2C()
    phpump.set_i2c_address(103)
    phpump.query("clear")

def set_cl(value):
    #global debugcl

    if float(value) > limitflow:
        value = limitflow

    logger.debug('set_cl ' + str(value))
    #set ml/min flow value
    print("set_cl: ", value)
    #debugcl = value
    clpump = AtlasI2C()
    clpump.set_i2c_address(104)
    if float(value) == 0:
        value = clpump.query("X") #stop dispensing
    else:
        value = clpump.query("D," + str(value) +",1") #dispense value for 1 minute

def get_cl():
    #global debugcl
    #logger.debug('get_cl')
    
    #get ml/min flow value
    clpump = AtlasI2C()
    clpump.set_i2c_address(104)
    value = clpump.query("D,?").split(",")[1] # = ?D,5.00,1
    #value = debugcl
    return value

def get_cl_fill():
    #global debugcl
    #global debugclfill
    logger.debug('get_cl_fill')
    #get pumped liquds ml from pump
    #debugclfill = float(debugclfill) + float(debugcl)
    #cl_pumped = debugclfill #>from pump
    clpump = AtlasI2C()
    clpump.set_i2c_address(104)
    cl_pumped = clpump.query("TV,?").split(",")[1].split("\x00")[0] #or "ATV,?"
    return  cl_can - float(cl_pumped)

def set_cl_fill():
    logger.debug('set_cl_fill')
    #set ml filling value

    #set pump to zero with command:
    #http://127.0.0.1:5000/clnewcan?missing=0
    clpump = AtlasI2C()
    clpump.set_i2c_address(104)
    clpump.query("clear")