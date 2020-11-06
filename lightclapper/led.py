#!/usr/bin/env python3
"""
led.py
"""
import RPi.GPIO as GPIO
from time import sleep
import logging

LED_OUTPUT = 21
LED_TEST_TIME_SECS = 0.5


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
    set_led_status()
        Sets the LED status
    invert_status()
        Inverts the status of the LED
    """

    def __init__(self, pin=LED_OUTPUT):
        """
        Initializes the Led

        Parameters
        ----------
        pin : int
            BCM GPIO pin number
        """
        self.__pin = pin
        self.__led_on = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
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
        output_gpio = GPIO.HIGH if status else GPIO.LOW
        GPIO.output(self.__pin, output_gpio)

        output_string = 'ON' if status else 'OFF'
        logging.debug('LED: {}'.format(output_string))

        self.__led_on = status

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
    led.set_status(True)
    sleep(LED_TEST_TIME_SECS)
    led.set_status(False)
    GPIO.cleanup()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    led_test()
