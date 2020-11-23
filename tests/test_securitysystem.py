#!/usr/bin/env python3
"""
SecuritySystem Tests
"""
import logging
import time
import unittest
unittest.TestLoader.sortTestMethodsUsing = None
from unittest import TestCase, main
from unittest.mock import patch, call, MagicMock
from securitysystem.securitysystem import SecuritySystem
from camera import Camera
from motionsensorclass import MotionSensorClass
import pathlib
from datetime import datetime
import securitysystem.constants as c

class TestMotionSensor(TestCase):
    """
    Test methods in MotionSensorClass
    Attributes
    ----------
    __mts : MotionSensorClass
    Methods
    -------
    setUp()
    tearDown()
    test_check_input_detected(mock_input)
    test_check_input_not_detected(mock_input)
    """

    def setUp(self):
        """
        Setup TestMotionSensor
        """
        self.__test_pin = 23
        self.__mts = MotionSensorClass(self.__test_pin)

    @patch('motionsensorclass.MotionSensorClass.check_input')
    def test1_check_input_detected(self, mock_input):
        """
        Test that check_input returns True if motion detected
        Parameters
        ----------
        mock_input : unittest.mock.Mock
            Mock patched RPi.GPIO.input module
        """
        mock_input.return_value = c.MOTION_DETECTED
        err_msg = 'Sensor detected motion not reported'
        self.assertTrue(self.__mic.check_input(), err_msg)

    @patch('motionsensorclass.MotionSensorClass.check_input')
    def test2_check_input_not_detected(self, mock_input):
        """
        Test that check_input returns False if motion not detected
        Parameters
        ----------
        mock_input : unittest.mock.Mock
            Mock patched RPi.GPIO.input module
        """
        mock_input.return_value = c.MOTION_NOT_DETECTED
        err_msg = 'Sensor reported motion not detected'
        self.assertFalse(self.__mic.check_input(), err_msg)


class TestCamera(TestCase):
    """
    Test methods in Camera
    Attributes
    ----------
    __cam : Camera
    Methods
    -------
    setUp()
    tearDown()
    test_record_video()
    """

    def setUp(self):
        """
        Setup TestCamera
        """
        self.__cam = Camera()
        self.__cam.start_camera()

    def tearDown(self):
        """
        Teardown TestCamera
        """
        self.__cam.close_camera()

    def test3_record_video(self):
        """
        Test that Camera records a video with a given date and time
        & video is stored on RPI desktop under "Security_Cam" folder
        """
        date = "test"
        time = "video"

        self.__cam.record_video(date, time)

        file = pathlib.Path("/home/pi/Desktop/Security_Cam/{}_{}.h264".format(date, time))
        err_msg = 'Video not recorded or stored'
        self.assertTrue(file.exists(), err_msg)

class TestSecuritySystem(TestCase):
    """
    Test methods of SecuritySystem
    Attributes
    ----------
    __mts_mock : MagicMock
    __security_system : SecuritySystem
    Methods
    -------
    setUp()
    test_update_status_on()
    test_update_status_off()
    test_send_notification()
    test_upload_video()
    test_email_link()
    """
    def setUp(self):
        """
        Setup SecuritySystem 
        """
        test_location = 'test_location'

        self.__mts_mock = MagicMock()
        self.__cam_mock = MagicMock()
        self.__security_system_mock = SecuritySystem(test_location, mts=self.__mts_mock, cam=self.__cam_mock)

        self.__cam = Camera()
        self.__test_pin = 23
        self.__mts = MotionSensorClass(self.__test_pin)
        self.__security_system = SecuritySystem(test_location, mts=self.__mts, cam=self.__cam)
        self.__link = None

    @patch('securitysystem.SecuritySystem.update_status')
    def test4_update_status_on(self):
        """
        Test if motion sensor detects motion, return = True
        """
        self.__mts_mock.check_input.return_value = c.MOTION_DETECTED
        err_msg = 'Motion detected'
        self.assertTrue(self.__security_system.update_status(),
            err_msg)
            
    # @patch('securitysystem.SecuritySystem.update_status')
    def test5_update_status_off(self):
        """
        Test if microphone sensor detects sound, return = False
        """
        self.__mts_mock.check_input.return_value = c.MOTION_NOT_DETECTED
        err_msg = 'Motion not detected'
        self.assertFalse(self.__security_system.update_status(),
            err_msg)

    def test6_convert_to_mp4(self):
        """
        Test if video is converted to mp4 file
        """
        date = "test"
        time = "video"
        self.__security_system.__convert_to_mp4(date, time)
        
        file = pathlib.Path("/home/pi/Desktop/Security_Cam/{}_{}.mp4".format(date, time))
        err_msg = 'Video not converted'
        self.assertTrue(file.exists(), err_msg)

    def test7_send_notification(self):
        """
        Test if notification is sent to phone via SMS
        """
        date = "test"
        time = "video"
        SMS = self.__security_system.__send_notification(date, time)
        err_msg = 'Video not uploaded'
        self.assertTrue(SMS, err_msg)

    def test8_upload_video(self):
        """
        Test if video can be uploaded
        """
        date = "test"
        time = "video"
        upl = self.__security_system.__upload_video(date, time)
        err_msg = 'Video not uploaded'
        self.assertTrue(upl, err_msg)

    def test9_email_link(self):
        """
        Test if email can be sent
        """
        date = "test"
        time = "video"
        sent = self.__security_system.__email_link(date, time, self.__link)
        err_msg = 'Email not Sent'
        self.assertTrue(sent, err_msg)

if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()