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
ph_can = 25000 #fixed value here
cl_can = 25000 #fixed value here

def set_ph(value):
    logger.debug('set_ph ' + str(value))
    #set ml/min flow value
    print("set_ph: ", str(value))

def get_ph():
    logger.debug('get_ph')
    #get ml/min flow value
    value = 20
    return value

def get_ph_fill():
    logger.debug('get_ph_fill')
    # logger.debug('get_ph_fill)
    #get pumped liquds ml from pump
    ph_pumped = 200 #>from pump

    return  ph_can - ph_pumped

def set_ph_fill(value):
    logger.debug('set_ph_fill ' + str(value))
    #set ml filling value

    #set pump to zero with command:
    #http://127.0.0.1:5000/phnewcan?missing=0
    print("set_ph_fill: ", value)

def set_cl(value):
    logger.debug('set_cl ' + str(value))
    #set ml/min flow value
    print("set_cl: ", value)

def get_cl():
    logger.debug('get_cl')
    #get ml/min flow value
    value = 20
    return value

def get_cl_fill():
    logger.debug('get_cl_fill')
    #get pumped liquds ml from pump
    cl_pumped = 300 #>from pump

    return  cl_can - cl_pumped

def set_cl_fill(value):
    logger.debug('set_cl_fill ' + str(value))
    #set ml filling value

    #set pump to zero with command:
    #http://127.0.0.1:5000/clnewcan?missing=0
    print("set_cl_fill: ", str(value))