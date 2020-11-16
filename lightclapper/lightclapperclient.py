"""
lightclapperclient.py
"""
import logging
import time
import re
from sqliteDB import LightDB
from thingspeakreader import ThingSpeakReader
from constants import (L2_M_5C1_READ_KEY,
                       L2_M_5C1_FEED)

POLL_TIME_SECS = 5   # TODO: check this time
HEADER = 1


class LightClapperClient:
    """
    Class to parse light clapper data
    and store in database

    Attributes
    ----------
    __reader : ThingSpeakReader
        Reader of ThingSpeak channel
    __db : LightClapperDB
        DB to store LightClapper node data

    Methods
    -------
    poll_channel()
        polls for new data from channel
    read_from_channel()
        Read & parse data from channel
    __add_data_from_channel()
        Add data from channel if it's not in DB table
    """

    def __init__(self, key=L2_M_5C1_READ_KEY, feed=L2_M_5C1_FEED):
        """
        Initialize light clapper node storage

        Parameters
        ----------
        key : str
            Read API key
        feed : str
            Feed number for channel
        """
        self.__reader = ThingSpeakReader(key=key, feed=feed)

        with LightDB(db_file='lightclapper.db', name='LightClapper') as db_obj:
            if not db_obj.table_exists():
                db_obj.create_table()

    def poll_channel(self):
        """
        Poll for new data in channel
        """
        try:
            while True:
                channel_data = self.read_from_channel()
                if channel_data:
                    self.__add_data_from_channel(channel_data)
                time.sleep(POLL_TIME_SECS)
        except KeyboardInterrupt:
            print('Exiting')
        except BaseException:
            print('An error or exception occurred!')

    def read_from_channel(self):
        """
        Parses data read from channel related to the
        Light Clapper Node

        Returns
        -------
        parsed_data : list
            data parsed from JSON dict read from channel
        """
        read_data = self.__reader.read_from_channel(header=HEADER)
        feeds = read_data['feeds']
        parsed_data = []
        data = {'date': '',
                'time': '',
                'lightStatus': ''}

        for f in feeds:
            date_data = f.get('created_at', '')
            date_list = re.split('T|Z', date_data)

            if len(date_list) < 2:
                return None

            data['date'] = date_list[0]
            data['time'] = date_list[1]
            data['lightStatus'] = f['field1']

            logging.debug('Data read: {}'.format(data))
            parsed_data.append(data)

        return parsed_data

    def __add_data_from_channel(self, channel_data):
        """
        Compares existing DB table with data read from channel.
        Add data if not in Table

        Parameters
        ----------
        channel_data : list
            data read from the channel
        """
        with LightDB(db_file='lightclapper.db', name='LightClapper') as db_obj:
            for data in channel_data:
                if not db_obj.record_exists(data):
                    db_obj.add_record(data)


def light_clapper_client_test():
    """
    Creates a LightClapperClient object for manual verification
    """
    light_clapper_client = LightClapperClient(
        key=L2_M_5C1_READ_KEY,
        feed=L2_M_5C1_FEED)
    light_clapper_client.poll_channel()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    light_clapper_client_test()
