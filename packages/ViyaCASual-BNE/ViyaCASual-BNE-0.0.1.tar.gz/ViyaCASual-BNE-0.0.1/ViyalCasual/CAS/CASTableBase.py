import pandas as pd


class CASTableBase(object):
    source_sql = None
    source_data = None
    source_cas = None
    source_caslib = None

    cas_table_name = None
    caslib = None

    decision_source = None
    decision = None

    db_conn = None
    clean_up = False

    def __init__(self, viya_conn, db_conn=None):
        self.viya_conn = viya_conn
        self.register_db_connection(db_conn)
        self.set_decision_source()

    def __del__(self):
        if self.clean_up:
            self.remove_from_cas()

    def register_db_connection(self, db_conn):
        self.db_conn = db_conn

    def set_decision_source(self):

        if self.decision_source is None:
            return

        module_obj = __import__('CAS')
        if hasattr(module_obj, self.decision_source):
            decision_module = getattr(module_obj, self.decision_source)
            self.decision = decision_module(self.db_conn, self.viya_conn)

    def remove_from_cas(self):
        try:
            self.viya_conn.drop_cas_table(self.cas_table_name, self.caslib)
        except:
            pass

    def update_from_records(self, records):
        self.viya_conn.update_cas_table(records, self.cas_table_name, self.caslib)

    def update_from_source(self):
        self.update_from_records(self.get_source_data())

    def get_source_data(self):

        if self.source_data is not None:
            return self.source_data

        self.pre_process_source_data()

        if self.source_cas and self.source_caslib:
            self.source_data = self.viya_conn.get_cas_table(self.source_cas, self.source_caslib)
        elif self.decision_source:
            self.decision.exec()
            self.source_data = self.viya_conn.get_cas_table(self.cas_table_name, self.caslib)
        else:
            if self.source_sql is not None:
                self.source_data = self.read_sql(self.source_sql, True)

        try:
            self.source_data.drop(['index'], axis=1, inplace=True)
        except KeyError:
            pass
        except IndexError:
            pass

        self.source_data = pd.DataFrame().from_records(self.source_data.to_records())
        self.post_process_source_data()

        return self.source_data

    def pre_process_source_data(self):
        pass

    def post_process_source_data(self):
        pass

    def get_from_cas(self):
        return self.viya_conn.get_cas_table(self.cas_table_name, self.caslib)

    def read_sql(self, sql, clear_index=False):
        self.__check_db_conn()
        if clear_index:
            return pd.read_sql_query(sql, self.db_conn.conn, index_col=None)
        else:
            return pd.read_sql_query(sql, self.db_conn.conn)

    def __check_db_conn(self):
        if self.db_conn is None:
            raise Exception('Please register a valid DB connection before using this method')
