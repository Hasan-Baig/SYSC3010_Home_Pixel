#!/usr/bin/env python3

"""
Record motion detected by PIR motion sensor
"""

import logging
from gpiozero import MotionSensor
from time import sleep
from datetime import datetime
import constants as c

MOTION_INPUT = 23
MOTION_POLL_TIME_SECS = 3.5
POLLING = True

class MotionSensorClass:
    """
    Class to represent the motion sensor
    Attributes
    ----------
    __mts : MotionSensor
        The MotionSensor
    Methods
    -------
    check_input()
        Checks if motion sensor detects input
    close_sensor()
        Turns off output to sensor
    """
    def __init__(self, mts=MotionSensor(MOTION_INPUT)): 
        """
        Initializes the Motion sensor
        Parameters
        ----------
        mts : MotionSensor
            The MotionSensor class from gpiozero
        """
        self.__mts = mts

    def check_input(self):
        """
        Checks if the motion sensor detects sound
        Returns
        -------
        bool
            True if motion detected
        """
        dateNow = ""
        timeNow = ""
        if self.__mts.wait_for_motion():
            dateNow = datetime.now().strftime("%Y-%m-%d")
            timeNow = datetime.now().strftime("%H:%M:%S")
            logging.debug("Motion Detected at {}".format(timeNow)) 
            return c.MOTION_DETECTED, dateNow, timeNow 
        
        return c.MOTION_NOT_DETECTED, dateNow, timeNow

    #extra
    def motionDetected(self):
        if self.__mts.motion_detected():
            return c.MOTION_DETECTED
        return c.MOTION_NOT_DETECTED

    def close_sensor(self):
        """
        Ignores output to sensor 
        """
        self.__mts.close()

def motionsensor_test():
    """
    Creates a MotionSensorClass object for manual verification
    """
    try:
        mts = MotionSensorClass()
        while POLLING:
            result = mts.check_input()
            if(result[0]):
                # Sleep before checking for motion again
                sleep(MOTION_POLL_TIME_SECS)
    except KeyboardInterrupt:
        logging.info('Exiting')
    except BaseException as e:
        logging.error('An error or exception occurred: ' + str(e))
    finally:
        mts.close_sensor()

if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_DEFAULT_LEVEL)
    motionsensor_test()
    
    