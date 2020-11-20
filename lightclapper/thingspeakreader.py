#!/usr/bin/env python3
"""
thingspeakreader.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import requests
import argparse
import logging
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

    reader = ThingSpeakReader(c.L2_M_5C2_READ_KEY, c.L2_M_5C2_FEED)
    fields = reader.read_from_channel(num_entries=number_of_entries)
    for f in fields.get('feeds', []):
        logging.info(f)

    read_url = c.READ_URL_LIMITED.format(
        CHANNEL_FEED=c.L2_M_5C2_FEED,
        RESULTS=number_of_entries)
    logging.info('Compare read data with results here: {}'.format(read_url))


def parse_args():
    """
    Parses arguments for manual verification of the ThingSpeakReader

    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    default_test_entries = 10

    parser = argparse.ArgumentParser(
        description='Run the ThingSpeakReader test program (CTRL-C to exit)')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    parser.add_argument('-n',
                        '--number',
                        default=default_test_entries,
                        type=int,
                        metavar='<{}>'.format(default_test_entries),
                        help='# of entries to read from ThingSpeak channel')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)
    read_test(args.number)
