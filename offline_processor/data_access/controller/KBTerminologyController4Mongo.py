from utils.MongoMapTags import DataMap
from utils.Logger import logging
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice
from bson.objectid import ObjectId
import settings


@DataMap(_schema=settings.mongo_db, _table="kb_terminology")
class KBTerminologyController4Mongo(BaseMongoController):

    def get_name_ids(self):
        datas = mgservice.query(query_cond=None, db=self._schema, table=self._table,
                                projection={'_id': True, 'cnName': True, 'engName': True})
        return datas

    def get_data_by_id(self, _id=''):
        """

        :param _id:
        :return: dict type
        """
        if type(_id) == str:
            cond = {"_id": ObjectId(_id)}
        elif type(_id) == ObjectId:
            cond = {"_id": _id}
        else:
            logging.error("message _id should be type str or objectId")
        datas = mgservice.query(query_cond=cond, db=self._schema, table=self._table)
        if datas:
            return datas[0]
        else:
            return None


if __name__ == '__main__':
    kb = KBTerminologyController4Mongo()
    datas = kb.get_name_ids()
    for data in datas:
        print(data)
