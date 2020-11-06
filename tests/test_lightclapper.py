#!/usr/bin/env python3
"""
test_lightclapper.py
"""
import logging
import RPi.GPIO as GPIO
from unittest import TestCase, main
from unittest.mock import patch, call, MagicMock
from lightclapper.lightclapper import LightClapper
from lightclapper.mic import Microphone
from lightclapper.led import Led


class TestLightClapper(TestCase):
    """
    Test methods in LightClapper
    """

    def setUp(self):
        """
        Setup TestLightClapper
        Use mock objects for microphone sensor & light
        """
        self.mic_mock = MagicMock()
        self.led_mock = MagicMock()
        self.led_mock.__led_on = False
        self.light_clapper = LightClapper(mic=self.mic_mock, led=self.led_mock)

    def test_check_and_update_status_true(self):
        """
        Test if microphone sensor detects sound, does
        check_clap_set_light retrun toggle = True
        """
        self.mic_mock.check_input.return_value = True
        self.assertTrue(self.light_clapper.check_and_update_status())

    def test_check_and_update_status_false(self):
        """
        Test if microphone sensor does not detect sound, does
        check_clap_set_light retrun toggle = False
        """
        self.mic_mock.check_input.return_value = False
        self.assertFalse(self.light_clapper.check_and_update_status())


@patch('RPi.GPIO.output', autospec=True)
class TestLed(TestCase):
    """
    Test methods in Led
    """

    def setUp(self):
        """
        Setup TestLed
        Uses patch decorator to replace output calls
        (For testing without HW at pins)
        """
        self.pin = 21
        self.led = Led(pin=self.pin)

    def tearDown(self):
        """
        Teardown TestLed
        """
        self.led.set_status(False)
        GPIO.cleanup()

    def test_invert_light_on_to_off(self, mock_output):
        """
        Test that LED status changes to off if already on
        & that 2 calls were made to RPi.GPIO.output
        """
        self.led.set_status(True)
        status = self.led.invert_status()
        err_msg = 'LED status did not change from on to off'
        self.assertFalse(status, err_msg)

        calls = [call(self.pin, GPIO.HIGH), call(self.pin, GPIO.LOW)]
        mock_output.assert_has_calls(calls)

    def test_invert_light_off_to_on(self, mock_output):
        """
        Test that LED status changes to on if already off
        & that 2 calls were made to RPi.GPIO.output
        """
        self.led.set_status(False)
        status = self.led.invert_status()
        err_msg = 'LED status did not change from off to on'
        self.assertTrue(status, err_msg)

        calls = [call(self.pin, GPIO.LOW), call(self.pin, GPIO.HIGH)]
        mock_output.assert_has_calls(calls)

    def test_set_status_on(self, mock_output):
        """
        Test that LED status changes on
        & that 1 call was made to RPi.GPIO.output
        """
        self.led.set_status(True)
        err_msg = 'LED status is not on'
        self.assertTrue(self.led.get_status(), err_msg)

        calls = [call(self.pin, GPIO.HIGH)]
        mock_output.assert_has_calls(calls)

    def test_set_status_off(self, mock_output):
        """
        Test that LED status changes off
        & that 1 call was made to RPi.GPIO.output
        """
        self.led.set_status(False)
        err_msg = 'LED status is not off'
        self.assertFalse(self.led.get_status(), err_msg)

        calls = [call(self.pin, GPIO.LOW)]
        mock_output.assert_has_calls(calls)


@patch('RPi.GPIO.input', autospec=True)
class TestMicrophone(TestCase):
    """
    Test methods in Microphone
    """

    def setUp(self):
        """
        Setup TestMicrophone
        Uses patch decorator to replace input calls
        (For testing without HW at pins)
        """
        self.pin = 20
        self.mic = Microphone(pin=self.pin)

    def tearDown(self):
        """
        Teardown TestLed
        """
        GPIO.cleanup()

    def test_check_input_detected(self, mock_input):
        """
        Test that check_input returns True if
        sound detected
        """
        mock_input.return_value = True
        err_msg = 'Microphone detected sound not reported'
        self.assertTrue(self.mic.check_input(), err_msg)

    def test_check_input_not_detected(self, mock_input):
        """
        Test that check_input returns False if
        sound not detected
        """
        mock_input.return_value = False
        err_msg = 'Microphone reported sound not detected'
        self.assertFalse(self.mic.check_input(), err_msg)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    main()
