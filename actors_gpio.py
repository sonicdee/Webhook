# -*- coding: utf-8 -*-
"""
@author: linus
"""

import RPi.GPIO as GPIO
 
#GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen
#GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # aus
#GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # an

#using GPIO https://raspi.tv/2014/rpi-gpio-quick-reference-updated-for-raspberry-pi-b

#port1: mainpump
RELAIS_1_GPIO = 17

#port3: heatpump -> broken !
RELAIS_3_GPIO = 17

#port2: light
RELAIS_2_GPIO = 17

#port4: ezo pumps
RELAIS_4_GPIO = 17

#do i need GPIO.cleanup() on exit

def init():
    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) # GPIO Nummern statt Board Nummern
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
    GPIO.setup(RELAIS_3_GPIO, GPIO.OUT)
    GPIO.setup(RELAIS_2_GPIO, GPIO.OUT)
    GPIO.setup(RELAIS_4_GPIO, GPIO.OUT)

def set_mainpump(onoff):

    if onoff == True:
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # an

    if onoff == False:
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # aus

def is_mainpump():
   
    if GPIO.input(RELAIS_1_GPIO) == 1:
        onoff = True
    else:
        onoff = False
    return onoff

def set_heatpump(onoff):

    if onoff == True:
        GPIO.output(RELAIS_3_GPIO, GPIO.HIGH) # an

    if onoff == False:
        GPIO.output(RELAIS_3_GPIO, GPIO.LOW) # aus

def is_heatpump():
    
    if GPIO.input(RELAIS_3_GPIO) == 1:
        onoff = True
    else:
        onoff = False
    return onoff

def set_light(onoff):

    if onoff == True:
        GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # an

    if onoff == False:
        GPIO.output(RELAIS_2_GPIO, GPIO.LOW) # aus

def is_light():

    if GPIO.input(RELAIS_2_GPIO) == 1:
        onoff = True
    else:
        onoff = False
    return onoff

def set_ezo(onoff):

    if onoff == True:
        GPIO.output(RELAIS_4_GPIO, GPIO.HIGH) # an

    if onoff == False:
        GPIO.output(RELAIS_4_GPIO, GPIO.LOW) # aus

def is_ezo():

    if GPIO.input(RELAIS_4_GPIO) == 1:
        onoff = True
    else:
        onoff = False
    return onoff