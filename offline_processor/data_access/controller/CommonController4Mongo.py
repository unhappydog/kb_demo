from services.tool_services.MongoService import mgService
from data_access.base.BaseMongoController import BaseMongoController
from utils.Logger import logging

class CommonController4Mongo(BaseMongoController):
    def __init__(self, schema, table):
        self._table = table
        self._schema = schema
