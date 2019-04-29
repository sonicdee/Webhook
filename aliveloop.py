# -*- coding: utf-8 -*-
"""
@author: linus
"""

#installieren:
# requests

import threading
import time
import datetime
import requests

import logging
from logging.handlers import TimedRotatingFileHandler

#my modules
#import sensors
import actors
import pumps

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('aliveloop.log', 
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)
#logger.setLevel(logging.DEBUG)

class ThreadingAlive(object):
    """ Threading class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=30):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        logger.debug('!running forever now!')
        while True:
            #do some work in background
            logger.debug('!Checking state for security reasons, now!')

            print(' .checking Mainpump')
            if actors.is_mainpump() == False:
                logger.debug("  !! Mainpump is off!! -> stopping PH and CL")
                logger.warning("!! Mainpump is off!! -> stopping PH and CL")

                pumps.set_cl(0)
                clnow = pumps.get_cl()
                logger.debug("    CL flow is now: " + clnow)

                pumps.set_ph(0)
                phnow = pumps.get_ph()
                logger.debug("    PH flow is now: " + phnow)
            else:
                logger.debug("  ..is on")            

            #check fhem is alive -> commandserver
            logger.debug(" .checking Fhem")
            url = 'http://192.168.178.25:8087/fhem?cmd.Dummy=set%20' + 'PoolAliveCheck' + '%20' + str(datetime.datetime.utcnow()+datetime.timedelta(hours=2))
            try:
                requests.get(url,timeout=7)
                logger.debug("  ..is alive")
            except requests.exceptions.ConnectionError:
                logger.debug("  !! Fhem not reachable -> stopping PH and CL")
                logger.warning("!! Fhem not reachable -> stopping PH and CL")

                pumps.set_cl(0)
                clnow = pumps.get_cl()
                logger.debug("    CL flow is now: " + clnow)

                pumps.set_ph(0)
                phnow = pumps.get_ph()
                logger.debug("    PH flow is now: " + phnow)
            pass

            logger.debug("!Check done!")
            time.sleep(self.interval)

aliveobject = ThreadingAlive()
#time.sleep(3)
#print('Do some start routine')
#time.sleep(2)
#print('Some more')