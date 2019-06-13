from data_access.base.BaseMongoController import BaseMongoController
from utils.MongoMapTags import DataMap, query, query_as_gen


@DataMap(_schema='kb_demo', _table='kb_weixin')
class WeixinController4Mongo(BaseMongoController):
    pass