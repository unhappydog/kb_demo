from data_access.base.BaseMongoController import BaseMongoController
from utils.MongoMapTags import DataMap, query
from settings import mongo_db
from services.tool_services.MongoService import mgService
import re
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo
import random


def random_image(func):
    images = [
        "http://thyrsi.com/t6/672/1550817073x2890149512.jpg",
        "http://thyrsi.com/t6/672/1550817157x2890149512.jpg",
        "http://thyrsi.com/t6/672/1550817185x2890149512.jpg"
    ]

    def _wrapper(*args, **kwargs):
        datas = func(*args, **kwargs)
        for data in datas:
            if data['IMG_URL'] != "" and type(data['IMG_URL']) == str:
                data['IMG_URL'] = data['IMG_URL'].split(';')[:3]
            # else:
            #     data['IMG_URL'] = random.sample(images, 1)

            # data['IMG_URL'] = [img for img in data['IMG_URL'] if re.match("^http.*\.(jpg|jpeg|gif|png)$", img)]
            data['IMG_URL'] = ";".join(data['IMG_URL'])
            # data['IMG_URL'] = "" if data['IMG_URL'] == "[]" else data['IMG_URL']
        return datas

    return _wrapper


@DataMap(_schema=mongo_db, _table="kb_news")
class NewController4Mongo(BaseMongoController):
    def __init__(self):
        self.keyword_dict = KBPostController4Mongo().get_prefix_dict()

    def tag_data(self, name):
        for k, v in self.keyword_dict.items():
            for keyword in v:
                if keyword in name:
                    return k
        return name

    @random_image
    def get_news_by(self, domain, tag, company_tag, orderBy="pubtime", page=1, limit=10):
        cond = {'ISREPLICATE': 0,
                      "ISBAD": 0}
        if domain:
            cond['DomainTag'] = domain

        if tag:
            cond['Tag'] = tag

        if company_tag:
            cond['CompanyTag'] = company_tag

        datas = mgService.query_sort(query_cond=cond, table=self._table, db=self._schema, sort_by=orderBy,ascending=-1,page=page, size=limit, projection={
            "title": 1,
            "TITLE": 1,
            "pubtime": 1,
            "PUBTIME": 1,
            "brief": 1,
            "BRIEF": 1,
            "content": 1,
            "CONTENT": 1,
            "author": 1,
            "AUTHOR": 1,
            "url": 1,
            "URL": 1,
            "IMG_URL": 1,
            "source": 1,
            "Tag": 1,
            "companys":1,
            "persons":1,
            "job_tag":1,
            "htmlContent":1,
            'htmlcontent':1
            })
        upper_column = ['title', 'pubtime', 'brief', 'content', 'author', 'url']
        for data in datas:
            for k,v in data.items():
                if k in upper_column:
                    data[k.upper()] = v
                    del data[k]
            if 'htmlcontent' in data.keys():
                data['htmlContent'] = data['htmlcontent']
                del data['htmlcontent']
        return datas

