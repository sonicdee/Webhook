# -*- coding: utf-8 -*-
"""
@author: linus
"""
#installieren: flask & requests
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
        state = request.args.get('state', '')
        if state == 'anack':
            #->Relais anschalten
            actors.sw_mainpump(True)

            #->Relais angeschaltet?
            actors.is_mainpump
            print('Pumpe angeschaltet')

            #->Setzte Fhem
            webhook('PoolPumpe','an')

            return 'Pumpe angeschaltet'
        elif state == 'auack':
            #->Relais ausschalten
            actors.sw_mainpump(False)

            #->Relais ausgeschalten?
            actors.is_mainpump
            print("Pumpe ausgeschaltet")

            #->Setzte Fhem
            webhook('PoolPumpe','aus')

            return 'Pumpe ausgeschaltet'
        return '', 200
    else:
        abort(400)

@app.route('/heatpump', methods=['GET'])
def heatpump():
    if request.method == 'GET':
        state = request.args.get('state', '')
        if state == 'anack':
            #->Relais anschalten
            actors.sw_heatpump(True)

            #->Relais angeschaltet?
            actors.is_heatpump
            print('WaermePumpe angeschaltet')

            #->wenn ja, setzte Fhem
            webhook('PoolWaPumpe','an')

            return 'WaermePumpe ausgeschaltet'
        elif state == 'auack':
            #->Relais ausschalten
            actors.sw_heatpump(False)

            #->Relais ausgeschalten?
            actors.is_heatpump
            print("WaermePumpe ausgeschaltet")

            #->wenn ja, setzte Fhem
            webhook('PoolWaPumpe','aus')

            return 'WaermePumpe ausgeschaltet'
        return '', 200
    else:
        abort(400)

@app.route('/light', methods=['GET'])
def light():
    if request.method == 'GET':
        state = request.args.get('state', '')
        if state == 'anack':
            #->Relais anschalten
            actors.sw_light(True)

            #->Relais angeschaltet?
            actors.is_light
            print('Licht angeschaltet')

            #->wenn ja, setzte Fhem
            webhook('PoolLight','an')

            return 'Licht ausgeschaltet'
        elif state == 'auack':
            #->Relais ausschalten
            actors.sw_light(False)

            #->Relais ausgeschalten?
            actors.is_light
            print("Licht ausgeschaltet")

            #->wenn ja, setzte Fhem
            webhook('PoolLight','aus')
            return 'Licht ausgeschaltet'
        return '', 200
    else:
        abort(400)
        
@app.route('/orpdo', methods=['GET'])
def orpdo():
    if request.method == 'GET':
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
        missing = request.args.get('missing', '')
        #send to pump
        pumps.set_ph_fill(missing)
        print("PH missing",missing)

        #get value from pump
        state = pumps.get_ph_fill

        #return state
        return "PH missing is now: %s" % (str(state)) , 200
    else:
        abort(400)

@app.route('/clnewcan', methods=['GET'])
def clnewcan():
    if request.method == 'GET':
        missing = request.args.get('missing', '')
        #send to pump
        pumps.set_cl_fill(missing)
        print("CL missing",missing)

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

