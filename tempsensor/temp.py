#!/usr/bin/env python3
"""
Purpose - Making sure temperature sensor is working
"""

import RPi.GPIO as GPIO
import logging
import smbus2
import bme280
import time

#ADD IN THE TEMP INPUT LINE

class Temperature():
	def __init__(self, pin = TEMP_INPUT):
#FINISH THE INITIALIZE TEMP

	def check_input(self):
#FINISH TO SEE IF THERE IS INPUT BEING DETECTED
 
def temperature_test():
#FINISH TEST FOR TEMP

if __name__ == "__main__":
	logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s",
		level = logging.DEBUG)
temperature_test()

