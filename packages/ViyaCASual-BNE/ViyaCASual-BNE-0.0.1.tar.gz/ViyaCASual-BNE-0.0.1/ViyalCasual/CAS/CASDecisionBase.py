import pandas as pd
from swat.cas.table import CASTable
from uuid import uuid4


class CASDecisionBase(object):
    model_lib = None
    model_table_name = None

    rule_name = None
    rule_version_name = None

    input_table_name = str(uuid4())
    output_table_name = str(uuid4())

    details = None

    inputs = list()
    outputs = list()

    def __init__(self, viya_conn, db_conn=None):
        self.warehouse = db_conn
        self.viya = viya_conn
        self.viya.conn.loadactionset('ds2')
        self.viya.conn.loadactionset('table')

    def set_details(self):
        self.details = self.viya.get_model_details(self.rule_name)
        self.__set_required_inputs_outputs()
        self.__set_latest_release()

    def __set_required_inputs_outputs(self):
        [self.register_columns(x) for x in self.details['flow']['steps']]

    def __set_latest_release(self):
        self.rule_version_name = '%s%s_%s' % (self.details['name'], self.details['majorRevision'], self.details['minorRevision'])

    def register_columns(self, value):
        for x in value['mappings']:
            if 'IN' in str(x['direction']).upper() and x['targetDecisionTermName'] not in self.inputs:
                self.inputs.append(x['targetDecisionTermName'])
            if 'OUT' in str(x['direction']).upper() and x['targetDecisionTermName'] not in self.outputs:
                self.outputs.append(x['targetDecisionTermName'])

    def exec(self):
        self.__run_model()

    def get_results(self):
        return pd.DataFrame(self.viya.conn.CASTable(self.output_table_name).to_records(index=False))

    def set_input(self, data):
        CASTable.from_records(self.viya.conn, data, casout={'name': self.input_table_name})

    # Run the Business Rule / Decision / Model against set input table
    # Promote output table for global use.
    def __run_model(self):
        self.viya.conn.ds2.runModel(
            modelName=self.rule_version_name,
            table={'name': self.input_table_name},
            modelTable={'caslib': self.model_lib, 'name': self.model_table_name},
            casOut={'name': self.output_table_name}
        )
