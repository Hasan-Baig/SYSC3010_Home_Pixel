import logging
import os
from unittest import TestCase, main, skipIf
from tempDB import TempDB

TEMP_DB = 'temp_tempsensor.db'
TEMP_TABLE = 'temp_tempsensor'
PREMADE_DB = 'tests/test_db/test_tempsensor.db'
PREMADE_TABLE = 'test_tempsensor'

class TestTempDB(TestCase):
	def setUp(self):
		self.__db = TempDB(db_file = TEMP_DB, name = TEMP_TABLE)
		self.__db.manual_enter()

	def tearDown(self):
		self.__db.manual_exit()
		if os.path.exists(TEMP_DB):
			os.remove(TEMP_DB)

	def test_create_table(self):
		error_msg = 'Table already exists'
		self.assertFalse(self.__db.table_exists(), error_msg)

		self.__db.create_table()
		error_msg ='Table does not exist'
		self.assertTrue(self.__db.table_exists(), error_msg)

	def test_add_good_record(self):
		record = {'date': '2020-11-22',
			  'time': '13:51:42',
			  'location': 'test_locattion',
			  'nodeID': 'test_node1',
		  	  'fanStatus': 1,
			  'tempVal': 24.3}

		self.__db.create_table()
		error_msg = 'Record exists unexpectedly'
		self.assertFalse(self.__db.record_exists(record), error_msg)

		self.__db.add_record(record)
		error_msg = "Record failed to be added to DB table"
		self.assertTrue(self.__db.record_exists(record), error_msg)

	def test_add_bad_record(self):
		record = {'date': '2020-11-22',
			  'time': '14:11:34',
			  'fanStatus': 1}

		self.__db.create_table()
		error_msg = 'Record exists unexpectedly'
		self.assertFalse(self.__db.record_exists(record), error_msg)

#		self.assertRaises(Exception, self.__db.add_record, record)

	@skipIf(not os.path.exists(PREMADE_DB), 'Run test in top level directory')
	def test_get_records(self):
		self.__db = TempDB(db_file = PREMADE_DB, name = PREMADE_TABLE)
		self.__db.manual_enter()

		expected_records = [{'date': '2020-11-22',
			    	     'time': '14:23:34',
			     	     'fanStatus': 0},
			    	    {'date': '2020-11-22',
			     	     'time': '14:24:43',
			     	     'fanStatus': 1}]

		retrieved_records = self.__db.get_records()
		error_msg = 'Retreived and expected records do not match'
		self.assertEqual(retrieved_records, expected_records, error_msg)

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level = logging.DEBUG)
	main()
