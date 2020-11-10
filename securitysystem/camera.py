#!/usr/bin/env python3

"""
Purpose:
Performs actions on camera module (actuator)
"""

import logging
from picamera import PiCamera as camera
from time import sleep

CAMERA_RECORD_TIME_SECS = 10

class Camera:

    def __init__(self): 
        camera = PiCamera()

    def start_camera(self):
        camera.start_preview()  

    def record_video(self, name):
        camera.start_recording('/home/pi/Desktop/Security_Cam/%s.h264' % name)
        sleep(CAMERA_RECORD_TIME_SECS)
        camera.stop_recording()

    def close_camera(self):
        camera.stop_preview()  

def camera_test():
    cam = Camera()
    camera.start_preview()  
    camera.start_recording('/home/pi/Desktop/Security_Cam/test/test_vid.h264')
    sleep(CAMERA_RECORD_TIME_SECS)
    camera.stop_recording()
    camera.stop_preview()  

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    camera_test()
    
    