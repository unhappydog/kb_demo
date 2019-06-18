from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from utils.Logger import logging
from data_access.base.BaseMongoController import BaseMongoController
from data_access.models.KB_Terminology import KB_Terminology
from services.tool_services.MongoService import mgService as mgservice
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo
from bson.objectid import ObjectId
import settings
import re


def format_jds(func):
    def __wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return [format_single_jd(jd) for jd in data]
    return __wrapper


def format_single_jd(jd):
    # format salary
    if re.match('[0-9]{1,10}-[0-9]{1,10}', jd['Salary']):
        jd['Salary'] = "-".join(["{:.0f}k".format(float(ele) / 1000) for ele in jd['Salary'].split('-')])
    elif re.match('[0-9]{1,10}以上', jd['Salary']):
        jd['Salary'] = "{:.0f}k以上".format(float(jd['Salary'][:-2])/1000)
    else:
        jd['Salary'] = ""
    return jd


@DataMap(_schema=settings.mongo_db, _table="kb_talent")
class KBTalentController4Mongo(BaseMongoController):
    def __init__(self):
        self.keyword_dict = KBPostController4Mongo().get_prefix_dict()

    @format_jds
    def get_talent_by_name_order_by_date(self, name, page=1, limit=10):

        data = mgservice.query_sort(query_cond={
            'JobTitle': {'$regex': self.tag_data(name)},
            "ISBAD": 0,
            "ISREPLICATE": 0,
            "duty": {"$exists": True},
            "requirement": {"$exists": True},
            "graph":{"$exists":True}
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
            'duty': 1,
            'requirement': 1,
            "JobLocation": 1,
            "graph": 1
        }, page=page, size=limit, sort_by="Startdate")

        return data

    pass

    def tag_data(self, name):
        for k, v in self.keyword_dict.items():
            for keyword in v:
                if keyword in name:
                    return k
        return name


if __name__ == '__main__':
    contoller = KBTalentController4Mongo()
    print(contoller.get_talent_by_name_order_by_date("数据挖掘工程师"))
