from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo
from services.tool_services.MongoService import mgService as mgservice
import re
from utils.Constants import post_prefix, REGEX_CN


@DataMap(_schema="kb_demo", _table="kb_project_experience")
class ProjectExperienceController4Mongo(BaseMongoController):
    def __init__(self):
        self.keyword_dict = KBPostController4Mongo().get_prefix_dict()

    def get_datas_by_name(self, name="", sort_by="projectEndTime", ascending=-1, page=1, size=10):
        if name == "算法工程师":
            return mgservice.query_sort(query_cond={'keyword':{"$regex":"算法"}},
                                    db=self._schema,
                                    table=self._table,sort_by=sort_by,
                                    ascending=ascending, page=page, size=size)

        keywords = self.keyword_dict.get(name, [])
        data = mgservice.query_sort(query_cond={'keyword':{'$in':keywords}},
                                    db=self._schema,
                                    table=self._table,sort_by=sort_by,
                                    ascending=ascending, page=page, size=size)
        return data



    def get_datas_by_name_v2(self, name="", sort_by="projectEndTime", ascending=-1, page=1, size=10):
        # add hot 算法工程师
        if name == "算法工程师":
            return mgservice.query_sort(query_cond={'keyword':{"$regex":"算法"}},
                                    db=self._schema,
                                    table=self._table,sort_by=sort_by,
                                    ascending=ascending, page=page, size=size)

        reg_pattern = "({0})".format("|".join(post_prefix))
        if re.match(".+" + reg_pattern + "$", name):
            keyword = re.sub(reg_pattern, '', name)
        else:
            keyword = name
        data = mgservice.query_sort(query_cond={'keyword':keyword},
                                    db=self._schema,
                                    table=self._table,sort_by=sort_by,
                                    ascending=ascending, page=page, size=size)
        return data


if __name__ == '__main__':
    controller = ProjectExperienceController4Mongo()
    # controller.get_datas_order_by("")
    # controller.delete_by_id("")
    print(controller.get_datas())
