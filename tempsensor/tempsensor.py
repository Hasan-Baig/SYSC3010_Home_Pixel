#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from fan import Fan
from temp import Temperature
from thingspeakwriter import ThingSpeakWriter
import thingspeakinfo as c
import argparse
import logging

POLL_TIME_SEC = 5
THRESHOLD = 25
DEFAULT_ID = 0
ID_INCREMENT = 1

class TempSensor:
	temp_sensor_id = DEFAULT_ID

	def __init__(self, location, temp=Temperature(), fan=Fan(), write=True, write_key=c.WRITE_KEY_D1):
		"""
		Initializes the attributes
		"""

		TempSensor.temp_sensor_id += ID_INCREMENT
		self.__node_id = '{node}_{id}'.format(
		    node = c.TEMP_SENSOR_NAME,
		    id = TempSensor.temp_sensor_id)

		self.__location = location
		self.__temp = temp
		self.__fan = fan
		self.__write_mode = write
		self.__writer = ThingSpeakWriter(write_key)

	def poll(self):
		"""
		Poll for temperature readings.
		Update Fan based on temp input.
		Write update to ThingSpeak channel.
		"""

		logging.info('TempSensor Program running')
		logging.info('Writing to channel mode enabled?: {}'.format(self.__write_mode))

		try:
			while True:
				tempDetected = self.update_status()
				self.__write_status_to_channel() #Always writing to channel when temperature is detected

				sleep_time = POLL_TIME_SEC if tempDetected else 0
				time.sleep(sleep_time)

		except KeyboardInterrupt:
			logging.info ("Exiting")
		except BaseException as e:
			logging.error (e.message)
			logging.error ("An error or exception occured!")
		finally:
			self.__fan.cold_status(True) #Set the Fan to OFF when program ends 
			GPIO.cleanup() #Cleanup GPIO

	def update_status(self):
		"""
		Checking for temperature values
		"""

		checkingtemp = self.__temp.read_data() #Reading data from temperature sensor
		logging.info ("Temperature Value: " + str(checkingtemp))

		#Checking to see if the temperature value is greater or less than the set Threshold value
		if checkingtemp > THRESHOLD:
			logging.info ("ROOM TOO HOT - TURNING ON")
			self.__fan.hot_status(True) #If greater, then fan turns ON
		if checkingtemp <= THRESHOLD:
			logging.info ("ROOM TOO COLD - TURNING OFF")
			self.__fan.cold_status(True) #If less, then fan turns OFF
		return checkingtemp

	def checking_status(self):
		"""
		Returning a temperature value
		"""
		checkingtemp = self.__temp.read_data()
		return checkingtemp

	def __write_status_to_channel(self):
		"""
		Write status of TempSensor to channel
		"""

		tval = self.__temp.read_data()
		fan_status = 0
		if self.__fan.get_status() == 1:
			fan_status = 1

		fields = {c.LOCATION_FIELD: self.__location,
			  c.NODE_ID_FIELD: self.__node_id,
			  c.FAN_STATUS_FIELD: fan_status,
			  c.TEMP_VAL_FIELD: tval}

		status, reason = self.__writer.write_to_channel(fields)
		if status != c.GOOD_STATUS:
			logging.error('Write to Thingspeak Channel was unsuccessful')

def parse_args():
	"""
	Parses arguments for manual operation of the TempSensor
	"""

	parser = argparse.ArgumentParser(description = "Run the TempSensor Program (CTRL-C to Exit)")
	parser.add_argument("-w",
			    "--write",
			    default = False,
			    action = "store_true",
			    help = "write data to channel")

	parser.add_argument("-v",
			    "--verbose",
			    default = False,
			    action = "store_true",
			    help = "Print all debug logs")

	parser.add_argument('-l',
			    '--location',
			    type=str,
			    required = True,
			    metavar='<owner_room>',
			    help = 'Specify owner and room')

	args = parser.parse_args()
	return args

if __name__ == "__main__":
	args = parse_args()
	logging_level = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(format=c.LOGGING_FORMAT, level = logging_level)

	temp_sensor = TempSensor(args.location, write=args.write)
	temp_sensor.poll()
