"""
sqliteDB.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import abc
import sqlite3
import logging
import argparse
import os
import constants as c

FIRST_ROW = 0
SINGLE_RECORD = 1


class SqliteDB(metaclass=abc.ABCMeta):
    """"
    DB to store data

    Attributes
    ----------
    _db_file : str
        file name of sqlite DB file
    _name : str
        name of DB
    _dbconnect : Connection
        sqlite connection object
    _cursor : Cursor
        cursor to perform SQL commands

    Methods
    -------
    manual_enter()
        manually perform context manager entry
    manual_exit()
        manually perform context manager exit
    table_exists()
        Check if table exists
    create_table()
        Abstract method to create table
    add_record(record)
        Abstract method to add record
    record_exists(record)
        Abstract method to check if record exists
    get_records()
        Abstract method to get records
    """

    def __init__(self, db_file, name):
        """
        Initialize SqliteDatabase Context Manager

        Parameters
        ----------
        db_file : str
            file name of sqlite DB file
        name : str
            name of DB
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

        Parameters
        ----------
        exception : type
        value
        trace : traceback
        """
        self.manual_exit()

    def manual_enter(self):
        """
        Performs steps in entry
        Available for manual use as per Facade pattern
        """
        self._dbconnect = sqlite3.connect(self._db_file)

        # Set row_factory to access columns by name
        self._dbconnect.row_factory = sqlite3.Row

        # Create a cursor to work with the db
        self._cursor = self._dbconnect.cursor()

    def manual_exit(self):
        """
        Performs steps in exit
        Available for manual use as per Facade pattern
        """
        self._dbconnect.commit()
        self._dbconnect.close()
        self._dbconnect = None
        self._cursor = None

    def table_exists(self):
        """
        Check if DB exists

        Returns
        -------
        table_exists : bool
            True if DB exists
        """
        # Check if table already exists
        self._cursor.execute("SELECT count(name) FROM sqlite_master WHERE \
                       type='table' AND name='{}'".format(self._name))

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


class LightClapperDB(SqliteDB):
    """
    DB for Light Clapper node

    Methods
    -------
    create_table()
        Creates a LightClapperDB table
    add_record(record)
        Adds entry to LightClapperDB table
    record_exists(record)
        Check if entry already exists in LightClapperDB
    get_records()
        Get all records from Table
    """

    def __init__(self, db_file=c.LIGHT_CLAPPER_DB_FILE,
                 name=c.LIGHT_CLAPPER_TABLE):
        """
        Initialize LightClapperDB

        Parameters
        ----------
        db_file : str
            file name of sqlite DB file
        name : str
            name of DB
        """
        super().__init__(db_file, name)

    def create_table(self):
        """
        Create table for LightClapperDB

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        """
        logging.debug('Creating new table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        self._cursor.execute(
            "create table {} (date text, \
             time text, location text, nodeID text, \
             lightStatus integer)".format(self._name))

    def add_record(self, record):
        """
        Add entry to LightClapperDB table

        Parameters
        ----------
        record : dict
            Entry to add to DB

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        Exception
            Invalid LightClapperDB record
        """
        logging.debug('Adding new entry to table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        date = record.get('date', '')
        time = record.get('time', '')
        location = record.get('location', '')
        node_id = record.get('nodeID', '')
        light_status = record.get('lightStatus', '')

        if '' in (date, time, node_id, location, light_status):
            raise Exception('Invalid LightClapperDB record!')

        self._cursor.execute(
            "insert into {} values(?, ?, ?, ?, ?)".format(self._name),
            (date, time, location, node_id, light_status))

    def record_exists(self, record):
        """
        Check if entry exists in LightClapper DB table

        Parameters
        ----------
        record : dict
            Entry to add to DB

        Returns
        -------
        record_exists : bool
            True if entry exists

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        """
        record_exists = False

        logging.debug('Check if record exists in table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        date = record.get('date', '')
        time = record.get('time', '')
        location = record.get('location', '')
        node_id = record.get('nodeID', '')
        light_status = record.get('lightStatus', '')

        self._cursor.execute(
            """SELECT count(*) FROM {} WHERE \
                date == ? and time = ? and location = ? and nodeID = ? \
                and lightStatus = ?""".format(self._name),
            (date, time, location, node_id, light_status))

        if self._cursor.fetchone()[FIRST_ROW] == SINGLE_RECORD:
            record_exists = True

        logging.debug('Record exists? : {}'.format(record_exists))
        return record_exists

    def get_records(self):
        """
        Return all records in table

        Returns
        -------
        records : list
            all records in Table
        """
        logging.debug('Get records from table')
        records = []
        self._cursor.execute("SELECT * FROM {}".format(self._name))
        rows = self._cursor.fetchall()

        for r in rows:
            record = {'date': r['date'],
                      'time': r['time'],
                      'location': r['location'],
                      'nodeID': r['nodeID'],
                      'lightStatus': r['lightStatus']}
            records.append(record)

        return records


def records_to_string(records):
    """
    Helper function:
    Make a string based on records that are passed in

    Parameters
    ----------
    records : list
        List of records read from DB

    Returns
    -------
    records_str : str
        String representation of records from DB
    """
    records_str = '  date|time|location|nodeID|lightStatus'
    for r in records:
        records_str += '\n  {}|{}|{}|{}|{}'.format(
            r.get('date', ''),
            r.get('time', ''),
            r.get('location', ''),
            r.get('nodeID', ''),
            r.get('lightStatus', ''))

    return records_str


def light_clapper_db_test(file_name, table_name, location, node_id):
    """
    Creates a LightClapperDB object for manual
    db verification

    Parameters
    ----------
    file_name : str
        Name of test DB file
    table : str
        Name of test DB table
    location : str
        Name of test location
    node_id : str
        Name of test node ID
    """
    default_date = '2020-11-21'
    default_time_1 = '20:05:45'
    default_time_2 = '23:15:30'

    records = [{'date': default_date,
                'time': default_time_1,
                'location': location,
                'nodeID': node_id,
                'lightStatus': c.ON_INT},
               {'date': default_date,
                'time': default_time_2,
                'location': location,
                'nodeID': node_id,
                'lightStatus': c.OFF_INT}]

    info_str = 'Attempting to add the following data...\n'
    info_str += records_to_string(records)
    logging.info(info_str)

    with LightClapperDB(db_file=file_name, name=table_name) as db_obj:
        logging.info('Checking & creating table if needed')
        if not db_obj.table_exists():
            db_obj.create_table()

        logging.info('Adding only the new records to table')
        for r in records:
            if not db_obj.record_exists(r):
                db_obj.add_record(r)

        logging.info('Retrieving all records')
        records = db_obj.get_records()
        records_str = records_to_string(records)
        logging.info('Read records:\n{}'.format(records_str))

    logging.info('Open {cwd}/{f} in SQL Browser for verification'.format(
        cwd=os.getcwd(), f=file_name))


def parse_args():
    """
    Parses arguments for manual operation of the LightClapperDB

    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    default_file_name = 'test.db'
    default_table_name = 'test'
    default_location = 'my_room'
    default_node_id = 'lightclapper_123'

    parser = argparse.ArgumentParser(
        description='Run the LightClapperDB test program')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    parser.add_argument('-lc',
                        '--light_clapper',
                        default=False,
                        action='store_true',
                        help='Run LightClapperDB test')

    parser.add_argument('-f',
                        '--file_name',
                        type=str,
                        default=default_file_name,
                        metavar='<file_name.db>',
                        help='Specify file name of SQL db (Relative to pwd)')

    parser.add_argument('-t',
                        '--table_name',
                        type=str,
                        default=default_table_name,
                        metavar='<test_table_name>',
                        help='Specify table name of SQL db')

    parser.add_argument('-l',
                        '--location',
                        type=str,
                        default=default_location,
                        metavar='<owner_room>',
                        help='Specify owner and room')

    parser.add_argument('-id',
                        '--node_id',
                        type=str,
                        default=default_node_id,
                        metavar='<node_id>',
                        help='Specify node ID')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    if args.light_clapper:
        light_clapper_db_test(
            args.file_name,
            args.table_name,
            args.location,
            args.node_id)
