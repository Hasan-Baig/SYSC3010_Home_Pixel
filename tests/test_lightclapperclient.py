#!/usr/bin/env python3
"""
test_lightclapperclient.py
TODO: add more tests
"""
import random
import logging
from unittest import TestCase, main
from thingspeakwriter import ThingSpeakWriter
from lightclapperclient import LightClapperClient
import constants as c


class TestLightClapperClient(TestCase):
    """
    Test methods in LightClapperStorage
    """

    def setUp(self):
        """
        Setup TestLightClapperStorage
        """
        self.writer = ThingSpeakWriter(c.L2_M_5C2_WRITE_KEY)
        self.storage = LightClapperClient(
            key=c.L2_M_5C2_READ_KEY,
            feed=c.L2_M_5C2_FEED)

    def test_data_parse(self):
        """
        Test parsing data read from channel
        """
        expected = '{}'.format(random.randint(1, 999999))
        test_fields = {'field1': expected}
        status, reason = self.writer.write_to_channel(test_fields)

        actual_data = self.storage.read_from_channel()
        actual = []
        for data in actual_data:
            actual.append(data.get('lightStatus', ''))

        err_msg = 'Parsed data does not match expected field'
        self.assertIn(expected, actual, err_msg)


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()
