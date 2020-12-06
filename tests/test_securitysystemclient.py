#!/usr/bin/env python3

"""
SecuritySystemClient.py tests
"""

import logging
from unittest import TestCase, main
from unittest.mock import patch
from securitysystemclient import SecuritySystemClient
import constants as c


@patch('thingspeakreader.ThingSpeakReader.read_from_channel')
class TestSecuritySystemClient(TestCase):
    """
    Test methods for SecuritySystemClient
    Attributes
    ----------
    __client : SecuritySystemClient
    Methods
    -------
    setUp()
    test_parse_good_data(mock_read)
    test_parse_bad_data(mock_read)
    """

    def setUp(self):
        """
        Setup SecuritySystemClient
        """
        self.__client = SecuritySystemClient(
            key=c.L2_M_5A2_READ_KEY,
            feed=c.L2_M_5A2_FEED)

    def test_parse_good_data(self, mock_read):
        """
        Test parsing valid data
        Parameters
        ----------
        mock_read : unittest.mock.Mock
            Mock patched thingspeakreader.ThingSpeakReader.read_from_channel
        """
        data = {'date': '2020-11-23',
                'time': '04:31:14',
                'location': 'hasan_bedroom',
                'nodeID': 'SecuritySystem_1'}

        date_data = data.get(c.DATE_TIME_FIELD, '')
        date_list = date_data.split(' ')

        mock_data = {'feeds':
                      [{
                        c.LOCATION_FIELD: data['location'],
                        c.NODE_ID_FIELD: data['nodeID'],
                        c.DATE_TIME_FIELD: '{d} {t}'.format(d=data['date'], t=data['time'])
                      }]
                    }

        expected = [data]
        mock_read.return_value = mock_data
        actual = self.__client.read_channel()
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
        data = {'date': '2020-11-23',
                'time': '04:31:14',
                'nodeID': 'SecuritySystem_1'}

        mock_data = {'feeds':
                      [{
                        c.NODE_ID_FIELD: data['nodeID'],
                        c.DATE_TIME_FIELD: '{d} {t}'.format(d=data['date'], t=data['time'])
                      }]
                    }
                    
        expected = []
        mock_read.return_value = mock_data
        actual = self.__client.read_channel()
        err_msg = 'Data parsed unexpectedly'
        self.assertEqual(actual, expected, err_msg)


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()