from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from utils.Logger import logging
from data_access.base.BaseMongoController import BaseMongoController
from data_access.models.KB_Terminology import KB_Terminology
from services.tool_services.MongoService import mgService as mgservice
from bson.objectid import ObjectId
import settings


@DataMap(_schema=settings.mongo_db, _table="kb_talent")
class KBTalentController4Mongo(BaseMongoController):
    def get_talent_by_name_order_by_date(self, name, page=1, limit=10):
        data = mgservice.query_sort(query_cond={
            'JobTitle': name,
            "ISBAD": 0,
            "ISREPLICATE": 0,
            "duty":{"$exists":True},
            "requirement":{"$exists":True}
        }, db=self._schema, table=self._table, projection={
            "_id": 1,
            "Name": 1,
            "Company": 1,
            "Salary": 1,
            "City": 1,
            "Education": 1,
            "Experience": 1,
            "Welfare": 1,
            "Source": 1,
            "JobType": 1,
            "Startdate": 1,
            "Enddate": 1,
            # "JobDescription": 1,
            'duty':1,
            'requirement':1,
            "JobLocation": 1,
            "graph": 1
        }, page=page, size=limit, sort_by="Startdate")

        return data

    pass


if __name__ == '__main__':
    contoller = KBTalentController4Mongo()
    print(contoller.get_talent_by_name_order_by_date("数据专家"))
