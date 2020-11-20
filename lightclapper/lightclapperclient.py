"""
lightclapperclient.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import logging
from time import sleep
import re
from sqliteDB import LightDB
from thingspeakreader import ThingSpeakReader
import constants as c

POLL_TIME_SECS = 5
DATE_LIST_LENGTH = 2
DATE_INDEX = 0
TIME_INDEX = 1
LAST_INDEX = -1
INCREMENT = 1
POLLING = True


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
    __add_data_from_channel(channel_data)
        Add data from channel if it's not in DB table
    """

    def __init__(self, key=c.L2_M_5C1_READ_KEY, feed=c.L2_M_5C1_FEED):
        """
        Initialize light clapper node storage

        Parameters
        ----------
        key : str
            Read API key
        feed : str
            Feed number for channel
        """
        self.__reader = ThingSpeakReader(key, feed=feed)

        with LightDB(db_file=c.LIGHT_CLAPPER_DB_FILE,
                     name=c.LIGHT_CLAPPER_TABLE) as db_obj:
            if not db_obj.table_exists():
                db_obj.create_table()

    def poll_channel(self):
        """
        Poll for new data in channel
        """
        try:
            while POLLING:
                channel_data = self.read_from_channel()

                if channel_data:
                    self.__add_data_from_channel(channel_data)

                sleep(POLL_TIME_SECS)

        except KeyboardInterrupt:
            logging.info('Exiting due to keyboard interrupt')

        except BaseException:
            logging.error('An error or exception occurred!')

    def read_from_channel(self):
        """
        Parses data read from channel related to the
        Light Clapper Node

        Returns
        -------
        parsed_data : list
            data parsed from JSON dict read from channel
        """
        parsed_data = []
        data = {'date': '',
                'time': '',
                'location': '',
                'nodeID': '',
                'lightStatus': ''}
        read_data = self.__reader.read_from_channel()
        feeds = read_data['feeds']

        # Return if no new data in channel after last saved data
        last_feed = feeds[LAST_INDEX]
        if last_feed == self.__latest_data:
            return parsed_data

        start_index = feeds.index(self.__latest_data) + INCREMENT

        for f in feeds[start_index:]:
            date_data = f.get('created_at', '')
            date_list = re.split('T|Z', date_data)

            if len(date_list) < DATE_LIST_LENGTH:
                # Skip entry since date cannot be parsed
                continue

            data['date'] = date_list[DATE_INDEX]
            data['time'] = date_list[TIME_INDEX]
            data['location'] = f.get(c.LOCATION_FIELD, '')
            data['nodeID'] = f.get(c.NODE_ID_FIELD, '')
            data['lightStatus'] = f.get(c.LIGHT_STATUS_FIELD, '')

            if '' in (data['nodeID'], data['location'], data['lightStatus']):
                # Skip entry since node, location or status are empty
                continue

            logging.debug('Data found: {}'.format(data))
            parsed_data.append(data)

        self.__latest_data = parsed_data[LAST_INDEX]

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
        key=c.L2_M_5C1_READ_KEY,
        feed=c.L2_M_5C1_FEED)
    light_clapper_client.poll_channel()


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_DEFAULT_LEVEL)
    light_clapper_client_test()
