from ViyalCasual.CAS.CASTableBase import CASTableBase
from ViyalCasual.CAS.CASDecisionBase import CASDecisionBase
from ViyalCasual.Viya.ViyaConnection import ViyaConnection, ViyaConnectionParams


class CAS(object):

    url = None
    user_name = None
    password = None
    port = 5570
    db_conn = None
    default_decision_lib = None
    default_decision_table = None

    viya = None
    table_base = None
    decision_base = None

    def __init__(self, server, username, password, db_conn, port=5570):
        self.url = server
        self.user_name = username
        self.password = password
        self.port = port
        self.setup(db_conn)

    def setup(self, db_conn):
        self.db_conn = db_conn
        self.viya = ViyaConnection(self.__register_viya_connection())
        self.table_base = CASTableBase(self.viya, self.db_conn)
        self.decision_base = CASDecisionBase(self.viya, self.db_conn)

    def __register_viya_connection(self):
        conn = ViyaConnectionParams()
        conn.url = self.url
        conn.port = self.port
        conn.user_name = self.user_name
        conn.password = self.password
        return conn