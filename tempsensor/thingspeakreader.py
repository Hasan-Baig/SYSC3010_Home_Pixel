#!/usr/bin/env python3

import requests
import logging
import json
from thingspeakinfo import (READ_KEY_D1, FEED_D1, READ_KEY_D2, FEED_D2, READ_URL)

class ThingSpeakReader():
	def __init__(self, key=READ_KEY_D1, feed=FEED_D1):
		self.__key = key
		self.__feed = feed

	def read_from_channel(self, header = 2):
		read_url = READ_URL.format(CHANNEL_FEED = self.__feed, READ_KEY = self.__key, HEADER = header)
		fields = requests.get(read_url).json()
		return fields

def read_test():
	reader = ThingSpeakReader(key = READ_KEY_D2, feed = FEED_D2)
#	reader = ThingSpeakReader(key = READ_KEY_D1, feed = FEED_D1)
	fields = reader.read_from_channel()
	logging.debug(fields)
	read_url = READ_URL.format(CHANNEL_FEED = FEED_D2, READ_KEY = READ_KEY_D2, HEADER = 2)
#	read_url = READ_URL.format(CHANNEL_FEED = FEED_D1, READ_KEY = READ_KEY_D2, HEADER = 2)
	logging.debug("Check Results --> {}".format(read_url))

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level = logging.DEBUG)
	read_test()

