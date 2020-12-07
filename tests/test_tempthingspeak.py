import random
import logging
import time
from unittest import TestCase, main
from thingspeakwriter import ThingSpeakWriter
from thingspeakreader import ThingSpeakReader
import thingspeakinfo as c

class TestThingSpeak(TestCase):
	def setUp(self):
		self.__writer = ThingSpeakWriter(c.WRITE_KEY_D2)
		self.__reader = ThingSpeakReader(key = c.READ_KEY_D2, feed = c.FEED_D2)
		time.sleep(1)

	def test_write_to_channel(self):
		test_fields = {'field1': "abc123"}
		expected_reason = "OK"
		error_msg = "Status of write was unexpected!"

		status, reason = self.__writer.write_to_channel(test_fields)
		self.assertEqual(status, c.GOOD_STATUS, error_msg)
		self.assertEqual(reason, expected_reason, error_msg)

	def test_write_to_invalid_channel(self):
		bad_writer = ThingSpeakWriter(key = '')
		test_fields = {'field1': "abc123"}
		expected_status = 400
		expected_reason = 'Bad Request'
		error_msg = ''

		status, reason = bad_writer.write_to_channel(test_fields)
		error_msg = 'Status of write was unexpected!'
		self.assertEqual(status, expected_status, error_msg)
		error_msg = 'Reason of request response was unexpected!'
		self.assertEqual(reason, expected_reason, error_msg)

	def test_write_and_read(self):
		random_min = 1
		random_max = 100000000
		expected_field = str(random.randint(random_min, random_max))
		error_msg = ''
		test_fields = {'field1': expected_field}

		status, reason = self.__writer.write_to_channel(test_fields)
		error_msg = 'Status of write was unexpected'
		self.assertEqual(status, c.GOOD_STATUS, error_msg)

		actual_fields = self.__reader.read_from_channel()
		actual = actual_fields['feeds'][-1]['field1']
		error_msg = 'Field read back does not match expected field!'
		self.assertEqual(actual, expected_field, error_msg)

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level = logging.DEBUG)
	main()
