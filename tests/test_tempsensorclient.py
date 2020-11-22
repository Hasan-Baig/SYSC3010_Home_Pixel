#!/usr/bin/env python3

import random
import logging
from unittest import TestCase, main
from tempsensor.thingspeakwriter import ThingSpeakWriter
from tempsensorclient import TempSensorClient
from thingspeakinfo import (READ_KEY_D2, WRITE_KEY_D2, FEED_D2)

class TestTempSensorClient(TestCase):
	def setUp(self):
		self.writer = ThingSpeakWriter(WRITE_KEY_D2)
		self.storage = TempSensorClient(key = READ_KEY_D2, feed = FEED_D2)

	def test_data_parse(self):
		expected = "{}".format(random.randint(1, 999999))
		test_fields = {"field1": expected}
		status, reason = self.writer.write(test_fields)

		actual_data = self.storage.read_from_channel()
		actual = []
		for data in actual_data:
			actual.append(data.get("fanStatus", ''))

		error_msg = "Parsed data does not match expected field"
		self.assertIn(expected, actual, error_msg)

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level = logging.INFO)
	main()
