#!/usr/bin/env python3
"""
light_clapper.py
"""
import RPi.GPIO as GPIO
import time
from camera import Camera
from motionsensorclass import MotionSensorClass
from thinkspeakwriter import ThingSpeakWriter
from constants import L2_M_5A1_WRITE_KEY, GOOD_STATUS
import argparse
import logging

POLL_TIME_SECS = 0.5 


class SecuritySystem:

    def __init__(self, mts=MotionSensorClass(), cam=Camera(), 
                 writer=ThingSpeakWriter(L2_M_5A1_WRITE_KEY)):
        """
        Initializes the attributes
        Parameters
        ----------
        mic : Microphone
            The microphone sensor
        led : Led
            The LED light
        writer : ThingSpeakWriter
            ThinkSpeak channel
        """
        self.__mts = mts
        self.__cam = cam
        self.__writer = writer
        
    def poll(self):
        """
        Poll for motion
        """
        try:
            self.__cam.start_camera()
            while True:
                motionDetected = self.update_status()

                if motionDetected[0]:
                    self.__write_to_channel(motionDetected[1], motionDetected[2])
                    # self.__send_notification(motionDetected[1], motionDetected[2])
                    # self.__upload_video()
                    # self.__email_link()

                # Wait before polling again
                sleep_time = POLL_TIME_SECS if motionDetected[0] else 0
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            print('Exiting')
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
        finally:
            self.__cam.close_camera()
            self.__mts.close_sensor()

    def update_status(self):
        """
        Check motion sensor for detected motion
        and set camera to record
        Returns
        -------
        result : bool, str, str
            True if motion detected, date of motion, time of motion
        """
        result = self.__mts.check_input()
        if(result[0]):
            self.__cam.record_video(result[1], result[2])
        return result[0], result[1], result[2]

    def __write_to_channel(self, date, time):
        """
        Write status of motion to channel
        """
        fields = {'field1': "{} {}".format(date, time)}
        status, reason = self.__writer.write(fields)
        if status != GOOD_STATUS:
            raise Exception('Write was unsuccessful')

    def __send_notification(self, date, time):
        """
        Send notification via SMS to mobile phone
        """
        # fields = {'field1': "{} {}".format(date, time)}
        # status, reason = self.__writer.write_to_channel(fields)
        # if status != GOOD_STATUS:
        #     raise Exception('Write was unsuccessful')

    def __upload_video(self):
        """
        Upload video to Google Drive
        """
        # fields = {'field1': "{} {}".format(date, time)}
        # status, reason = self.__writer.write_to_channel(fields)
        # if status != GOOD_STATUS:
        #     raise Exception('Write was unsuccessful')

    def __email_link(self):
        """
        Email link to gmail of Google Drive access link 
        """
        # fields = {'field1': "{} {}".format(date, time)}
        # status, reason = self.__writer.write_to_channel(fields)
        # if status != GOOD_STATUS:
        #     raise Exception('Write was unsuccessful')


def parse_args():
    """
    Parses arguments for manual testing of LightClapper
    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(description='Run the SecuritySystem program (CTRL-C to exit)')
    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging_level)

    security_system = SecuritySystem()
    security_system.poll()