"""
db.py
TODO: move to database folder later
"""
import abc
import sqlite3
import logging


LIGHT_CLAPPER_DB = 'lightclapper.db'
LIGHT_CLAPPER_NAME = 'LightClapper'


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


class LightDB(SqliteDB):
    """
    DB for Light Clapper node

    Methods
    -------
    create_table()
        Creates a LightClapperDB table
    add_record()
        Adds entry to LightClapperDB table
    record_exists()
        Check if entry already exists in LightClapperDB
    get_records()
        Get all records from Table
    """

    def __init__(self, db_file=LIGHT_CLAPPER_DB, name=LIGHT_CLAPPER_NAME):
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
        """
        logging.debug('Creating new table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')
        self._cursor.execute("create table {} (date text, \
                         time text, lightStatus integer) \
                         ".format(self._name))

    def add_record(self, record):
        """
        Add entry to LightClapperDB table

        Parameters
        ----------
        record : dict
            Entry to add to DB
        """
        logging.debug('Adding new entry to table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        self._cursor.execute("insert into {} values(?, ?, ?)".format(
            self._name),
            (record['date'], record['time'], record['lightStatus']))

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
        """
        logging.debug('Check if record exists in table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        date = record['date']
        time = record['time']
        light_status = record['lightStatus']

        self._cursor.execute("""SELECT count(*) FROM {} WHERE \
             date == ? and time = ? and lightStatus = ?""".format(self._name),
                             (date, time, light_status))

        record_exists = True if self._cursor.fetchone()[0] == 1 else False

        logging.debug('Record exists? : {}'.format(record_exists))
        return record_exists

    def get_records(self):
        """
        Return all records in table

        TODO: might not be needed

        Returns
        -------
        records : dict
            all records in Table
        """
        # TODO
        pass


def light_clapper_db_test():
    """
    Creates a LightClapperDB object for manual
    db verification
    """
    with LightDB(db_file='test.db', name='test') as db_obj:
        record = {'date': 'fake_date',
                  'time': 'fake_time',
                  'lightStatus': 1}

        if not db_obj.table_exists():
            db_obj.create_table()

        if not db_obj.record_exists(record):
            db_obj.add_record(record)

    # TODO: add more verification

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    light_clapper_db_test()
