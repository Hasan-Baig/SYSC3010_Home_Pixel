#!/usr/bin/env python3

import requests
import logging
import json
import argparse
import thingspeakinfo as c

class ThingSpeakReader():
	"""
	Thingspeak Reader Class
	"""
	def __init__(self, key=c.READ_KEY_D1, feed=c.FEED_D1):
		self.__key = key
		self.__feed = feed

	def read_from_channel(self, num_entries=None):
		"""
		Reading from the channel
		"""

		if num_entries:
			read_url = c.READ_URL_LIMITED.format(
				CHANNEL_FEED = self.__feed,
				READ_KEY = self.__key,
				RESULTS = num_entries)
		else:
			read_url = c.READ_URL.format(
				CHANNEL_FEED = self.__feed,
				READ_KEY = self.__key)

		fields = requests.get(read_url).json()
		return fields

def read_test():
	logging.info('Reading last {} feed entries'.format(number_of_entries))

	reader = ThingSpeakReader(c.READ_KEY_D2, c.FEED_D2)
	fields = reader.read_from_channel(num_entries = number_of_entries)
	for f in fields.get('feeds', []):
		logging.info(f)

	read_url = c.READ_URL_LIMITED.format(
		CHANNEL_FEED = c.FEED_D2,
		RESULTS = number_of_entries)
	logging.info('Compare read data with results here: {}'.format(read_url))

def parse_args():
	default_test_results = 10

	parser = argparse.ArgumentParser(
		description = 'Run the ThingSpeakReader test program')

	parser.add_argument('-v',
			    '--verbose',
			    default = False,
			    action = 'store_true',
			    help = 'Print all debug logs')

	parser.add_argument('-n',
			    '--number',
			    default = default_test_results,
			    type = int,
			    metavar = '<number_of_results>',
			    help = '# of entries to read from ThingSpeak Channel')

	args = parser.parse_args()
	return args

if __name__ == "__main__":
	args = parse_args()
	logging_level = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(format = c.LOGGIN_FORMAT, level = logging_level)
	read_test(args.number)

