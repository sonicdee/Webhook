# -*- coding: utf-8 -*-
"""
@author: linus
"""
#installieren:
# flask
# requests

#http://127.0.0.1:5000/webhook?arg1=hello&arg2=world

from flask import Flask, request, abort
import requests

import logging
from logging.handlers import TimedRotatingFileHandler

#my modules
import sensors
import actors
import pumps
import aliveloop

app = Flask(__name__)

# setting allowed IPs to my local netork and to localhost
#allowed_ips = ['192.168.178.', '127.0.0.1']

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('webhook.log', 
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.warning)

def webhook(device, value):
    url = 'http://192.168.178.25:8087/fhem?cmd.Dummy=set%20' + device + '%20' + str(value)
    try:
        r = requests.get(url,timeout=2)
        logger.debug('webhook url: %s status: %s text: %s', url, r.status_code, r.reason)
    except requests.exceptions.ConnectionError as e:
        logger.warning('webhook url: %s error: %s', url, e.args[0].reason)
    pass

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

#http://127.0.0.1:5000/shutdown
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

#von fhem aufrufen alle 1 min:
#http://192.168.178.103:5000/getsensors
#testen http://127.0.0.1:5000/getsensors
@app.route('/getsensors', methods=['GET'])
def getsensors():
    #recieve sensor values from local sensors
    ##>from sensors
    logger.debug('/getsensors')

    ph = sensors.ph()
    orp = sensors.orp()
    temp = sensors.temp()

    ##pump flow rate
    ph_flow = pumps.get_ph()
    cl_flow = pumps.get_cl()

    ph_liq = pumps.get_ph_fill()
    cl_liq = pumps.get_cl_fill()

    #then send sensor values to fhem
    webhook('PoolPHadd',ph_flow) #trueflow
    webhook('PoolORPadd',cl_flow) #trueflow
    webhook('PoolPH',ph) # set ph first
    webhook('PoolORP',orp) # then orp -> cl is now calculated
    webhook('PoolTemp',temp)
    webhook('PoolPHkanister',ph_liq)
    webhook('PoolORPkanister',cl_liq)   
    
    #check relais states
    if actors.is_mainpump() == True:
        webhook('PoolPumpe','an')
    elif actors.is_mainpump() == False:
        webhook('PoolPumpe','aus')
    #TODO: check relais states of others also: light and wapump

    return '', 200

#URLs und zur Fhemseite:
#http://192.168.178.103:5000/mainpump?state=anack anack
#testen #http://127.0.0.1:5000/mainpump?state=anack
#PoolPumpe Status von Fhem"curl http://192.168.178.103:5000/mainpump?state=$EVTPART0"
@app.route('/mainpump', methods=['GET'])
def mainpump():
    if request.method == 'GET':
        logger.debug('/mainpump')

        state = request.args.get('state', '')
        if state == 'anack':
            logger.debug('anack -> Pumpe anschalten')
            #->Relais anschalten
            actors.set_mainpump(True)

            #->Relais angeschaltet?
            if actors.is_mainpump() == True:
                logger.debug('anack -> Pumpe angeschaltet')
                #->Setzte Fhem
                webhook('PoolPumpe','an')
                logger.debug('an zu Fhem -> Pumpe angeschaltet')
                return 'Pumpe angeschaltet'
            elif actors.is_mainpump() == False:
                logger.warning('anack -> !!! Pumpe anschalten NICHT möglich !')
                return 'Pumpe anschalten NICHT möglich !!'
        elif state == 'auack':
            logger.debug('auack -> Pumpe ausschalten')
            #->Relais ausschalten
            actors.set_mainpump(False)

            #->Relais ausgeschalten?
            if actors.is_mainpump() == False:
                logger.debug('auack -> Pumpe ausgeschaltet')
                
                #wenn ausgeschaltet wird !! dann PHflow und CLflow sofort auf 0 schalten:
                pumps.set_cl(0)
                #get value from pump
                current = pumps.get_cl()
                #then send back to fhem
                webhook('PoolORPadd',str(current))
                        
                #send to pumpS
                pumps.set_ph(0)
                #get value from pump
                current = pumps.get_ph()
                #then send back to fhem
                webhook('PoolPHadd',str(current))

                #->Setzte Fhem
                webhook('PoolPumpe','aus')
                logger.debug('aus zu Fhem -> Pumpe ausgeschaltet')

                return 'Pumpe ausgeschaltet'
            elif actors.is_mainpump() == True:
                logger.warning('auack -> !!! Pumpe ausschalten NICHT möglich !')
                return 'Pumpe ausschalten NICHT möglich !!'
        
            return 'Pumpenfehler'
        return '', 200
    else:
        abort(400)

#http://192.168.178.103:5000/heatpump?state=auack auack
#WärmePumpe Status von Fhem"curl http://192.168.178.103:5000/heatpump?state=$EVTPART0"
@app.route('/heatpump', methods=['GET'])
def heatpump():
    if request.method == 'GET':
        logger.debug('/heatpump')

        state = request.args.get('state', '')
        if state == 'anack':
            logger.debug('anack -> WaPumpe anschalten')
            #->Relais anschalten
            actors.set_heatpump(True)

            #->Relais angeschaltet?
            #TODO:  if actors.is_heatpump() == True:
            actors.is_heatpump
            logger.debug('anack -> WaPumpe angeschaltet')

            #->wenn ja, setzte Fhem
            webhook('PoolWaPumpe','an')
            logger.debug('an zu Fhem -> WaPumpe angeschaltet')

            return 'WaermePumpe ausgeschaltet'
        elif state == 'auack':
            logger.debug('auack -> WaPumpe ausschalten')
            #->Relais ausschalten
            actors.set_heatpump(False)

            #->Relais ausgeschalten?
            #TODO:  if actors.is_heatpump() == False:
            actors.is_heatpump
            logger.debug('auack -> WaPumpe ausgeschaltet')

            #->wenn ja, setzte Fhem
            webhook('PoolWaPumpe','aus')
            logger.debug('aus zu Fhem -> Pumpe ausgeschaltet')

            return 'WaermePumpe ausgeschaltet'
        return '', 200
    else:
        abort(400)

