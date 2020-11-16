import abc
import sqlite3
import logging
from datetime import datetime

TEMP_SENSOR_DB = "tempsensor.db"
TEMP_SENSOR_NAME = "TempSensor"

class SqliteDB(metaclass=abc.ABCMeta):
	def __init__(self, db_file, name):
		self._db_file = db_file
		self._name = name
		self._dbconnect = None
		self._cursor = None

	def __enter__(self):
		self.manual_enter()
		return self

	def __exit__(self, exception, value, trace):
		self.manual_exit()

	def manual_enter(self):
		self._dbconnect = sqlite3.connect(self._db_file)
		self._dbconnect.row_factory = sqlite3.Row
		self._cursor = self._dbconnect.cursor()

	def manual_exit(self):
		self._dbconnect.commit()
		self._dbconnect.close()
		self._dbconnect = None
		self._cursor = None

	def table_exists(self):
		self._cursor.execute("SELECT count(name) FROM sqlite_master WHERE \
			       type = 'table' AND name = '{}'".format(self._name))

		table_exists = True if self._cursor.fetchone()[0] == 1 else False
		return table_exists

	@abc.abstractmethod
	def create_table(self):
		pass

	@abc.abstractmethod
	def add_record(self, record):
		pass

	@abc.abstractmethod
	def record_exists(self, record):
		pass

	@abc.abstractmethod
	def get_records():
        	pass


class TempDB(SqliteDB):
	def __init__(self, db_file=TEMP_SENSOR_DB, name=TEMP_SENSOR_NAME):
        	super().__init__(db_file, name)

	def create_table(self):
		logging.debug('Creating new table')
		if not self._dbconnect or not self._cursor:
	            raise Exception('Invalid call to Context Manager method!')
		self._cursor.execute("Create Table {} (date text, time text, fanStatus integer)".format(self._name))

	def add_record(self, record):
		logging.debug('Adding new entry to table')
		if not self._dbconnect or not self._cursor:
			raise Exception('Invalid call to context Manager method!')

		self._cursor.execute("Insert into {} values(?, ?, ?)".format(
		     self._name),
		     (record['date'], record['time'], record['fanStatus']))

	def record_exists(self, record):
		logging.debug('Check if record exists in table')
		if not self._dbconnect or not self._cursor:
			raise Exception('Invalid call to Context Manager method!')

		date = record['date']
		time = record['time']
		fan_status = record['fanStatus']

		self._cursor.execute("""SELECT count(*) FROM {} WHERE \
	             date == ? and time = ? and fanStatus = ?""".format(self._name), (date, time, fan_status))

		record_exists = True if self._cursor.fetchone()[0] == 1 else False

		logging.debug('Record exists : {}'.format(record_exists))
		return record_exists

	def get_records(self):
		logging.debug("Return all records in table")
		if not self._dbconnect or not self._cursor:
			raise Exception("Invalid call to Context Manager method!")

		self._cursor.execute("""SELECT * FROM {}""".format(self._name))

		for row in self._cursor:
			print(row['date'], row['time'], row['fanStatus'])

def temp_sensor_db_test():
	with TempDB(db_file='test.db', name='test') as db_obj:
		record = {'date': 'fake_date',
			  'time': 'fake_time',
			  'fanStatus': 1}

		if not db_obj.table_exists():
			db_obj.create_table()

		if not db_obj.record_exists(record):
			db_obj.add_record(record)

		db_obj.get_records()

if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level = logging.DEBUG)
	temp_sensor_db_test()

