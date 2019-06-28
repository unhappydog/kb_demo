from core.processors.cv_processor import cvProcessor
from core.base.BaseTask import BaseTask
from data_access.controller.CommonController4Mongo import CommonController4Mongo
import re


@cvProcessor.add_as_processors(order=11, stage=2, schema='kb_graph', table='kb_graph_cv_processed')
class SaveTask(BaseTask):
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.controller = CommonController4Mongo(schema, table)


    def fit(self, data):
        self.controller.insert_datas_from_df(data)
        return data
