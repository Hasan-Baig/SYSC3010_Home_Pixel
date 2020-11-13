#!/usr/bin/env python3
"""
Reading data collected from ThinkSpeak
"""
import requests
import json
import logging
from constants import (L2_M_5A2_READ_KEY,
                       L2_M_5A2_FEED,
                       READ_URL)


class ThingSpeakReader():

    def __init__(self, key, feed):
        self.__key = key
        self.__feed = feed

    def read_from_channel(self, header=2):
        read_url = READ_URL.format(
            CHANNEL_FEED=self.__feed,
            READ_KEY=self.__key,
            HEADER=header)
        fields = requests.get(read_url).json()
        return fields


def read_test():
    reader = ThingSpeakReader(L2_M_5A2_READ_KEY, L2_M_5A2_FEED)
    jsonData = reader.read_from_channel()
    logging.debug(jsonData)
    
    feild_1=jsonData['feeds']
    
    values=[]
    for x in feild_1:
        values.append(x['field1'])
    
    logging.debug('The last 2 results are: {}'.format(values))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    read_test()