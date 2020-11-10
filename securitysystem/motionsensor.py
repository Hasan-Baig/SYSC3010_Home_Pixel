#!/usr/bin/env python3

"""
Purpose:
Record motion detected by PIR sensor
"""

import logging
from gpiozero import MotionSensor as motion
from time import sleep
from datetime import datetime

MOTION_INPUT = 23
MOTION_POLL_TIME_SECS = 3

class MotionSensor:

    def __init__(self, pin=MOTION_INPUT): 
        self.__pin = pin
        motion = MotionSensor(self.__pin)

    def check_input(self):
        if motion.wait_for_motion():
            timestamp = "{0:%H}:{0:%M}:{0:%S}"
            datestamp = "{0:%Y}-{0:%m}-{0:%d}"
            logging.debug("Motion Detected!")
            movement = True 
        return movement, datestamp, timestamp 

def motionsensor_test():
    try:
        mts = MotionSensor()
        while True:
            result = mts.check_input()
            if(result[0]):
                sleep(MOTION_POLL_TIME_SECS)
    except KeyboardInterrupt:
        logging.info('Exiting')
    except BaseException:
        logging.error('An error or exception occurred!')
    finally:
        motion.close()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    motionsensor_test()
    
    