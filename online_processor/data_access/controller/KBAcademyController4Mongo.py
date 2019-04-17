from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice
from data_access.models.KB_Academy import kb_academy
from settings import mongo_db


@DataMap(_schema=mongo_db, _table="kb_academy")
class KBAcademyController4Mongo(BaseMongoController):
    @return_type(kb_academy)
    def get_datas_order_by(self, sort_by="", ascending=-1, page=1, size=10):
        return mgservice.query_sort(None, self._table, self._schema, sort_by, ascending, page, size)

    @return_type(kb_academy)
    def count_tag(self, tag_column, cond=None):
        return mgservice.count_tag(tag_column, self._schema, self._table, cond=cond)

    @return_type(kb_academy)
    def get_data_by_name(self, name):
        return mgservice.query({"schoolName": name}, self._schema, self._table)
