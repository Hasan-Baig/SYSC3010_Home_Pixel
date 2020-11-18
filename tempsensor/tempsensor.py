import RPi.GPIO as GPIO
import time
from fan import Fan
from temp import Temperature
from thingspeakwriter import ThingSpeakWriter
from thingspeakinfo import WRITE_KEY_D1, GOOD_STATUS
import argparse
import logging

POLL_TIME_SEC = 10
THRESHOLD = 25
#THRESHOLD = 10

class TempSensor:
	def __init__(self, temp=Temperature(), fan=Fan(), writer = ThingSpeakWriter(WRITE_KEY_D1)):
		self.__temp = temp
		self.__fan = fan
		self.__writer = writer

	def poll(self):
		try:
			while True:
				tempDetected = self.update_status()
				if tempDetected > THRESHOLD:
					self.__write_to_channel(tempDetected)
				if tempDetected <= THRESHOLD:
					self.__write_to_channel(tempDetected)

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
		if checkingtemp <= THRESHOLD:
			print ("ROOM TOO COLD - TURNING OFF")
			self.__fan.cold_status(True)
		return checkingtemp

	def __write_to_channel(self, tempDetected):
		status = 1 if self.__fan.get_status() else 0
		fields = {"field1": status}
		status, reason = self.__writer.write(fields)
		if status != GOOD_STATUS:
			raise Exception("Write was unsuccesful")

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

	args = parser.parse_args()
	return args

if __name__ == "__main__":
	args = parse_args()
	logging_level = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level = logging_level)

	temp_sensor = TempSensor()
	temp_sensor.poll()
