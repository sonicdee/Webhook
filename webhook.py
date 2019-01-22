# -*- coding: utf-8 -*-
"""
@author: linus
"""
#installieren:
# flask
# requests

#von fhem aufrufen alle x min:
#http://127.0.0.1:5000/getsensors

#http://127.0.0.1:5000/webhook?arg1=hello&arg2=world
#http://127.0.0.1:5000/shutdown

#URL und Fhemseitig:
#Relais:
#http://127.0.0.1:5000/mainpump?state=anack auack
#PoolPumpe "curl http://192.168.178.73:5000/mainpump?state=$EVTPART0"

#Pumpe:
#http://127.0.0.1:5000/phpdo?do:=value 7
#PoolDosierPumpePH "curl http://192.168.178.73:5000/phdo?$EVTPART0=$EVTPART1"

#Kansiter füllen (sende 0 gepumpt zu Pumpe):
#http://127.0.0.1:5000/clnewcan?missing=0
#http://127.0.0.1:5000/phnewcan?missing=0

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

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/getsensors', methods=['GET'])
def getsensors():
    #recieve sensor values from local sensors
    ##>from sensors
    logger.debug('/getsensors')

    ph = sensors.ph()
    orp = sensors.orp()
    temp = sensors.temp()

    ph_liq = pumps.get_ph_fill()
    cl_liq = pumps.get_cl_fill()

    ##pump flow rate
    ph_flow = pumps.get_ph()
    cl_flow = pumps.get_cl()

    #then send sensor values to fhem
    webhook('PoolPHadd',ph_flow) #trueflow
    webhook('PoolORPadd',cl_flow) #trueflow
    webhook('PoolPH',ph)
    webhook('PoolORP',orp)
    webhook('PoolTemp',temp)
    webhook('PoolPHkanister',ph_liq)
    webhook('PoolORPkanister',cl_liq)   
   
    return '', 200

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
            actors.is_mainpump
            logger.debug('anack -> Pumpe angeschaltet')

            #->Setzte Fhem
            webhook('PoolPumpe','an')
            logger.debug('an zu Fhem -> Pumpe angeschaltet')

            return 'Pumpe angeschaltet'
        elif state == 'auack':
            logger.debug('auack -> Pumpe ausschalten')
            #->Relais ausschalten
            actors.set_mainpump(False)

            #->Relais ausgeschalten?
            actors.is_mainpump
            logger.debug('auack -> Pumpe ausgeschaltet')

            #->Setzte Fhem
            webhook('PoolPumpe','aus')
            logger.debug('aus zu Fhem -> Pumpe ausgeschaltet')

            return 'Pumpe ausgeschaltet'
        return '', 200
    else:
        abort(400)

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
            actors.is_heatpump
            logger.debug('auack -> WaPumpe ausgeschaltet')

            #->wenn ja, setzte Fhem
            webhook('PoolWaPumpe','aus')
            logger.debug('aus zu Fhem -> Pumpe ausgeschaltet')

            return 'WaermePumpe ausgeschaltet'
        return '', 200
    else:
        abort(400)

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
            actors.is_light
            logger.debug('auack -> Licht ausgeschaltet')

            #->wenn ja, setzte Fhem
            webhook('PoolLight','aus')
            logger.debug('aus zu Fhem -> Licht ausgeschaltet')

            return 'Licht ausgeschaltet'
        return '', 200
    else:
        abort(400)
        
@app.route('/orpdo', methods=['GET'])
def orpdo():
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

@app.route('/phdo', methods=['GET'])
def phdo():
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

    #todo: beim starten stand and fhem senden !?, bzw. einen Stand annehmen!?