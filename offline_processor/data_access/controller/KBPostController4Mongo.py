from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice
import settings


@DataMap(_schema=settings.mysql_db, _table="kb_post")
class KBPostController4Mongo(BaseMongoController):
    def get_prefix_dict(self):
        datas = mgservice.query({"postName": {"$regex": "师"}}, self._schema, self._table,
                                projection={"_id": 0, "prefix": 1, "postName": 1})
        return {data['postName']: data['prefix'] for data in datas}

    pass


if __name__ == '__main__':
    controller = KBPostController4Mongo()
    print(controller.get_prefix_dict())
