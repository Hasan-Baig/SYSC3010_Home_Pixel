import abc
import sqlite3
import logging
import argparse
import os
import thingspeakinfo as c
from datetime import datetime

FIRST_ROW = 0
SINGLE_RECORD = 1

class SqliteDB(metaclass=abc.ABCMeta):
	"""
	DB to store data
	"""

	def __init__(self, db_file, name):
		"""
		Initializes TempDB Context Manager
		"""

		self._db_file = db_file
		self._name = name
		self._dbconnect = None
		self._cursor = None

	def __enter__(self):
		"""
		DB context manager entry
		"""
		self.manual_enter()
		return self

	def __exit__(self, exception, value, trace):
		"""
		DB context manager exit
		"""
		self.manual_exit()

	def manual_enter(self):
		self._dbconnect = sqlite3.connect(self._db_file)
		self._dbconnect.row_factory = sqlite3.Row #Set row_factory to access columns by name
		self._cursor = self._dbconnect.cursor() #Create a cursor to work with the db

	def manual_exit(self):
		self._dbconnect.commit()
		self._dbconnect.close()
		self._dbconnect = None
		self._cursor = None

	def table_exists(self):
		"""
		Checking if table exists
		"""

		#Checking if table already exists
		self._cursor.execute("SELECT count(name) FROM sqlite_master WHERE \
			       type = 'table' AND name = '{}'".format(self._name))

		if self._cursor.fetchone()[FIRST_ROW] == SINGLE_RECORD:
			table_exists = True
		else:
			table_exists = False

		logging.debug('Table exists? : {}'.format(table_exists))
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
	"""
	Database for TempDB node
	"""

	def __init__(self, db_file=c.TEMP_SENSOR_DB_FILE, name=c.TEMP_SENSOR_TABLE):
        	super().__init__(db_file, name)

	def create_table(self):
		"""
		Creating a table for TempSensorDB
		"""

		logging.debug('Creating new table')
		if not self._dbconnect or not self._cursor:
	            raise Exception('Invalid call to Context Manager method!')

		#Storing a table with the fields date / time / location / nodeID / fanStatus / temperature value
		self._cursor.execute(
			"create table {} (date text, \
			 time text, location text, nodeID text, \
			 fanStatus integer, tempVal float)".format(self._name))

	def add_record(self, record):
		"""
		Adding data to the TempSensorDB Table
		"""

		logging.debug('Adding new entry to table')
		if not self._dbconnect or not self._cursor:
			raise Exception('Invalid call to context Manager method!')

		#Fields being stored
		date = record.get('date', '')
		time = record.get('time', '')
		location = record.get('location', '')
		node_id = record.get('nodeID', '')
		fan_status = record.get('fanStatus', '')
		temp_val = record.get('tempVal', '')

		if '' in (date, time, node_id, location, fan_status, temp_val):
			raise Exception('Invalid TempSensorDB record!')

		self._cursor.execute(
			"insert into {} values(?, ?, ?, ?, ?, ?)".format(self._name),
			(date, time, location, node_id, fan_status, temp_val))

	def record_exists(self, record):
		"""
		Checking if records exist already in the table
		"""

		record_exists = False

		logging.debug('Check if record exists in table')
		if not self._dbconnect or not self._cursor:
			raise Exception('Invalid call to Context Manager method!')

		date = record.get('date', '')
		time = record.get('time', '')
		location = record.get('location', '')
		node_id = record.get('nodeID', '')
		fan_status = record.get('fanStatus', '')
		temp_val = record.get('tempVal', '')

		self._cursor.execute(
			"""SELECT count(*) FROM {} WHERE \
				date == ? and time = ? and location = ? and nodeID = ? \
				and fanStatus = ? and tempVal = ?""".format(self._name), (date, time, location, node_id, fan_status, temp_val))

		if self._cursor.fetchone()[FIRST_ROW] == SINGLE_RECORD:
			record_exists = True

		logging.debug('Record exists? : {}'.format(record_exists))
		return record_exists

	def get_records(self):
		"""
		Returning all records in Table
		"""

		logging.debug("Return all records in table")
		records = []
		self._cursor.execute("SELECT * FROM {}".format(self._name))
		rows = self._cursor.fetchall()

		for r in rows:
			record = {'date': r['date'],
				  'time': r['time'],
				  'location': r['location'],
				  'nodeID': r['nodeID'],
				  'fanStatus': r['fanStatus'],
				  'tempVal': r['tempVal']}
			records.append(record)

		return records

def records_to_string(records):
	records_str = '    date|time|location|nodeID|fanStatus|tempVal'
	for r in records:
		records_str += '\n    {}|{}|{}|{}|{}|{}'.format(
			r.get('date', ''),
			r.get('time', ''),
			r.get('location', ''),
			r.get('nodeID', ''),
			r.get('fanStatus', ''),
			r.get('tempVal', ''))

	return records_str

def temp_sensor_db_test(file_name, table_name, location, node_id):

	default_date = '2020-11-21'
	default_time_1 = '14:35:32'
	default_time_2 = '23:12:45'
	default_temp_val = 23.2
	default_temp_val_2 = 43.2

	records = [{'date': default_date,
		    'time': default_time_1,
		    'location': location,
		    'nodeID': node_id,
		    'fanStatus': 1,
		    'tempVal': default_temp_val},
		   {'date': default_date,
		    'time': default_time_2,
		    'location': location,
		    'nodeID': node_id,
		    'fanStatus': 0,
		    'tempVal': default_temp_val_2}]

	info_str = 'Attempting to add the following data ...\n'
	info_str += records_to_string(records)
	logging.info(info_str)

	with TempDB(db_file=file_name, name=table_name) as db_obj:
		logging.info('Checking & Creating table if needed')
		if not db_obj.table_exists():
			db_obj.create_table()

		logging.info('Adding only the new records to table')
		for r in records:
			if not db_obj.record_exists(r):
				db_obj.add_record(r)

		logging.info('Retrieving all records')
		record = db_obj.get_records()
		records_str = records_to_string(records)
		logging.info('Read records:\n{}'.format(records_str))

	logging.info('Open {cwd}/{f} in SQL Browser for verificaiton'.format(
		cwd=os.getcwd(), f=file_name))

def parse_args():
	default_file_name = 'test.db'
	default_table_name = 'test'
	default_location = 'my_room'
	default_node_id = 'tempsensor_123'

	parser = argparse.ArgumentParser(
		description = 'Run the TempSensorDB test program')

	parser.add_argument('-v',
			    '--verbose',
			    default = False,
			    action = 'store_true',
			    help = 'Print all debug logs')

	parser.add_argument('-tp',
			    '--temp_sensor',
			    default = False,
			    action = 'store_true',
			    help = 'Run TempSensorDB test')

	parser.add_argument('-f',
			    '--file_name',
			    type = str,
			    default = default_file_name,
			    metavar = '<file_name.db>',
			    help = 'Specify table name of SQL db')

	parser.add_argument('-l',
			    '--location',
			    type = str,
			    default = default_location,
			    metavar = '<owner_room>',
			    help = 'Specify owner and room')

	parser.add_argument('-id',
			    '--node_id',
			    type = str,
			    default = default_node_id,
			    metavar = '<node_id>',
			    help = 'Specify node ID')

	args = parser.parse_args()
	return args

if __name__ == "__main__":
	args = parse_args()
	logging_level = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(format = c.LOGGING_FORMAT, level = logging_level)

	if args.temp_sensor:
		temp_sensor_db_test(
			args.file_name,
			args.table_name,
			args.location,
			args.node_id)
	else:
		logging.error('No test DB specified')
