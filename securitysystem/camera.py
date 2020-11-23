#!/usr/bin/env python3

"""
Performs actions on camera module (actuator)
"""

import logging
from picamera import PiCamera
from time import sleep
from datetime import datetime
import constants as c

CAMERA_RECORD_TIME_SECS = 10

class Camera:
    """
    Class to represent Camera actuator
    Attributes
    ----------
    __camera : Camera
        The camera
    Methods
    -------
    start_camera()
        Starts preview of camera
    record_video(date, time)
        Records video
    close_camera()
        Stops preview of camera
    """
    def __init__(self, camera=PiCamera()):
        """
        Initializes the Camera
        Parameters
        ----------
        camera : PiCamera()
            The picamera class
        """
        self.__camera = camera

    def start_camera(self):
        """
        Starts preview of camera 
        Rotates camera 180 degrees
        """
        self.__camera.start_preview() 
        self.__camera.rotation = 180

    def record_video(self, date, time):
        """
        Records a video for 10s
        Parameters
        ----------
        date : str
            Date of motion detected
        time : str
            Time of motion detected
        """
        logging.info('Start Recording')
        self.__camera.start_recording('/home/pi/Desktop/Security_Cam/{}_{}.h264'.format(date, time))
        sleep(CAMERA_RECORD_TIME_SECS)
        self.__camera.stop_recording()
        logging.info('Stop Recording')


    def close_camera(self):
        """
        Stops preview of camera 
        """
        logging.info('Close Camera Preview')
        self.__camera.stop_preview()  

def camera_test():
    """
    Creates an Camera object for manual verification
    """
    camera_test = Camera()

    camera_test.start_camera()
    date = datetime.today().strftime("%Y-%m-%d")
    time = datetime.today().strftime("%H:%M:%S")
    camera_test.record_video(date, time)
    camera_test.close_camera()

if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_DEFAULT_LEVEL)
    camera_test()
    
    