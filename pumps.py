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

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('pumps.log', 
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

##pump can liquids (ml of can)
ph_can = 25000.00 #fixed value here
cl_can = 25000.00 #fixed value here

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
    global debugph

    if float(value) > limitflow:
        value = limitflow
    
    logger.debug('set_ph ' + str(value))
    #set ml/min flow value
    print("set_ph: ", str(value))
    debugph = value
    
def get_ph():
    global debugph
    logger.debug('get_ph')
    #get ml/min flow value
    value = debugph
    return value

def get_ph_fill():
    global debugph
    global debugphfill

    logger.debug('get_ph_fill')
    # logger.debug('get_ph_fill)
    #get pumped liquds ml from pump
    debugphfill = float(debugphfill) + float(debugph)
    ph_pumped = debugphfill #>from pump

    return  ph_can - ph_pumped

def set_ph_fill(value):
    logger.debug('set_ph_fill ' + str(value))
    #set ml filling value

    #TODO: setzten geht nicht im demomode
    #set pump to zero with command:
    #http://127.0.0.1:5000/phnewcan?missing=0
    print("set_ph_fill: ", value)

def set_cl(value):
    global debugcl

    if float(value) > limitflow:
        value = limitflow

    logger.debug('set_cl ' + str(value))
    #set ml/min flow value
    print("set_cl: ", value)
    debugcl = value

def get_cl():
    global debugcl
    logger.debug('get_cl')
    #get ml/min flow value
    value = debugcl
    return value

def get_cl_fill():
    global debugcl
    global debugclfill
    logger.debug('get_cl_fill')
    #get pumped liquds ml from pump
    debugclfill = float(debugclfill) + float(debugcl)
    cl_pumped = debugclfill #>from pump

    return  cl_can - cl_pumped

def set_cl_fill(value):
    logger.debug('set_cl_fill ' + str(value))
    #set ml filling value
    #TODO: setzten geht nicht im demomode
    #set pump to zero with command:
    #http://127.0.0.1:5000/clnewcan?missing=0
    print("set_cl_fill: ", str(value))