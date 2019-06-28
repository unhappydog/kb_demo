from core.processors.cv_processor import cvProcessor
from core.base.BaseTask import BaseTask
from data_access.controller.CommonController4Mongo import CommonController4Mongo
from services.tool_services.neo_service import NeoService
from utils.Constants import is_bad_column, is_replicate_column, cv_label
from core.linker.Searcher import Searcher
import pandas as pd
import re


neoService = NeoService.instance()
@cvProcessor.add_as_processors(order=11, stage=2, schema='kb_graph', table='kb_graph_news_processed')
class SaveTask(BaseTask):
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.controller = CommonController4Mongo(schema, table)


    def fit(self, data):
        self.controller.insert_datas_from_df(data)
        return data

@cvProcessor.add_as_processors(order=12, stage=2)
class ExtractTask(BaseTask):
    def __init__(self):
        self.linker = Linker()

    def fit(self, data):
        data = data[data.apply(lambda x: x[is_bad_column] ==0 and x[is_replicate_column] ==0 , axis=1)]
        # humans = data.apply(lambda x: x[['age', 'birthday', '']])
        return data

    def ontology_and_relation(self, x):
        neoService.create(c)
