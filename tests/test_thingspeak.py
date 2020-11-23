#!/usr/bin/env python3
"""
ThingSpeak tests
"""
from __future__ import absolute_import

import random
import logging
import time
from datetime import datetime
from unittest import TestCase, main
from thingspeakwriter import ThingSpeakWriter
from thingspeakreader import ThingSpeakReader
import constants as c

SLEEP_TIME_SECS = 1
LAST_INDEX = -1


class TestThingSpeak(TestCase):
    """
    Test methods for ThingSpeakWriter and ThingSpeakReader
    Attributes
    ----------
    __writer : ThingSpeakWriter
    __reader : ThingSpeakReader
    Methods
    -------
    setUp()
    test_write_to_valid_channel()
    test_write_to_invalid_channel()
    test_write_and_read()
    """

    def setUp(self):
        """
        Setup test method
        """
        self.__writer = ThingSpeakWriter(c.L2_M_5A2_WRITE_KEY)
        self.__reader = ThingSpeakReader(key=c.L2_M_5A2_READ_KEY,
                                         feed=c.L2_M_5A2_FEED)
        time.sleep(SLEEP_TIME_SECS)

    def test_write_to_valid_channel(self):
        """
        Write to valid channel
        """
        test_data = datetime.now()
        test_fields = {c.TEST_FIELD: test_data}
        expected_reason = 'OK'
        err_msg = 'Status of write was unexpected!'

        status, reason = self.__writer.write(test_fields)
        self.assertEqual(status, c.GOOD_STATUS, err_msg)
        self.assertEqual(reason, expected_reason, err_msg)

    def test_write_to_invalid_channel(self):
        """
        Write to invalid channel
        """
        invalid_writer = ThingSpeakWriter(key='')
        test_data = datetime.now()
        test_fields = {c.TEST_FIELD: test_data}
        expected_status = 400
        expected_reason = 'Bad Request'
        err_msg = ''

        status, reason = invalid_writer.write(test_fields)
        err_msg = 'Status of write was unexpected!'
        self.assertEqual(status, expected_status, err_msg)
        err_msg = 'Reason of request response was unexpected!'
        self.assertEqual(reason, expected_reason, err_msg)

    def test_write_and_read(self):
        """
        Write and Read from channel
        """
        test_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_fields = {c.TEST_FIELD: test_data}

        err_msg = ''

        status, reason = self.__writer.write(test_fields)
        err_msg = 'Status of write was unexpected!'
        self.assertEqual(status, c.GOOD_STATUS, err_msg)

        actual_fields = self.__reader.read_from_channel()
        actual = actual_fields['feeds'][LAST_INDEX][c.TEST_FIELD]
        err_msg = 'Field read back does not match test_data!'
        self.assertEqual(actual, test_data, err_msg)


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()