#!/usr/bin/env python3

#import random
import logging
from unittest import TestCase, main
from unittest.mock import patch
from tempsensor.thingspeakwriter import ThingSpeakWriter
from tempsensorclient import TempSensorClient
import thingspeakinfo as c
#from thingspeakinfo import (READ_KEY_D2, WRITE_KEY_D2, FEED_D2)

@patch('thingspeakreader.ThingSpeakReader.read_from_channel')
class TestTempSensorClient(TestCase):
	def setUp(self):
		#self.writer = ThingSpeakWriter(WRITE_KEY_D2)
		self.__client = TempSensorClient(key = c.READ_KEY_D2, feed = c.FEED_D2)

	def test_data_parse(self, mock_read):
		#expected = "{}".format(random.randint(1, 999999))
		#test_fields = {"field1": expected}
		test_fields = {'date': '2020-12-06',
			       'time': '16:23:14',
			       'location': 'my_room',
			       'nodeID': 'tempsensor_123',
			       'fanStatus': 1,
			       'tempVal': 23.4}

		mock_data = {'feeds':
			     [{'created_at': '{d}T{t}Z'.format(d=test_fields['date'],
							       t=test_fields['time']),
			       c.LOCATION_FIELD: test_fields['location'],
			       c.NODE_ID_FIELD: test_fields['nodeID'],
			       c.FAN_STATUS_FIELD: test_fields['fanStatus'],
			       c.TEMP_VAL_FIELD: test_fields['tempVal']}]}

		expected = [test_fields]
		mock_read.return_value = mock_data
		actual = self.__client.read_from_channel()
		error_msg = 'Expected data does not match expected field'
		self.assertEqual(actual, expected, error_msg)

		"""
		actual_data = self.storage.read_from_channel()
		actual = []
		for data in actual_data:
			actual.append(data.get("fanStatus", ''))

		error_msg = "Parsed data does not match expected field"
		self.assertIn(expected, actual, error_msg)
		"""

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level = logging.INFO)
	main()
