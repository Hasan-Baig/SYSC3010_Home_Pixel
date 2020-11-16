#!/usr/bin/env python3
"""
Purpose - Performs actions for the fan module
"""
import logging
import RPi.GPIO as GPIO
from time import sleep

FAN_PIN = 23
FAN_TEST_TIME = 5

class Fan:
	def __init__(self, pin=FAN_PIN):
		self.__pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.__pin, GPIO.OUT)

	def get_status(self):
		return self.__fan_on

	def hot_status(self, status):
		output_gpio = GPIO.HIGH
		GPIO.output(self.__pin, output_gpio)

		output_string = "ROOM TOO HOT - ON"
		logging.debug("FAN: {}".format(output_string))
		self.__fan_on = status

	def room_status(self, status):
		output_gpio = GPIO.LOW
		GPIO.output(self.__pin, output_gpio)

		output_string = "ROOM @ GOOD TEMP - OFF"
		logging.debug("FAN: {}".format(output_string))
		self.__fan_on = status

	def cold_status(self, status):
		output_gpio = GPIO.LOW
		GPIO.output(self.__pin, output_gpio)

		output_string = "ROOM TOO COLD - OFF"
		logging.debug("FAN: {}".format(output_string))
		status = 0
		self.__fan_on = status

def fan_test():
	fanTest = Fan()
	fanTest.hot_status(True)
	sleep(FAN_TEST_TIME)
	fanTest.cold_status(True)
	sleep(FAN_TEST_TIME)
	fanTest.hot_status(True)
	sleep(FAN_TEST_TIME)
	fanTest.room_status(True)

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s = %(message)s",
		 level = logging.DEBUG)
	fan_test()

