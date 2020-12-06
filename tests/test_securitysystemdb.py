#!/usr/bin/env python3
"""
SecuritySystemDB tests
"""
import logging
import os
from unittest import TestCase, main, skipIf
from sqliteDB import SecuritySystemDB
import constants as c

TEMP_DB = 'temp_securitysystem.db'
TEMP_TABLE = 'temp_securitysystem'
PREMADE_DB = 'tests/test_db/temp_securitysystem.db'
PREMADE_TABLE = 'temp_securitysystem'

class TestLightClapperDB(TestCase):
    """
    Test methods for SecuritySystemDB
    Attributes
    ----------
    __db: SecuritySystemDB
        DB being test
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
        Setup TestSecuritySystemDB
        """
        self.__db = SecuritySystemDB(db_file=TEMP_DB,
                                     name=TEMP_TABLE)
        self.__db.manual_enter()

    def tearDown(self):
        """
        Teardown TestSecuritySystemDB
        """
        self.__db.manual_exit()
        if os.path.exists(TEMP_DB):
            os.remove(TEMP_DB)

    def test_create_table(self):
        """
        Test creating new table that doesn't exist
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
        record = {'date': '2020-11-23',
                  'time': '23:06:34',
                  'location': 'test_room',
                  'nodeID': 'securitysystem_34'}

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
        record = {'date': '2020-11-23',
                  'time': '23:06:34',
                  'nodeID': 'securitysystem_34'}

        self.__db.create_table()
        err_msg = 'Record exists unexpectedly'
        self.assertFalse(self.__db.record_exists(record), err_msg)

        self.assertRaises(Exception, self.__db.add_record, record)

    @skipIf(not os.path.exists(PREMADE_DB), 'Run test in top level directory')
    def test_get_records(self):
        """
        Test retrieving pre-determined records from DB.
        """
        self.__db = SecuritySystemDB(db_file=PREMADE_DB,
                                   name=PREMADE_TABLE)
        self.__db.manual_enter()

        expected_records = [{'date': '2020-11-24',
                             'location': 'hasan_bedroom',
                             'nodeID': 'securitysystem_19',
                             'time': '19:07:13'},
                            {'date': '2020-11-22',
                             'location': 'hasan_bedroom',
                             'nodeID': 'securitysystem_19',
                             'time': '12:00:15'}]

        retrieved_records = self.__db.get_records()
        err_msg = 'Retrieved and expected records do not match'
        self.assertEqual(retrieved_records, expected_records, err_msg)


if __name__ == '__main__':
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_TEST_LEVEL)
    main()