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

#my modules
#import sensors
import actors
import pumps

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
        while True:
            #do some work in background
            print('!Checking state for security reasons, now!')

            print(' .checking Mainpump')
            if actors.is_mainpump() == False:
                print("  !! Mainpump is off!! -> stopping PH and CL")
                pumps.set_cl(0)
                clnow = pumps.get_cl()
                print("    CL flow is now:", clnow)

                pumps.set_ph(0)
                phnow = pumps.get_ph()
                print("    PH flow is now:", phnow)
            else:
                print("  ..is on")            

            #check fhem is alive -> commandserver
            print(' .checking Fhem')
            url = 'http://192.168.178.25:8087/fhem?cmd.Dummy=set%20' + 'PoolAliveCheck' + '%20' + str(datetime.datetime.now())
            try:
                requests.get(url,timeout=2)
                print("  ..is alive")
            except requests.exceptions.ConnectionError:
                print("  !! Fhem not reachable -> stopping PH and CL")
                pumps.set_cl(0)
                clnow = pumps.get_cl()
                print("    CL flow is now:", clnow)

                pumps.set_ph(0)
                phnow = pumps.get_ph()
                print("    PH flow is now:", phnow)
            pass
               
            

            print('!Check done!')
            time.sleep(self.interval)

aliveobject = ThreadingAlive()
#time.sleep(3)
#print('Do some start routine')
#time.sleep(2)
#print('Some more')