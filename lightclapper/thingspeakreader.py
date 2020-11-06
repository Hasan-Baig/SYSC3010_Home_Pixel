#!/usr/bin/env python3
"""
thingspeakreader.py
TODO: Move to common directory later if needed
"""
import requests
import logging
from constants import (L2_M_5C1_READ_KEY,
                       L2_M_5C2_READ_KEY,
                       L2_M_5C1_FEED,
                       L2_M_5C2_FEED,
                       READ_URL)


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
    read_from_channel()
        Read data from ThingSpeak channel
    """

    def __init__(self, key=L2_M_5C1_READ_KEY, feed=L2_M_5C1_FEED):
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

    def read_from_channel(self, header=2):
        """
        Read from a given ThingSpeak channel

        Parameters
        ----------
        header : int
            Number of data entries to read

        Returns
        -------
        fields : dict
            fields read from ThingSpeak channel
        """
        read_url = READ_URL.format(
            CHANNEL_FEED=self.__feed,
            READ_KEY=self.__key,
            HEADER=header)
        fields = requests.get(read_url).json()
        return fields


def read_test():
    """
    Creates a ThingSpeakRead object for manual verification
    """
    reader = ThingSpeakReader(key=L2_M_5C2_READ_KEY, feed=L2_M_5C2_FEED)
    fields = reader.read_from_channel()
    logging.debug(fields)
    read_url = READ_URL.format(
        CHANNEL_FEED=L2_M_5C2_FEED,
        READ_KEY=L2_M_5C2_READ_KEY,
        HEADER=2)
    logging.debug('Check results here: {}'.format(read_url))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    read_test()
