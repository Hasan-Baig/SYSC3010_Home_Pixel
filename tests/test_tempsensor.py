# tempsensor unit tests
import logging
import RPi.GPIO as GPIO
from unittest import TestCase, main
from unittest.mock import patch, call, MagicMock
from tempsensor.tempsensor import TempSensor
from tempsensor.fan import Fan
from tempsensor.temp import Temperature
THRESHOLD = 20

class TestTempSensor(TestCase):
	def setUp(self):
		self.fan_mock = MagicMock()
		self.temp_mock = MagicMock()
		self.fan_mock.__fan_on = False
		self.temp_sensor = TempSensor(temp = self.fan_mock, fan = self.fan_mock)

	def test_check_and_update_status_true(self):
		self.temp_mock.check_input.return_value = True
		self.assertTrue(self.temp_sensor.check_and_update_status())

	def test_check_and_update_status_false(self):
		self.temp_mock.check_input.return_value = False
		self.assertFalse(self.temp_sensor.check_and_update_status())

@patch("RPi.GPIO.output", autospec = True)
class TestFan(TestCase):
	def SetUp(self):
		self.pin = 23
		self.fan = Fan(pin=self.pin)

	def tearDown(self):
		self.fan.set_status(False)
		GPIO.cleanup()

	def test_hot_status(self, mock_output):
		if tempval > THRESHOLD:
			self.fan.set_status(True)
			status = self.fan.hot_status()
		error_msg = "Fan did not change from off to on"
		self.assertTrue(self.fan.get_status(), error_msg)

		calls = [call(self.pin, GPIO.HIGH), call(self.pin, GPIO.LOW)]
		mock_output.assert_has_calls(calls)

	def test_cold_status(self, mock_output):
		if tempval < THRESHOLD:
			self.fan.set_status(True)
			status = self.fan.cold_status()
		error_msg = "Fan did not change from on to off"
		self.assertFalse(self.fan.get_status(), error_msg)

		calls = [call(self.pin, GPIO.LOW), call(self.pin, GPIO.HIGH)]
		mock_output.assert_has_calls(calls)

@patch("RPi.GPIO.input", autospec = True)
class TestTemperature(TestCase):
	def setUp(self):
		self.pin = 3
		self.temp = Temperature(pin = self.pin)

	def tearDown(self):
		GPIO.cleanup()

	def test_check_input_detected(self, mock_input):
		mock_input.return_value = True
		error_msg = "Temperature detected temp, not reported"
		self.assertTrue(self.temp.check_input(), error_msg)

	def test_check_input_not_detected(self, mock_input):
		mock_input.return_value = False
		error_msg = "Temperature reported temp, not detected"
		self.assertFalse(self.temp.check_input(), error_msg)

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level = logging.INFO)
	main()



