#!/usr/bin/env python3
"""
test_lightclapperclient.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import logging
from unittest import TestCase, main
from unittest.mock import patch
from lightclapperclient import LightClapperClient
import constants as c


@patch('thingspeakreader.ThingSpeakReader.read_from_channel')
class TestLightClapperClient(TestCase):
    """
    Test methods in LightClapperClient

    Attributes
    ----------
    __client : LightClapperClient

    Methods
    -------
    setUp()
    test_parse_good_data(mock_read)
    test_parse_bad_data(mock_read)
    """

    def setUp(self):
        """
        Setup TestLightClapperClient
        """
        self.__client = LightClapperClient(
            key=c.L2_M_5C2_READ_KEY,
            feed=c.L2_M_5C2_FEED)

    def test_parse_good_data(self, mock_read):
        """
        Test parsing valid data

        Parameters
        ----------
        mock_read : unittest.mock.Mock
            Mock patched thingspeakreader.ThingSpeakReader.read_from_channel
        """
        data = {'date': '2020-11-21',
                'time': '21:44:53',
                'location': 'my_room',
                'nodeID': 'lightclapper_123',
                'lightStatus': c.ON_INT}
        mock_data = {'feeds':
                     [{'created_at': '{d}T{t}Z'.format(d=data['date'],
                                                       t=data['time']),
                       c.LOCATION_FIELD: data['location'],
                       c.NODE_ID_FIELD: data['nodeID'],
                       c.LIGHT_STATUS_FIELD: data['lightStatus']}]}

        expected = [data]
        mock_read.return_value = mock_data
        actual = self.__client.read_from_channel()
        err_msg = 'Expected data not successfully parsed'
        self.assertEqual(actual, expected, err_msg)

    def test_parse_bad_data(self, mock_read):
        """
        Test parsing invalid data (missing or incorrect fields)

        Parameters
        ----------
        mock_read : unittest.mock.Mock
            Mock patched thingspeakreader.ThingSpeakReader.read_from_channel
        """
        data = {'date': '2020-11-21',
                'time': '21:44:53',
                'lightStatus': 'abc'}
        mock_data = {'feeds':
                     [{'created_at': '{d}T{t}Z'.format(d=data['date'],
                                                       t=data['time']),
                       c.LIGHT_STATUS_FIELD: data['lightStatus']}]}

        expected = []
        mock_read.return_value = mock_data
        actual = self.__client.read_from_channel()
        err_msg = 'Data parsed unexpectedly'
        self.assertEqual(actual, expected, err_msg)


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()
