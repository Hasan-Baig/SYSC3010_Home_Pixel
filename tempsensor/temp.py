#!/usr/bin/env python3
"""
Purpose - Making sure temperature sensor is working
"""

import RPi.GPIO as GPIO
import logging
import smbus2
import bme280
from time import sleep
from datetime import datetime

address = 0x77
bus = smbus2.SMBus(1)

calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)

TEMP_PIN = 3
TEMP_POLL_TIME = 1

class Temperature:
	def __init__(self, pin = TEMP_PIN):
		self.__pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.__pin, GPIO.IN)

	def check_input(self):
		tempval = 0
		if GPIO.input(self.__pin):
			logging.debug("Temp Detected")
			tempval = data.temperature
		return tempval

def temperature_test():
	try:
		sensor = Temperature()
		while True:
			if sensor.check_input():
				sleep(TEMP_POLL_TIME)
	except KeyboardInterrupt:
		logging.info("Exiting")
	except BaseException:
		logging.error("An error or exception occured")
	finally:
		GPIO.cleanup()

if __name__ == "__main__":
	logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s",
		level = logging.DEBUG)
#temperature_test()

