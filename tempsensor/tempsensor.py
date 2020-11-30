#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from fan import Fan
from temp import Temperature
from thingspeakwriter import ThingSpeakWriter
import thingspeakinfo as c
import argparse
import logging

POLL_TIME_SEC = 10
THRESHOLD = 25
DEFAULT_ID = 0
ID_INCREMENT = 1


class TempSensor:
	temp_sensor_id = DEFAULT_ID
	def __init__(self, location, temp=Temperature(), fan=Fan(), write=False, write_key=ThingSpeakWriter(c.WRITE_KEY_D1)):
		TempSensor.temp_sensor_id += ID_INCREMENT
		self.__node_id = '{node}_{id}'.format(
		    node = c.TEMP_SENSOR_NAME,
		    id = TempSensor.temp_sensor_id)

		self.__location = location
#		self.__tval = tval
		self.__temp = temp
		self.__fan = fan
		self.__write_mode = write
		self.__writer = ThingSpeakWriter(write_key) if write else None

	def poll(self):
		try:
			while True:
				tempDetected = self.update_status()

#				if tempDetected > THRESHOLD:
#					self.__write_to_channel(tempDetected, tval)
#					self.__write_to_channel(tval)
#				if tempDetected <= THRESHOLD:
#					self.__write_to_channel(tempDetected, tval)
#					self.__write_to_channel(tval)


				if tempDetected > THRESHOLD:
					if self.__write_mode:
						self.__write_status_to_channel()
				if tempDetected < THRESHOLD:
					if self.__write_mode:
						self.__write_status_to_channel()
				sleep_time = POLL_TIME_SEC if tempDetected else 0
				time.sleep(sleep_time)
		except KeyboardInterrupt:
			print ("Exiting")
		except BaseException as e:
			print (e.message)
			print ("An error or exception occured!")
		finally:
			self.__fan.cold_status(True)
			GPIO.cleanup()

	def update_status(self):
		checkingtemp = self.__temp.read_data()
		print ("Temperature Value: " + str(checkingtemp))
		if checkingtemp > THRESHOLD:
			print ("ROOM TOO HOT - TURNING ON")
			self.__fan.hot_status(True)
#			self.__write_to_channel(checkingtemp)
		if checkingtemp <= THRESHOLD:
			print ("ROOM TOO COLD - TURNING OFF")
			self.__fan.cold_status(True)
#			self.__write_to_channel(checkingtemp)
		return checkingtemp

	def checking_status(self):
		checkingtemp = self.__temp.read_data()
		return checkingtemp

	def __write_status_to_channel(self):
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
