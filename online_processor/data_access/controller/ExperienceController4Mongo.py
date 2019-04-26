from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice
import re
from utils.Constants import post_prefix, REGEX_CN


@DataMap(_schema="kb_demo", _table="kb_project_experience")
class ProjectExperienceController4Mongo(BaseMongoController):

    def get_datas_by_name(self, name="", sort_by="projectEndTime", ascending=-1, page=1, size=10):
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
