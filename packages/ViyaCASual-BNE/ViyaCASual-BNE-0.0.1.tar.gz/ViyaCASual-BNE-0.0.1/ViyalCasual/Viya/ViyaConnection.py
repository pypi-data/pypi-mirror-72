import swat
import sasctl
import json
from ViyalCasual.Viya import ViyaConnectionExceptions


class ViyaConnectionParams(object):
    url = None
    user_name = None
    password = None
    port = 5570


class ViyaConnection(object):
    conn = None
    crl = None
    auto_connect = True

    def __init__(self, conn_parameters=ViyaConnectionParams()):
        self.swat = swat

        self.url = conn_parameters.url
        self.port = conn_parameters.port
        self.user_name = conn_parameters.user_name
        self.password = conn_parameters.password

        if self.url is None:
            raise ViyaConnectionExceptions.ViyaConfigURL()
        if self.port is None:
            raise ViyaConnectionExceptions.ViyaConfigPort()
        if self.user_name is None:
            raise ViyaConnectionExceptions.ViyaConfigUserName()
        if self.password is None:
            raise ViyaConnectionExceptions.ViyaConfigPassword()

        if self.auto_connect:
            try:
                self.conn = swat.CAS(self.url, self.port, self.user_name, self.password)
            except:
                raise ViyaConnectionExceptions.ViyaSWATConnection()

            try:
                self.ctl = sasctl.Session(self.url, self.user_name, self.password)
            except:
                raise ViyaConnectionExceptions.ViyaSASCTLConnection()

    def increase_row_download_limit(self, limit):
        self.swat.set_option('cas.dataset.max_rows_fetched', limit)

    def get_server_status(self):
        return self.conn.serverstatus()

    def get_cas_table(self, table_name, caslib_name=None):
        return self.conn.CASTable(name=table_name, caslib=caslib_name)

    def drop_cas_table(self, table_name, caslib_name=None):
        table = self.conn.CASTable(name=table_name, caslib=caslib_name)
        table.dropTable()

    def update_cas_table(self, records, table_name, caslib_name=None):
        try:
            self.drop_cas_table(table_name, caslib_name)
        except:
            pass

        self.swat.cas.table.CASTable.from_records(self.conn, records,
                                             casout={'name': table_name,
                                                     'caslib': caslib_name,
                                                     'promote': True})

    def get_model_details(self, model_name):
        model_url = None
        returns = self.ctl.get('/decisions/flows')
        text = json.loads(returns.text)
        for link in text['items']:
            if str(link['name']).upper() == str(model_name).upper():
                model_url = '/decisions/flows/%s' % link['id']
                break
        if model_url is None:
            raise Exception('Unable to find decision')

        returns = self.ctl.get(model_url)
        return json.loads(returns.text)

    def get_latest_model_release(self, model_name):
        model_info = self.get_model_details(model_name)
        return '%s%s_%s' % (model_info['name'], model_info['majorRevision'], model_info['minorRevision'])