#http://192.168.178.103:5000/light?state=anack auack
#Licht Status von Fhem"curl http://192.168.178.103:5000/light?state=$EVTPART0"
@app.route('/light', methods=['GET'])
def light():
    if request.method == 'GET':
        logger.debug('/light')

        state = request.args.get('state', '')
        if state == 'anack':
            logger.debug('anack -> Licht anschalten')
            #->Relais anschalten
            actors.set_light(True)

            #->Relais angeschaltet?
            #TODO:  if actors.is_light() == True:
            actors.is_light
            logger.debug('anack -> Licht angeschaltet')

            #->wenn ja, setzte Fhem
            webhook('PoolLight','an')
            logger.debug('an zu Fhem -> Licht angeschaltet')

            return 'Licht ausgeschaltet'
        elif state == 'auack':
            #->Relais ausschalten
            logger.debug('auack -> Licht ausschalten')
            actors.set_light(False)

            #->Relais ausgeschalten?
            #TODO:  if actors.is_light() == False:
            actors.is_light
            logger.debug('auack -> Licht ausgeschaltet')

            #->wenn ja, setzte Fhem
            webhook('PoolLight','aus')
            logger.debug('aus zu Fhem -> Licht ausgeschaltet')

            return 'Licht ausgeschaltet'
        return '', 200
    else:
        abort(400)

#DosierPumpen:
#http://192.168.178.103:5000/phdo?do:=77
#testen http://127.0.0.1:5000/phdo?do:=77
#PoolDosierPumpePH Status von Fhem "curl http://192.168.178.103:5000/phdo?$EVTPART0=$EVTPART1"        
@app.route('/orpdo', methods=['GET'])
def orpdo():
      #->Pumpe angeschaltet?
    if actors.is_mainpump() == False:
        pumps.set_ph(0)
        current = pumps.get_ph()
        webhook('PoolPHadd',str(current))
        return 'Pumpe ist ausgeschaltet->setzte 0!'
    if request.method == 'GET':
        logger.debug('/orpdo')

        do = request.args.get('do:', '')

        #send to pump
        pumps.set_cl(do)

        #get value from pump
        current = pumps.get_cl()

        #then send back to fhem
        webhook('PoolORPadd',str(current))
        #http://192.168.178.25:8087/fhem?cmd.Dummy=set%20PoolORPadd%20Wert

        return '', 200
    else:
        abort(400)

#http://192.168.178.103:5000/orpdo?do:=77
#testen http://127.0.0.1:5000/orpdo?do:=77
#PoolDosierPumpePH Status von Fhem "curl http://192.168.178.103:5000/phdo?$EVTPART0=$EVTPART1"
@app.route('/phdo', methods=['GET'])
def phdo():
      #->Pumpe angeschaltet?
    if actors.is_mainpump() == False:
        pumps.set_ph(0)
        current = pumps.get_ph()
        webhook('PoolPHadd',str(current))
        return 'Pumpe ist ausgeschaltet->setzte 0!'
    if request.method == 'GET':
        logger.debug('/phdo')

        do = request.args.get('do:', '')
        
        #send to pump
        pumps.set_ph(do)

        #get value from pump
        current = pumps.get_ph()

        #then send back to fhem
        webhook('PoolPHadd',str(current))
        #http://192.168.178.25:8087/fhem?cmd.Dummy=set%20PoolPHadd%20Wert

        return '', 200
    else:
        abort(400)

#Kansiter füllen (dann muss sende: 0 gepumpt zu Pumpe):
#http://192.168.178.103:5000/clnewcan?missing=0
#http://192.168.178.103:5000/phnewcan?missing=0
@app.route('/phnewcan', methods=['GET'])
def phnewcan():
    if request.method == 'GET':
        logger.debug('/phnewcan')

        missing = request.args.get('missing', '')
        #send to pump
        pumps.set_ph_fill(missing)
        logger.debug("set PH fill: " + missing)

        #get value from pump
        state = pumps.get_ph_fill

        #return state
        return "PH missing is now: %s" % (str(state)) , 200
    else:
        abort(400)

@app.route('/clnewcan', methods=['GET'])
def clnewcan():
    if request.method == 'GET':
        logger.debug('/clnewcan')

        missing = request.args.get('missing', '')
        #send to pump
        pumps.set_cl_fill(missing)
        logger.debug("set CL fill: " + missing)

        #get value from pump
        state = pumps.get_cl_fill #>from pump

        #return state
        return "CL missing is now: %s" % (str(state)) , 200
    else:
        abort(400)

# @app.route('/webhook', methods=['GET'])
# def webhook():
#     if request.method == 'GET':
#         #print(request.json)
#         print(request.args)
#         arg1 = request.args.get('arg1', '')
#         print(arg1)
#         arg2 = request.args.get('arg2', '')
#         print(arg2)
#         return '', 200
#     else:
#         abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    aliveobject = aliveloop.ThreadingAlive
