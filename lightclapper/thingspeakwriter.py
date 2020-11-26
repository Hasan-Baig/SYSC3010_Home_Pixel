#!/usr/bin/env python3
"""
thingspeakwriter.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import http.client
import urllib
import random
import argparse
import logging
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
    write_to_channel(fields)
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
            fields to write to ThingSpeak channel

        Returns
        -------
        status : int
            status of write
        reason : str
            reason for status of write
        """
        headers = {'Content-typZZe': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}
        fields['key'] = self.__key
        status = None
        reason = None
        params = urllib.parse.urlencode(fields)
        logging.debug('Fields to write: {}'.format(fields))

        try:
            conn = http.client.HTTPConnection('api.thingspeak.com:80')
            conn.request('POST', '/update', params, headers)
            response = conn.getresponse()
            status = response.status
            reason = response.reason
            conn.close()
        except Exception:
            logging.error("Connection failed!")

        logging.debug('{response_status}, {response_reason}'.format(
            response_status=status,
            response_reason=reason))
        return status, reason


def write_test(test_data):
    """
    Creates a ThingSpeakWriter object for manual verification

    Parameters
    ----------
    test_data : str
        Custom data to write to ThingSpeak channel
    """
    writer = ThingSpeakWriter(c.L2_M_5C2_WRITE_KEY)

    fields = {c.TEST_FIELD: test_data}

    logging.info('Writing {data} to {field}'.format(
        data=test_data,
        field=c.TEST_FIELD))
    writer.write_to_channel(fields)

    read_url = c.READ_URL.format(
        CHANNEL_FEED=c.L2_M_5C2_FEED,
        READ_KEY=c.L2_M_5C2_READ_KEY)
    logging.info('Compare with most recent data here: {}'.format(read_url))


def parse_args():
    """
    Parses arguments for manual verification of the ThingSpeakWriter

    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    random_min = 1
    random_max = 1000000
    default_test_data = str(random.randint(random_min, random_max))

    parser = argparse.ArgumentParser(
        description='Run the ThingSpeakWriter test program')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    parser.add_argument('-d',
                        '--data',
                        default=default_test_data,
                        type=str,
                        metavar='<custom_data>',
                        help='Data to write to ThingSpeak channel')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)
    write_test(args.data)
