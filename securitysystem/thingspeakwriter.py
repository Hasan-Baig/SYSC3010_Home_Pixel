#!/usr/bin/env python3
"""
Writing data collected from motion sensor to ThingSpeak
"""
import http.client
import urllib
import logging
import argparse
from datetime import datetime
import constants as c

class ThingSpeakWriter():
    """
    Class to write to ThingSpeak channel
    Attributes
    ----------
    __key : str
        Write API key
    Methods
    -------
    write(fields)
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

    def write(self, fields):
        """
        Writes to a given ThingSpeak channel
        Parameters
        ----------
        fields : dict
            fields to write to ThingSpeak channel
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
                   
        conn = http.client.HTTPConnection('api.thingspeak.com:80')

        try:
            conn.request('POST', '/update', params, headers)
            response = conn.getresponse()
            status = response.status
            reason = response.reason
            conn.close()
        except Exception:
            print("Connection failed!")

        logging.debug('({}, {})'.format(status, reason))
        return status, reason

def write_test():
    """
    Creates a ThingSpeakWriter object for manual verification
    """
    writer = ThingSpeakWriter(c.L2_M_5A2_WRITE_KEY)

    test_date = datetime.now().strftime("%Y-%m-%d")
    test_time = datetime.now().strftime("%H:%M:%S")

    fields = {c.TEST_FIELD: "{} {}".format(test_date, test_time)}

    logging.info('Writing {} {} to {}'.format(test_date, test_time, c.TEST_FIELD))
    writer.write(fields)

    read_url = c.READ_URL.format(
        CHANNEL_FEED=c.L2_M_5A2_FEED,
        READ_KEY=c.L2_M_5A2_READ_KEY)
    
    logging.info('Check results here: {}'.format(read_url))

def parse_args():
    """
    Parses arguments for manual verification of the ThingSpeakWriter
    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(
        description='Run the ThingSpeakWriter test program')

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
    write_test()