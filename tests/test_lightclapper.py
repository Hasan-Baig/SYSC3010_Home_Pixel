#!/usr/bin/env python3
"""
test_lightclapper.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import logging
import RPi.GPIO as GPIO
from unittest import TestCase, main
from unittest.mock import patch, call, MagicMock
from lightclapper.lightclapper import LightClapper
from lightclapper.mic import Microphone
from lightclapper.led import Led
import constants as c


@patch('RPi.GPIO.output', autospec=True)
class TestLed(TestCase):
    """
    Test methods in Led

    Attributes
    ----------
    __pin : int
    __led : Led

    Methods
    -------
    setUp()
    tearDown()
    test_invert_light_on_to_off(mock_output)
    test_invert_light_off_to_on(mock_output)
    """

    def setUp(self):
        """
        Setup TestLed
        """
        self.__pin = 21
        self.__led = Led(pin=self.__pin)

    def tearDown(self):
        """
        Teardown TestLed
        """
        self.__led.set_status(c.LED_OFF)
        GPIO.cleanup()

    def test_invert_light_on_to_off(self, mock_output):
        """
        Test that LED status changes to off if already on
        & that 2 calls were made to RPi.GPIO.output

        Parameters
        ----------
        mock_output : unittest.mock.Mock
            Mock patched RPi.GPIO.output module
        """
        self.__led.set_status(c.LED_ON)
        err_msg = 'LED status is not on'
        self.assertTrue(self.__led.get_status(), err_msg)

        status = self.__led.invert_status()
        err_msg = 'LED status did not change from on to off'
        self.assertFalse(status, err_msg)

        calls = [call(self.__pin, GPIO.HIGH), call(self.__pin, GPIO.LOW)]
        mock_output.assert_has_calls(calls)

    def test_invert_light_off_to_on(self, mock_output):
        """
        Test that LED status changes to on if already off
        & that 2 calls were made to RPi.GPIO.output

        Parameters
        ----------
        mock_output : unittest.mock.Mock
            Mock patched RPi.GPIO.output module
        """
        self.__led.set_status(c.LED_OFF)
        err_msg = 'LED status is not off'
        self.assertFalse(self.__led.get_status(), err_msg)

        status = self.__led.invert_status()
        err_msg = 'LED status did not change from off to on'
        self.assertTrue(status, err_msg)

        calls = [call(self.__pin, GPIO.LOW), call(self.__pin, GPIO.HIGH)]
        mock_output.assert_has_calls(calls)


@patch('RPi.GPIO.input', autospec=True)
class TestMicrophone(TestCase):
    """
    Test methods in Microphone

    Attributes
    ----------
    __mic : Microphone

    Methods
    -------
    setUp()
    tearDown()
    test_check_input_detected(mock_input)
    test_check_input_not_detected(mock_input)
    """

    def setUp(self):
        """
        Setup TestMicrophone
        """
        test_pin = 20
        self.__mic = Microphone(test_pin)

    def tearDown(self):
        """
        Teardown TestLed
        """
        GPIO.cleanup()

    def test_check_input_detected(self, mock_input):
        """
        Test that check_input returns True if
        sound detected

        Parameters
        ----------
        mock_input : unittest.mock.Mock
            Mock patched RPi.GPIO.input module
        """
        mock_input.return_value = c.SOUND_DETECTED
        err_msg = 'Microphone detected sound not reported'
        self.assertTrue(self.__mic.check_input(), err_msg)

    def test_check_input_not_detected(self, mock_input):
        """
        Test that check_input returns False if
        sound not detected

        Parameters
        ----------
        mock_input : unittest.mock.Mock
            Mock patched RPi.GPIO.input module
        """
        mock_input.return_value = c.SOUND_NOT_DETECTED
        err_msg = 'Microphone reported sound not detected'
        self.assertFalse(self.__mic.check_input(), err_msg)


class TestLightClapper(TestCase):
    """
    Test methods in LightClapper

    Attributes
    ----------
    __mic_mock : MagicMock
    __light_clapper : LightClapper

    Methods
    -------
    setUp()
    test_check_and_update_status_toggled()
    test_check_and_update_status_not_toggled()
    """

    def setUp(self):
        """
        Setup TestLightClapper
        Use mock objects for microphone sensor & light
        """
        self.__mic_mock = MagicMock()
        led_mock = MagicMock()
        led_mock.__led_on = c.LED_OFF
        test_location = 'test_location'
        self.__light_clapper = LightClapper(test_location,
                                            mic=self.__mic_mock, led=led_mock)

    def test_check_and_update_status_toggled(self):
        """
        Test if microphone sensor detects sound, does
        check_clap_set_light return toggled = True
        """
        self.__mic_mock.check_input.return_value = c.SOUND_DETECTED
        err_msg = 'LED not toggled but sound detected'
        self.assertTrue(
            self.__light_clapper.check_and_update_status(),
            err_msg)

    def test_check_and_update_status_not_toggled(self):
        """
        Test if microphone sensor does not detect sound, does
        check_clap_set_light return toggled = False
        """
        self.__mic_mock.check_input.return_value = c.SOUND_NOT_DETECTED
        err_msg = 'LED to be toggled but no sound detected'
        self.assertFalse(
            self.__light_clapper.check_and_update_status(),
            err_msg)


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()
