from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice


@DataMap(_schema="kb_demo", _table="CV")
class CVController4Mongo(BaseMongoController):
    def get_datas_order_by(self, sort_by="", ascending=-1, page=1, size=10):
        return mgservice.query_sort(None, self._table, self._schema, sort_by, ascending, page, size)

    def count_tag(self, tag_column, cond=None):
        return mgservice.count_tag(tag_column, self._schema, self._table, cond=cond)


if __name__ == '__main__':
    controller = CVController4Mongo()
    # controller.get_datas_order_by("")
    controller.delete_by_id("")
