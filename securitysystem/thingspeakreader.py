#!/usr/bin/env python3
"""
Reading data collected from ThingSpeak
"""
import requests
import json
import logging
import argparse
import constants as c

class ThingSpeakReader():
    """
    Class to read from ThingSpeak channel
    Attributes
    ----------
    __key : str
        Read API key
    __feed : str
        Feed number for channel
    Methods
    -------
    read_from_channel(num_entries)
        Read data from ThingSpeak channel
    """
    def __init__(self, key, feed):
        """
        Initializes the ThingSpeakReader
        Parameters
        ----------
        key : str
            Read API key
        feed : str
            Feed number for channel
        """
        self.__key = key
        self.__feed = feed

    def read_from_channel(self, num_entries=None):
        """
        Read from a given ThingSpeak channel
        Parameters
        ----------
        num_entries : int
            Option to specify N entries read back
        Returns
        -------
        fields : dict
            fields read from ThingSpeak channel
        """
        if num_entries:
            read_url = c.READ_URL_LIMITED.format(
                CHANNEL_FEED=self.__feed,
                READ_KEY=self.__key,
                RESULTS=num_entries)
        else:
            read_url = c.READ_URL.format(
                CHANNEL_FEED=self.__feed,
                READ_KEY=self.__key)

        fields = requests.get(read_url).json()
        return fields

def read_test(number_of_entries):
    """
    Creates a ThingSpeakReader object for manual verification
    Parameters
    ----------
    number_of_entries : int
        Number of entries to read back if available
    """
    logging.info('Reading last {} feed entries'.format(number_of_entries))

    reader = ThingSpeakReader(c.L2_M_5A2_READ_KEY, c.L2_M_5A2_FEED)
    jsonData = reader.read_from_channel(num_entries=number_of_entries)
    
    feild_1=jsonData['feeds']
    
    values=[]
    for x in feild_1:
        values.append(x['field1'])
    
    logging.debug('The last {} results are: {}'.format(number_of_entries, values))

def parse_args():
    """
    Parses arguments for manual verification of the ThingSpeakReader
    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    default_test_results = 10

    parser = argparse.ArgumentParser(
        description='Run the ThingSpeakReader test program')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    parser.add_argument('-n',
                        '--number',
                        default=default_test_results,
                        type=int,
                        metavar='<number_of_results>',
                        help='# of entries to read from ThingSpeak channel')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)
    read_test(args.number)