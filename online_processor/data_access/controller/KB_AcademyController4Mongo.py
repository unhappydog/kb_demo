from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.MongoService import mgservice


@DataMap(_schema="kb_demo", _table="kb_academy")
class KB_AcademyController4Mongo(BaseMongoController):
    def get_datas_order_by(self, sort_by="", ascending=-1, page=1, size=10):
        return mgservice.query_sort(None, self._table, self._schema, sort_by, ascending, page, size)

    def count_tag(self, tag_column, cond=None):
        return mgservice.count_tag(tag_column, self._schema, self._table, cond=cond)
