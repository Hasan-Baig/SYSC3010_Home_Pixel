#!/usr/bin/env python3
"""
test_thingspeak.py
"""
import random
import logging
import time
from unittest import TestCase, main
from thingspeakwriter import ThingSpeakWriter
from thingspeakreader import ThingSpeakReader
from constants import (L2_M_5C2_WRITE_KEY,
                       L2_M_5C2_READ_KEY,
                       L2_M_5C2_FEED,
                       GOOD_STATUS)

SLEEP_TIME_SECS = 1


class TestThingSpeak(TestCase):
    """
    Test methods in ThingSpeakWriter & ThingSpeakReader
    """

    def setUp(self):
        """
        Setup test method
        Sleep to allow time for ThingSpeak writes
        """
        self.writer = ThingSpeakWriter(L2_M_5C2_WRITE_KEY)
        self.reader = ThingSpeakReader(key=L2_M_5C2_READ_KEY,
                                       feed=L2_M_5C2_FEED)
        time.sleep(SLEEP_TIME_SECS)

    def test_good_write_to_channel(self):
        """
        Write to valid channel
        """
        test_fields = {'field1': 'abc123'}
        status, reason = self.writer.write_to_channel(test_fields)

        err_msg = 'Status of write was unexpected!'
        self.assertEqual(status, GOOD_STATUS, err_msg)
        self.assertEqual(reason, 'OK', err_msg)
        pass

    def test_bad_write_to_channel(self):
        """
        Write to invalid channel
        """
        bad_writer = ThingSpeakWriter(key='')
        test_fields = {'field1': 'abc123'}
        status, reason = bad_writer.write_to_channel(test_fields)

        err_msg = 'Status of write was unexpected!'
        self.assertEqual(status, 400, err_msg)
        self.assertEqual(reason, 'Bad Request', err_msg)

    def test_read_channel(self):
        """
        Read from channel
        """
        expected = '{}'.format(random.randint(1, 999999))
        test_fields = {'field1': expected}
        status, reason = self.writer.write_to_channel(test_fields)

        err_msg = 'Status of write was unexpected!'
        self.assertEqual(status, GOOD_STATUS, err_msg)
        self.assertEqual(reason, 'OK', err_msg)

        actual_fields = self.reader.read_from_channel()
        actual = actual_fields['feeds'][-1]['field1']

        err_msg = 'Field read back does not match expected field!'
        self.assertEqual(actual, expected, err_msg)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    main()
