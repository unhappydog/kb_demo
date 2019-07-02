from core.processors.news_processor import newsProcessor
from core.base.BaseTask import BaseTask
from data_access.controller.CommonController4Mongo import CommonController4Mongo
import re


@newsProcessor.add_as_processors(order=11, stage=2, schema='kb_demo', table='kb_news')
class SaveTask(BaseTask):
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.controller = CommonController4Mongo(schema, table)


    def fit(self, data):
        self.controller.insert_datas_from_df(data)
        return data
