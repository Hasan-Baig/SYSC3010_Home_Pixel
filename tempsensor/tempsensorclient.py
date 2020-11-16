import logging
import time
import re
from tempDB import TempDB
from thingspeakreader import ThingSpeakReader
from thingspeakinfo import (READ_KEY_D1, READ_KEY_D2, FEED_D1, FEED_D2)

POLL_TIME_SECS = 10
HEADER = 1

class TempSensorClient:
	def __init__(self, key, feed):
		self.__reader = ThingSpeakReader(key, feed)

		with TempDB(db_file = 'tempsensor.db', name = 'TempSensor') as db_obj:
			if not db_obj.table_exists():
				db_obj.create_table()

	def poll_channel(self):
		try:
			while True:
				channel_data = self.read_from_channel()
			if channel_data:
				self.__add_data_from_channel(channel_data)
			time.sleep(POLL_TIME_SECS)
		except KeyboardInterrupt:
			print ("Exiting")
		except BaseException as e:
			print ("An error or exception occurred: " + str(e))

	def read_from_channel(self):
		read_data = self.__reader.read_from_channel(HEADER)
		feeds = read_data['feeds']

		parsed_data = []
		data = {'date': '',
			'time': '',
			'fanStatus': ''}

		for f in feeds:
			date_data = f.get('created_at', '')
			date_list = re.split('T|Z', date_data)

			if len(date_list) < 2:
				return None

			data['date'] = date_list[0]
			data['time'] = date_list[1]
			data['fanStatus'] = f['field1']

			logging.debug('Data read: {}'.format(data))
			parsed_data.append(data)

		return parsed_data

	def __add_data_from_channel(self, channel_data):
		with TempDB(db_file = 'tempsensor.db', name = 'TempSensor') as db_obj:
			for data in channel_data:
				if not db_obj.record_exists(data):
					db_obj.add_record(data)

def temp_sensor_client_test():
	temp_sensor_client = TempSensorClient(READ_KEY_D1, FEED_D1)
	temp_sensor_client.poll_channel()

if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level = logging.DEBUG)
	temp_sensor_client_test()
