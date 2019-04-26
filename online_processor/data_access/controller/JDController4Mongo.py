from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice


@DataMap(_schema="kb_demo", _table="JD")
class JDController4Mongo(BaseMongoController):
    pass


if __name__ == '__main__':
    controller = JDController4Mongo()
    # controller.get_datas_order_by("")
    # controller.delete_by_id("")
    print(controller.get_datas())
