#!/usr/bin/env python3
"""
test_thingspeak.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import random
import logging
import time
from unittest import TestCase, main
from thingspeakwriter import ThingSpeakWriter
from thingspeakreader import ThingSpeakReader
import constants as c

SLEEP_TIME_SECS = 1
LAST_INDEX = -1


class TestThingSpeak(TestCase):
    """
    Test methods in ThingSpeakWriter & ThingSpeakReader

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
        Sleep to allow time for ThingSpeak writes
        """
        self.__writer = ThingSpeakWriter(c.L2_M_5C2_WRITE_KEY)
        self.__reader = ThingSpeakReader(key=c.L2_M_5C2_READ_KEY,
                                         feed=c.L2_M_5C2_FEED)
        time.sleep(SLEEP_TIME_SECS)

    def test_write_to_valid_channel(self):
        """
        Write to valid channel
        """
        test_fields = {c.TEST_FIELD: 'abc123'}
        expected_reason = 'OK'
        err_msg = 'Status of write was unexpected!'

        status, reason = self.__writer.write_to_channel(test_fields)
        self.assertEqual(status, c.GOOD_STATUS, err_msg)
        self.assertEqual(reason, expected_reason, err_msg)

    def test_write_to_invalid_channel(self):
        """
        Write to invalid channel
        """
        bad_writer = ThingSpeakWriter(key='')
        test_fields = {c.TEST_FIELD: 'abc123'}
        expected_status = 400
        expected_reason = 'Bad Request'
        err_msg = ''

        status, reason = bad_writer.write_to_channel(test_fields)
        err_msg = 'Status of write was unexpected!'
        self.assertEqual(status, expected_status, err_msg)
        err_msg = 'Reason of request response was unexpected!'
        self.assertEqual(reason, expected_reason, err_msg)

    def test_write_and_read(self):
        """
        Read from channel
        """
        random_min = 1
        random_max = 10000000
        expected_field = str(random.randint(random_min, random_max))
        err_msg = ''
        test_fields = {c.TEST_FIELD: expected_field}

        status, reason = self.__writer.write_to_channel(test_fields)
        err_msg = 'Status of write was unexpected!'
        self.assertEqual(status, c.GOOD_STATUS, err_msg)

        actual_fields = self.__reader.read_from_channel()
        actual = actual_fields['feeds'][LAST_INDEX][c.TEST_FIELD]
        err_msg = 'Field read back does not match expected field!'
        self.assertEqual(actual, expected_field, err_msg)


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()
