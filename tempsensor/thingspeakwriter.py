#!/usr/bin/env python3

import http.client
import urllib
import logging
from datetime import datetime

from thingspeakinfo import (WRITE_KEY_D2, READ_KEY_D2, FEED_D2, READ_URL)

class ThingSpeakWriter():
	def __init__(self, key):
		self.__key = key

	def write(self, fields):
		fields['key'] = self.__key
		status = None
		reason = None
		params = urllib.parse.urlencode(fields)

		logging.debug('Fields: {}'.format(fields))

		headers = {"Content-typeZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = http.client.HTTPConnection("api.thingspeak.com:80")

		try:
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			status = response.status
			reason = response.reason
			conn.close()
		except:
			print ("Connection Failed")

		logging.debug('{0}, {1}'.format(status, reason))
		return status, reason

def write_test():
	writer = ThingSpeakWriter(WRITE_KEY_D2)
	test_data = datetime.now()
	fields = {"field1" : test_data}

	logging.debug("Writing {} to field1".format(test_data))
	writer.write(fields)

	read_url = READ_URL.format(CHANNEL_FEED = FEED_D2, READ_KEY = READ_KEY_D2, HEADER = 2)
	logging.debug("Check results here --> {}".format(read_url))

if __name__ == "__main__":
	logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s", level = logging.DEBUG)
	write_test()


