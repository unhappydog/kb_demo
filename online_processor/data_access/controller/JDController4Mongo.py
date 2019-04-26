from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice
from settings import mongo_db
from bson.objectid import ObjectId
import logging
from datetime import datetime,timedelta


@DataMap(_schema=mongo_db, _table="kb_talent")
class JDController4Mongo(BaseMongoController):
    def get_datas_order_by(self, sort_by="", ascending=-1, page=1, size=10):
        return mgservice.query_sort(None, self._table, self._schema, sort_by, ascending, page, size)

    def get_data_by_id(self, _id=''):
        """
        :param _id:
        :return: dict type
        """
        if type(_id) == str:
            cond = {"_id":ObjectId(_id)}
        elif type(_id) == ObjectId:
            cond = {"_id": _id}
        else:
            logging.error("message _id should be type str or objectId")
        datas = mgservice.query(query_cond=cond, db=self._schema, table=self._table)
        if datas:
            return datas
        else:
            return None

    def count_tag(self, tag_column, cond=None):
        return mgservice.count_tag(tag_column, self._schema, self._table, cond=cond)

    def get_datas_by_date(self,start_date,end_date):
        query_cond = {"Startdate":{"$lte":end_date,"$gte":start_date}}
        return mgservice.query(query_cond=query_cond, db=self._schema, table=self._table)

    def get_datas_by_date_and_jobtitle(self,end_date = datetime.now(),custom_month = 6,job_title=[]):
        start_date = datetime.now() - timedelta(days=custom_month*30)
        start_date = datetime(start_date.year,start_date.month,1)
        query_cond = {"Startdate":{"$lte":end_date,"$gte":start_date},"JobTitle":{"$all":[job_title]}}
        return mgservice.query(query_cond=query_cond, db=self._schema, table=self._table)

if __name__ == '__main__':
    controller = JDController4Mongo()
    controller.get_datas_order_by("")
    # controller.delete_by_id("")
    print(controller.get_datas())

