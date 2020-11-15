#!/usr/bin/env python3

"""
Purpose:
Record motion detected by PIR sensor
"""

import logging
from gpiozero import MotionSensor
from time import sleep
from datetime import datetime

MOTION_INPUT = 23
MOTION_POLL_TIME_SECS = 3.5

class MotionSensorClass:

    def __init__(self, mts=MotionSensor(MOTION_INPUT)): 
        self.__mts = mts

    def check_input(self):
        dateNow = "none"
        timeNow = "none"
        if self.__mts.wait_for_motion():
            dateNow = datetime.now().strftime("%Y-%m-%d")
            timeNow = datetime.now().strftime("%H:%M:%S")
            logging.debug("Motion Detected at {}".format(timeNow))
            movement = True 
        return movement, dateNow, timeNow 

    def close_sensor(self):
        self.__mts.close()

def motionsensor_test():
    try:
        mts = MotionSensorClass()
        while True:
            result = mts.check_input()
            if(result[0]):
                sleep(MOTION_POLL_TIME_SECS)
    except KeyboardInterrupt:
        logging.info('Exiting')
    except BaseException as e:
        logging.error('An error or exception occurred: ' + str(e))
    finally:
        mts.close()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    motionsensor_test()
    
    