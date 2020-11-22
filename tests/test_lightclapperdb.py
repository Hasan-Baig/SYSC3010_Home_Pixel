#!/usr/bin/env python3
"""
test_lightclapperdb.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import logging
import os
from unittest import TestCase, main, skipIf
from sqliteDB import LightClapperDB
import constants as c

TEMP_DB = 'temp_lightclapper.db'
TEMP_TABLE = 'temp_lightclapper'
PREMADE_DB = 'tests/test_db/test_lightclapper.db'
PREMADE_TABLE = 'test_lightclapper'


class TestLightClapperDB(TestCase):
    """
    Test methods in LightClapperDB

    Attributes
    ----------
    __db: LightClapperDB
        DB under test

    Methods
    -------
    setUp()
    tearDown()
    test_create_table()
    test_add_good_record()
    test_add_bad_record()
    test_get_records()
    """

    def setUp(self):
        """
        Setup TestLightClapperDB
        """
        self.__db = LightClapperDB(db_file=TEMP_DB,
                                   name=PREMADE_TABLE)
        self.__db.manual_enter()

    def tearDown(self):
        """
        Teardown TestLightClapperDB
        """
        self.__db.manual_exit()
        if os.path.exists(TEMP_DB):
            os.remove(TEMP_DB)

    def test_create_table(self):
        """
        Test creating table that doesn't already exist
        """
        err_msg = 'Table already exists'
        self.assertFalse(self.__db.table_exists(), err_msg)

        self.__db.create_table()

        err_msg = 'Table does not exist'
        self.assertTrue(self.__db.table_exists(), err_msg)

    def test_add_good_record(self):
        """
        Test adding new, good record to DB
        """
        record = {'date': '2020-11-22',
                  'time': '14:03:17',
                  'location': 'test_room',
                  'nodeID': 'lightclapper_456',
                  'lightStatus': c.ON_INT}

        self.__db.create_table()
        err_msg = 'Record exists unexpectedly'
        self.assertFalse(self.__db.record_exists(record), err_msg)

        self.__db.add_record(record)
        err_msg = 'Record failed to be added to DB table'
        self.assertTrue(self.__db.record_exists(record), err_msg)

    def test_add_bad_record(self):
        """
        Test adding new, bad record to DB
        """
        record = {'date': '2020-11-22',
                  'time': '14:03:17',
                  'lightStatus': c.ON_INT}

        self.__db.create_table()
        err_msg = 'Record exists unexpectedly'
        self.assertFalse(self.__db.record_exists(record), err_msg)

        self.assertRaises(Exception, self.__db.add_record, record)

    @skipIf(not os.path.exists(PREMADE_DB), 'Run test in top level directory')
    def test_get_records(self):
        """
        Test retrieving pre-determined records from DB.
        """
        self.__db = LightClapperDB(db_file=PREMADE_DB,
                                   name=PREMADE_TABLE)
        self.__db.manual_enter()

        expected_records = [{'date': '2020-11-22',
                             'time': '12:00:14',
                             'location': 'my_room',
                             'nodeID': 'lightclapper_21',
                             'lightStatus': c.OFF_INT},
                            {'date': '2020-11-22',
                             'time': '12:00:15',
                             'location': 'my_room',
                             'nodeID': 'lightclapper_21',
                             'lightStatus': c.ON_INT}]

        retrieved_records = self.__db.get_records()
        err_msg = 'Retrieved and expected records do not match'
        self.assertEqual(retrieved_records, expected_records, err_msg)


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()
