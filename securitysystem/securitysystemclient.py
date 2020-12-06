"""
Read data from ThingSpeak and store in Database
"""
import logging
import time
import string
import argparse
from sqliteDB import SecuritySystemDB
from thingspeakreader import ThingSpeakReader
import constants as c

POLL_TIME_SECS = 5
FIRST_INDEX = 0
LAST_INDEX = -1
INCREMENT = 1
DATE_LIST_LENGTH = 2
DATE_INDEX = 0
TIME_INDEX = 1
POLLING = True

class SecuritySystemClient:
    """
    Class to parse SecuritySystem node data
    and store in SecuritySystemDB database
    Attributes
    ----------
    __reader : ThingSpeakReader
        Reader of ThingSpeak channel
    __latest_data : dict
        Latest data read from ThingSpeak channel
    Methods
    -------
    poll_channel()
        polls for new data from channel
    read_channel()
        Read & parse data from channel
    __parse_data(feed)
        Parse data for SecuritySystem fields
    __add_data_from_channel(channel_data)
        Add data from channel if it's not in DB table
    """
    def __init__(self, key, feed):
        """
        Initialize SecuritySystemClient
        Parameters
        ----------
        key : str
            Read API key
        feed : str
            Feed number for channel
        """
        self.__reader = ThingSpeakReader(key, feed)
        self.__latest_data = None

        with SecuritySystemDB(db_file=c.SECURITY_SYSTEM_DB, name=c.SECURITY_SYSTEM_NAME) as db_obj:
            if not db_obj.table_exists():
                db_obj.create_table()

    def poll_channel(self):
        """
        Poll for new data in channel.
        If new data is found, add it to SecuritySystemDB
        """
        logging.info('SecuritySystemClient program running')
        try:
            while POLLING:
                channel_data = self.read_channel()

                if channel_data:
                    logging.info('New data parsed from channel')
                    self.__add_data_from_channel(channel_data)

                time.sleep(POLL_TIME_SECS)
        except KeyboardInterrupt:
            print('Exiting due to keyboard interrupt')
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))

    def read_channel(self):
        """
        Parses data read from channel related to the
        SecuritySystem node
        Returns
        -------
        parsed_data : list
            data parsed from JSON dict read from channel
        """
        read_data = self.__reader.read_from_channel()
        feeds = read_data['feeds']
        parsed_data = []

        # Return if no data or if no new data in channel after last saved data
        if not feeds or feeds[LAST_INDEX] == self.__latest_data:
            logging.debug('No new data parsed from channel')
            return parsed_data
        
        # Find starting index (start after latest data or at beginning)
        if self.__latest_data:
            start_index = feeds.index(self.__latest_data) + INCREMENT
        else:
            start_index = FIRST_INDEX
        
        # Iterate through feeds & parse for data
        for f in feeds[start_index:]:
            parse_status, data = self.__parse_data(f)
            if parse_status:
                parsed_data.append(data)

        # Update latest_data value to new latest data record
        self.__latest_data = feeds[LAST_INDEX]

        return parsed_data

    def __parse_data(self, feed):
        """
        Parse data from given feed
        Parameters
        ----------
        feed : dict
            Data read in feed from ThingSpeak
        Returns
        -------
        bool
            True if data successfully parsed
        data : dict
            Data parsed
        """
        data = {}      
        location = feed.get(c.LOCATION_FIELD, '')
        node_id = feed.get(c.NODE_ID_FIELD, '')
        date_data = feed.get(c.DATE_TIME_FIELD, '')
        date_list = date_data.split(' ')

        if len(date_list) < DATE_LIST_LENGTH:
            logging.warning('Skipping entry with unparseable date')
            print(date_list)
            return False, data
        elif '' in [location, node_id]:
            logging.warning('Skipping entry with missing fields')
            return False, data

        data = {'date': date_list[DATE_INDEX],
                'time': date_list[TIME_INDEX],
                'location': location,
                'nodeID': node_id}

        logging.debug('Data parsed from channel: {}'.format(data))
        return True, data

    def __add_data_from_channel(self, channel_data):
        """
        Compares existing DB table with data read from channel.
        Add data if not in Table
        Parameters
        ----------
        channel_data : list
            data read from the channel
        """
        with SecuritySystemDB(db_file=c.SECURITY_SYSTEM_DB, name=c.SECURITY_SYSTEM_NAME) as db_obj:
            for data in channel_data:
                if not db_obj.record_exists(data):
                    db_obj.add_record(data)


def security_system_client_test():
    """
    Creates a SecuritySystemClient object for manual verification
    """
    security_system_client = SecuritySystemClient(c.L2_M_5A1_READ_KEY,c.L2_M_5A1_FEED)
    security_system_client.poll_channel()

def parse_args():
    """
    Parses arguments for manual operation of the SecuritySystemClient
    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(
        description='Run the SecuritySystemClient program (CTRL-C to exit)')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)
    security_system_client_test()