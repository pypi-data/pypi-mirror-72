import pandas as pd


class DataConnector(object):

    server = None
    username = None
    password = None
    driver = None
    database = None

    def __init__(self, database=None):
        self.database = database

    def read_sql(self, sql):
        return pd.read_sql(sql, self.conn)

    def execute_sql(self, sql, data=None):
        cursor = self.conn.cursor()
        if data is None:
            cursor.execute(sql)
        else:
            cursor.fast_executemany = True
            cursor.executemany(sql, data)
        cursor.commit()
        cursor.close()


class MSSQLConnector(DataConnector):

    def __init__(self, database='Warehouse'):
        import pyodbc
        connection_string = 'DRIVER=%s;SERVER=%s;PORT=1433;UID=%s;PWD=%s;Database=%s'
        connection_string = connection_string % (
            self.driver, self.server, self.username, self.password, database
        )
        self.conn = pyodbc.connect(connection_string)

    @staticmethod
    def execute_stored_proc(stored_proc, table='PollingStaging'):
        staging = MSSQLConnector(table)
        cursor = staging.conn.cursor()
        cursor.execute('EXEC dbo.%s' % stored_proc)
        cursor.commit()
        cursor.close()


class SqliteConnector(DataConnector):

    def __init__(self, database=None):
        import sqlite3
        self.conn = sqlite3.connect(database)