#!/usr/bin/env python3
"""
Purpose - Performs actions for the fan module
"""

import RPi.GPIO as GPIO
from time import sleep
import logging

FAN_PIN = 23
FAN_TIME = 10

class Fan:
	def __init__(self, pin = FAN_PIN):
		self.__pin = pin
		self.__fan_on = False
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.__pin, GPIO.OUT)

	def get_status(self):
		return self.__fan_on

	def set_status(self, status):
		output_gpio = GPIO.HIGH if status else GPIO.LOW
		GPIO.output(self.__pin, output_gpio)

		output_string = "ON" if status else "OFF"
		logging.debug("FAN: {}".format(output_string))

		self.__fan_on = status

def fan_test():
	fan = Fan()
	fan.set_status(True)
	sleep(FAN_TIME)
	fan.set_status(False)
	GPIO.cleanup()

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s = %(message)s",
		 level = logging.DEBUG)
	fan_test()

