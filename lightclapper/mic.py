#!/usr/bin/env python3
"""
mic.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import RPi.GPIO as GPIO
from time import sleep
import logging
import constants as c

SOUND_INPUT_PIN = 20
MIC_POLL_TIME_SECS = 0.5
GPIO_WARNINGS_OFF = False
POLLING = True


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

    def __init__(self, pin=SOUND_INPUT_PIN):
        """
        Initializes the Microphone sensor

        Parameters
        ----------
        pin : int
            BCM GPIO pin number
        """
        self.__pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(GPIO_WARNINGS_OFF)
        GPIO.setup(self.__pin, GPIO.IN)

    def check_input(self):
        """
        Checks if the microphone sensor detects sound

        Returns
        -------
        sound_detected : bool
            True if sound detected
        """
        sound_detected = False
        if GPIO.input(self.__pin):
            logging.debug("Microphone sensor detects sound")
            sound_detected = True
        return sound_detected


def microphone_test():
    """
    Creates a Microphone object for manual microphone sensor verification
    """
    try:
        mic = Microphone()
        while POLLING:
            if mic.check_input() == c.SOUND_DETECTED:
                sleep(MIC_POLL_TIME_SECS)

    except KeyboardInterrupt:
        logging.info('Exiting due to keyboard interrupt')

    except BaseException:
        logging.error('An error or exception occurred!')

    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_DEFAULT_LEVEL)
    microphone_test()
