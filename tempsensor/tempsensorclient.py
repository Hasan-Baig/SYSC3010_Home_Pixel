import logging
import time
import re
import argparse
from tempDB import TempDB
from thingspeakreader import ThingSpeakReader
import thingspeakinfo as c

POLL_TIME_SECS = 10
DATE_LIST_LENGTH = 2
DATE_INDEX = 0
TIME_INDEX = 1
FIRST_INDEX = 0
LAST_INDEX = -1
INCREMENT = 1

class TempSensorClient:
	def __init__(self, key=c.READ_KEY_D1, feed=c.FEED_D1):
		self.__reader = ThingSpeakReader(key, feed)
		self.__latest_data = None

		with TempDB(db_file = c.TEMP_SENSOR_DB_FILE, name = c.TEMP_SENSOR_TABLE) as db_obj:
			if not db_obj.table_exists():
				db_obj.create_table()

	def poll_channel(self):
		logging.info('TempSensorClient Program Running')
		try:
			while True:
				channel_data = self.read_from_channel()
			if channel_data:
				self.__add_data_from_channel(channel_data)
			time.sleep(POLL_TIME_SECS)
		except KeyboardInterrupt:
			logging.info('Exiting due to keyboard interrupt')
		except BaseException as e:
			logging.error('An error or exception occured!')
			logging.error('Error Traceback: {}'.format(e))

	def read_from_channel(self):
		parsed_data = []
		read_data = self.__reader.read_from_channel()
		feeds = read_data.get('feeds', '')

		if not feeds or feeds[LAST_INDEX] == self.__latest_data:
			logging.debug('No new data parsed fromm channel')
			return parsed_data

		if self.__latest_data:
			start_index = feeds.index(self.__latest_data) + INCREMENT
		else:
			start_index = FIRST_INDEX

		for f in feeds[start_index:]:
			parse_status, data = self.__parse_data(f)
			if parse_status:
				parsed_data.append(data)

		self.__latest_data = feeds[LAST_INDEX]

		return parsed_data

	def __parse_data(self, feed):
		data = {}
		date_data = feed.get('created_at', '')
		date_list = re.split('T|Z', date_data)
		location = feed.get(c.LOCATION_FIELD, '')
		node_id = feed.get(c.NODE_ID_FIELD, '')

		try:
			fan_status = int(feed.get(c.FAN_STATUS_FIELD, ''))
			tval = int(feed.get(c.TEMP_VAL_FIELD, ''))
		except ValueError:
			logging.warning('Skipping entry iwth invalid fan and temp val type')
			return False, data

		if len(date_list) < DATE_LIST_LENGTH:
			logging.warning('Skipping entry with unparseable date')
			return False, data
		elif '' in [location, node_id]:
			logging.warning('Skipping entry iwth missing fields')
			return False, data
		elif fan_status not in [0, 1]:
			logging.warning('Skipping entry with invalid fan status')
			return False, data

		data = {'date': date_list[DATE_INDEX],
			'time': date_list[TIME_INDEX],
			'locaiton': location,
			'nodeID': node_id,
			'fanStatus': fan_status,
			'tempVal': tval}

		logging.debug('Data parsed from channel: {}'.format(data))
		return True, data

	def __add_data_from_channel(self, channel_data):
		with TempDB(db_file = 'tempsensor.db', name = 'TempSensor') as db_obj:
			for data in channel_data:
				if not db_obj.record_exists(data):
					db_obj.add_record(data)

def temp_sensor_client_test():
	url = c.READ_URL.format(
	    CHANNEL_FEED = c.FEED_D1,
	    READ_KEY = c.READ_KEY_D1)
	logging.info('Link to Thingspeak channel data: {}'.format(url))

	temp_sensor_client = TempSensorClient(
	    key = c.READ_KEY_D1,
	    feed = c.FEED_D1)
	temp_sensor_client.poll_channel()

def parse_args():
	parser = argparse.ArgumentParser(
		description = 'Run the TempSensorClient program (CTRL-C to exit)')

	parser.add_argument('-v',
			    '--verbose',
			    default = False,
			    action = 'store_true',
			    help = 'Print all debug logs')
	args = parser.parse_args()
	return args

if __name__ == "__main__":
	args = parse_args()
	logging_level = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(format = c.LOGGING_FORMAT, level = logging_level)
	temp_sensor_client_test()
