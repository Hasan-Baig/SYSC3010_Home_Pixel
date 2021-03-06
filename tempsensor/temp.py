#!/usr/bin/env python3
import RPi.GPIO as GPIO
import logging
import smbus2
import bme280
from time import sleep
from datetime import datetime

class Temperature:
	def __init__(self, poll_time = 1):
		self._bus = smbus2.SMBus(1)
		self._address = 0x77 #Checking to see if the temperature sensor is properly communicating with the RPi
		self._calibration_params = bme280.load_calibration_params(self._bus,self._address) #Calibrating the bme280 temperature sensor
		self._temp_poll_time = poll_time #Polling for the given time
		self._data = dict()

	def read_data(self):
		self._data = bme280.sample(self._bus, self._address, self._calibration_params) #Taking in a single temperature reading
		return self._data.temperature #Returning the reading

def temperature_test():
	sensor = Temperature()
	while True:
		logging.info("Reading Sensor")
		logging.info("Temperature Read: " + str(sensor.read_data()))
		sleep(sensor._temp_poll_time)

if __name__ == "__main__":
	logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s", level = logging.DEBUG)
	temperature_test()
