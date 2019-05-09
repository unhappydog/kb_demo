from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice


@DataMap(_schema="kb_demo", _table="kb_talent_bank")
class KBTalentBankController4Mongo(BaseMongoController):
    def get_datas_order_by(self, sort_by="updateTime", ascending=-1, page=1, size=10, mode=None):
        if not mode:
            cond = None
        else:
            cond = {"source_method": mode}
        return mgservice.query_sort(cond, self._table, self._schema, sort_by, ascending, page, size)

    def count_tag(self, tag_column, cond=None):
        return mgservice.count_tag(tag_column, self._schema, self._table, cond=cond)

    def get_datas_by_keyword(self, keyword="", sort_by="updateTime", ascending=-1, page=1, size=10, mode=None):
        if not mode:
            cond = {
                "keyword": keyword
            }
        else:
            cond = {
                "keyword": keyword,
                "source_method": mode
            }
        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)

    def get_datas_by_education(self, education="", sort_by="updateTime", ascending=-1, page=1, size=10, mode=None):
        if not mode:
            cond = {
                "highestEducationDegree": education,
            }
        else:
            cond = {
                "highestEducationDegree": education,
                "source_method": mode
            }

        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)

    def get_datas_by_source(self, source="", sort_by="updateTime", ascending=-1, page=1, size=10, mode=None):
        if not mode:
            cond = {"source": source}
        else:
            cond = {"source": source,
                    "source_method": mode}

        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)

    def get_datas_by(self, cond, sort_by="updateTime", ascending=-1, page=1, size=10):
        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)


if __name__ == '__main__':
    controller = KBTalentBankController4Mongo()
    # controller.get_datas_order_by("")
    # controller.delete_by_id("")
    print(controller.get_datas())
