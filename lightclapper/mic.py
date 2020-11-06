#!/usr/bin/env python3
"""
mic.py
"""
import RPi.GPIO as GPIO
from time import sleep
import logging

SOUND_INPUT = 20
MIC_POLL_TIME_SECS = 0.5


class Microphone:
    """
    Class to represent the microphone sensor

    Attributes
    ----------
    __pin : int
        BCM GPIO pin number

    Methods
    -------
    check_input()
        Checks if microphone sensor detects input
    """

    def __init__(self, pin=SOUND_INPUT):
        """
        Initializes the Microphone sensor

        Parameters
        ----------
        pin : int
            BCM GPIO pin number
        """
        self.__pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__pin, GPIO.IN)

    def check_input(self):
        """
        Checks if the microphone sensor detects sound

        Returns
        -------
        sound : bool
            True if sound detected
        """
        sound = False
        if GPIO.input(self.__pin):
            logging.debug("Sound detected!")
            sound = True
        return sound


def microphone_test():
    """
    Creates a Microphone object for manual microphone sensor verification
    """
    try:
        mic = Microphone()
        while True:
            if mic.check_input():
                sleep(MIC_POLL_TIME_SECS)
    except KeyboardInterrupt:
        logging.info('Exiting')
    except BaseException:
        logging.error('An error or exception occurred!')
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    microphone_test()
