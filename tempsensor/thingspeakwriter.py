#!/usr/bin/env python3

import http.client
import urllib
import random
import logging
import thingspeakinfo as c
from datetime import datetime

class ThingSpeakWriter():
	def __init__(self, key):
		self.__key = key

	def write_to_channel(self, fields):
		fields['key'] = self.__key
		status = None
		reason = None
		params = urllib.parse.urlencode(fields)

		logging.debug('Fields to write: {}'.format(fields))

		headers = {"Content-typeZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = http.client.HTTPConnection("api.thingspeak.com:80")

		try:
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			status = response.status
			reason = response.reason
			conn.close()
		except Exception:
			logging.error("Connection Failed")

		logging.debug('{response_status}, {response_reason}'.format(
			response_status = status,
			response_reason = reason))
		return status, reason

def write_test():
	writer = ThingSpeakWriter(c.WRITE_KEY_D2)
	test_data = datetime.now()
	fields = {c.TEST_FIELD: test_data}

	logging.debug("Writing {data} to {field}".format(
		data=test_data,
		field = c.TEST_FIELD))
	writer.write_to_channel(fields)

	read_url = READ_URL.format(CHANNEL_FEED = c.FEED_D2, READ_KEY = c.READ_KEY_D2)
	logging.info("Check results here --> {}".format(read_url))

if __name__ == "__main__":
	logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s", level = logging.DEBUG)
	write_test()


