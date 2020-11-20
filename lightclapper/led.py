#!/usr/bin/env python3
"""
led.py

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

LED_OUTPUT_PIN = 21
LED_TEST_TIME_SECS = 0.5
GPIO_WARNINGS_OFF = False
ON_STRING = 'ON'
OFF_STRING = 'OFF'


class Led:
    """
    Class to represent Led actuator

    Attributes
    ----------
    __pin : int
        BCM GPIO pin number
    __led_on : bool
        True if LED on

    Methods
    -------
    get_led_status()
        Returns the status of LED
    set_led_status(status)
        Sets the LED status
    invert_status()
        Inverts the status of the LED
    """

    def __init__(self, pin=LED_OUTPUT_PIN):
        """
        Initializes the Led

        Parameters
        ----------
        pin : int
            BCM GPIO pin number
        """
        self.__pin = pin
        self.__led_on = c.LED_OFF
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(GPIO_WARNINGS_OFF)
        GPIO.setup(self.__pin, GPIO.OUT)

    def get_status(self):
        """
        Returns
        -------
        self.__led_on : bool
            True if LED on
        """
        return self.__led_on

    def set_status(self, status):
        """
        Sets the LED status

        Parameters
        ----------
        status : bool
            True if LED on, False if LED off
        """
        output_gpio = None
        output_string = ''

        if status == c.LED_ON:
            output_gpio = GPIO.HIGH
            output_string = ON_STRING
        else:
            output_gpio = GPIO.LOW
            output_string = OFF_STRING

        GPIO.output(self.__pin, output_gpio)
        self.__led_on = status
        logging.debug('LED status updated to {}'.format(output_string))

    def invert_status(self):
        """
        Inverts the LED status
         - If LED status on, turn off LED
         - If LED status off, turn on LED

        Returns
        -------
        self.__led_on : bool
            True if LED on
        """
        self.set_status(not self.__led_on)
        return self.__led_on


def led_test():
    """
    Creates an Led object for manual LED verification
    """
    led = Led()

    led.set_status(c.LED_ON)
    sleep(LED_TEST_TIME_SECS)
    led.set_status(c.LED_OFF)

    GPIO.cleanup()


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_DEFAULT_LEVEL)
    led_test()
