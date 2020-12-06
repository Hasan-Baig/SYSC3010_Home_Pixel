#!/usr/bin/env python3

import logging
import RPi.GPIO as GPIO
from unittest import TestCase, main
from unittest.mock import patch, call, MagicMock
from tempsensor.tempsensor import TempSensor
from tempsensor.fan import Fan
from tempsensor.temp import Temperature
import thingspeakinfo as c

class TestTempSensor(TestCase):
	def setUp(self):
		self.__temp_mock = MagicMock()
		fan_mock = MagicMock()
		fan_mock.__fan_on = False
		test_location = 'test_location'
		self.__temp_sensor = TempSensor(test_location, temp = self.__temp_mock, fan = fan_mock)

	def test_checking_status_true(self):
		"""
		Testing to see if the TempSensor node is functioning properly
		"""
		self.__temp_mock.read_data.return_value = True
		self.assertTrue(self.__temp_sensor.checking_status())

	def test_checking_status_false(self):
		"""
		Testing to see if the TempSensor node does not function properly
		"""
		self.__temp_mock.read_data.return_value = False
		self.assertFalse(self.__temp_sensor.checking_status())

@patch("RPi.GPIO.output", autospec = True)
class TestFan(TestCase):
	def setUp(self):
		self.pin = 23
		self.fan = Fan(pin=self.pin)

	def tearDown(self):
		self.fan.room_status(True)
		GPIO.cleanup()

	def test_hot_status(self, mock_output):
		"""
		TESTING FAN TURNING OFF TO ON
		"""
		self.fan.room_status(True)
		status = self.fan.hot_status(True)
		err_msg = "FAN status did not change from off to on"
		self.assertFalse(status, err_msg)

		calls = [call(self.pin, GPIO.LOW), call(self.pin, GPIO.HIGH)]
		mock_output.assert_has_calls(calls)

	def test_cold_status(self, mock_output):
		"""
		TESTING FAN TURNING ON TO OFF
		"""
		self.fan.hot_status(True)
		status = self.fan.cold_status(True)
		err_msg = "FAN status did not change from on to off"
		self.assertFalse(status, err_msg)

		calls = [call(self.pin, GPIO.HIGH), call(self.pin, GPIO.LOW)]
		mock_output.assert_has_calls(calls)

@patch("RPi.GPIO.output", autospec = True)
class TestTemperature(TestCase):
	def setUp(self):
		self.temp = Temperature()

	def tearDown(self):
		GPIO.cleanup()

	def test_check_input_detected(self, mock_input):
		"""
		Testing Input Detected
		"""
		mock_input.return_value = True
		err_msg = "Temp Sensor did not detect any temperature"
		self.assertTrue(self.temp.read_data(), err_msg)

	def test_check_input_not_detected(self, mock_input):
		"""
		Testing input NOT detected
		"""
		mock_input.return_value = False
		err_msg = "Temp Sensor detected temperature"
		self.assertTrue(self.temp.read_data(), err_msg)

if __name__ == '__main__':
	logging.basicConfig(format=c.LOGGING_FORMAT, level = c.LOGGING_TEST_LEVEL)
	main()



