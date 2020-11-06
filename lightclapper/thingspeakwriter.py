#!/usr/bin/env python3
"""
thingspreakwriter.py
TODO: move to common directory later if needed
"""
import http.client
import urllib
import logging
from datetime import datetime
from constants import (L2_M_5C2_WRITE_KEY,
                       L2_M_5C2_READ_KEY,
                       L2_M_5C2_FEED,
                       READ_URL)


class ThingSpeakWriter():
    """
    Class to write to ThingSpeak channel

    Attributes
    ----------
    __key : str
        Write API key

    Methods
    -------
    write_to_channel()
        Writes data to ThingSpeak channel
    """

    def __init__(self, key):
        """
        Initializes the ThingSpeakWriter

        Parameters
        ----------
        key : str
            Write API key
        """
        self.__key = key

    def write_to_channel(self, fields):
        """
        Writes to a given ThingSpeak channel

        Parameters
        ----------
        fields : dict
            field to write to ThingSpeak channel

        Returns
        -------
        status : int
            status of write
        reason : str
            reason for status of write
        """
        fields['key'] = self.__key
        status = None
        reason = None
        params = urllib.parse.urlencode(fields)

        logging.debug('Fields: {}'.format(fields))

        headers = {'Content-typZZe': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}
        try:
            conn = http.client.HTTPConnection('api.thingspeak.com:80')
            conn.request('POST', '/update', params, headers)
            response = conn.getresponse()
            status = response.status
            reason = response.reason
            conn.close()
        except Exception:
            print("Connection failed!")

        logging.debug('{0}, {1}'.format(status, reason))
        return status, reason


def write_test():
    """
    Creates a ThingSpeakWriter object for manual verification
    """
    writer = ThingSpeakWriter(L2_M_5C2_WRITE_KEY)

    test_data = datetime.now()
    fields = {'field1': test_data}

    logging.debug('Writing {} to field1'.format(test_data))
    writer.write_to_channel(fields)

    read_url = READ_URL.format(
        CHANNEL_FEED=L2_M_5C2_FEED,
        READ_KEY=L2_M_5C2_READ_KEY,
        HEADER=2)
    logging.debug('Check results here: {}'.format(read_url))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    write_test()
