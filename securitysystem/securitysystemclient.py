"""
Read data from ThingSpeak and store in Database
"""
import logging
import time
import string
from sqliteDB import SecurityDB
from thingspeakreader import ThingSpeakReader
from constants import (L2_M_5A1_READ_KEY,
                       L2_M_5A2_READ_KEY,
                       L2_M_5A1_FEED,
                       L2_M_5A2_FEED)

POLL_TIME_SECS = 5
HEADER = 1

class SecuritySystemClient:

    def __init__(self, key, feed):
        self.__reader = ThingSpeakReader(key, feed)

        with SecurityDB(db_file='securitysystem.db', name='SecuritySystem') as db_obj:
            if not db_obj.table_exists():
                db_obj.create_table()

    def poll_channel(self):
        try:
            while True:
                channel_data = self.read_channel()
                if channel_data:
                    self.__add_data_from_channel(channel_data)
                time.sleep(POLL_TIME_SECS)
        except KeyboardInterrupt:
            print('Exiting')
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))

    def read_channel(self):
        read_data = self.__reader.read_from_channel(HEADER)
        feeds = read_data['feeds']

        parsed_data = []
        data = {'date': '', 'time': ''}

        for f in feeds:
            date_data = f['field1']
            date_list = date_data.split(' ')

            if len(date_list) < 2:
                return None

            data['date'] = date_list[0]
            data['time'] = date_list[1]

            logging.debug('Data read: {}'.format(data))
            parsed_data.append(data)

        return parsed_data

    def __add_data_from_channel(self, channel_data):
        with SecurityDB(db_file='securitysystem.db', name='SecuritySystem') as db_obj:
            for data in channel_data:
                if not db_obj.record_exists(data):
                    db_obj.add_record(data)


def security_system_client_test():
    security_system_client = SecuritySystemClient(L2_M_5A1_READ_KEY,L2_M_5A1_FEED)
    security_system_client.poll_channel()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    security_system_client_test()