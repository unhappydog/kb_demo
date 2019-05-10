from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo


@DataMap(_schema="kb_demo", _table="kb_talent_bank")
class KBTalentBankController4Mongo(BaseMongoController):

    def __init__(self):
        self.keyword_dict = KBPostController4Mongo().get_prefix_dict()
        self.word_to_title = {v_sub: k for k, v in self.keyword_dict.items() for v_sub in v}
        # self.title_to_word = {v:k for k,v in self.word_to_title.items()}

    def get_datas_order_by(self, sort_by="updateTime", ascending=-1, page=1, size=10, mode=None):
        if not mode:
            cond = None
        else:
            cond = {"source_method": mode}
        return mgservice.query_sort(cond, self._table, self._schema, sort_by, ascending, page, size)

    def count_tag(self, tag_column, cond=None):
        return mgservice.count_tag(tag_column, self._schema, self._table, cond=cond)

    def get_datas_by_name(self, keyword="", sort_by="updateTime", ascending=-1, page=1, size=10, mode=None):
        if not mode:
            cond = {
                # "keyword": {"$regex":keyword}
                "keyword": {"$in": self.keyword_dict.get(keyword)}
            }
        else:
            cond = {
                # "keyword": {"$regex":keyword},
                "keyword": {"$int": self.keyword_dict.get(keyword)},
                "source_method": mode
            }
        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)

    def search_datas_by_keyword(self, keyword="", sort_by="updateTime", ascending=-1, page=1, size=10):
        cond = {
            "keyword":{"$regex":keyword}
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

    def count_datas(self, cond):
        # mgservice.cou
        return mgservice.count_datas(cond, table=self._table, db=self._schema)

    def count_tags(self, cond=None):
        datas = mgservice.count_tag("keyword", self._schema, self._table)
        num_map = {data['keyword']: data['num'] for data in datas}
        temp = {}
        for k,v in num_map.items():
            if self.word_to_title.get(k) in temp.keys():
                temp[self.word_to_title.get(k)] += v
            else:
                temp[self.word_to_title.get(k)] = v

        result = {
            "sources": {data['source']: data['num'] for data in mgservice.count_tag("source", self._schema, self._table)
                        if data['source'] != ''},
            "education": {data['highestEducationDegree']: data['num'] for data in
                          mgservice.count_tag("highestEducationDegree", self._schema, self._table) if
                          data['highestEducationDegree'] != ''},
            "jobTitle": temp
        }
        return result


if __name__ == '__main__':
    controller = KBTalentBankController4Mongo()
    # controller.get_datas_order_by("")
    # controller.delete_by_id("")
    print(controller.get_datas())
