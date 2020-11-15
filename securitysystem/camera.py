#!/usr/bin/env python3

"""
Purpose:
Performs actions on camera module (actuator)
"""

import logging
from picamera import PiCamera
from time import sleep
from datetime import datetime

CAMERA_RECORD_TIME_SECS = 10

class Camera:

    def __init__(self, camera=PiCamera()):
        self.__camera = camera

    def start_camera(self):
        self.__camera.start_preview() 
        self.__camera.rotation = 180

    def record_video(self, date, time):
        self.__camera.start_recording('/home/pi/Desktop/Security_Cam/{}_{}.h264'.format(date, time))
        sleep(CAMERA_RECORD_TIME_SECS)
        self.__camera.stop_recording()

    def close_camera(self):
        self.__camera.stop_preview()  

def camera_test():
    camera_test = Camera()
    camera_test.start_camera()
    date = datetime.today().strftime("%Y-%m-%d")
    time = datetime.today().strftime("%H:%M:%S")
    camera_test.record_video(date, time)
    camera_test.close_camera()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    camera_test()
    
    