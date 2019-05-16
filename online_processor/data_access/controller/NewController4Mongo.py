from data_access.base.BaseMongoController import BaseMongoController
from utils.MongoMapTags import DataMap, query
from settings import mongo_db
from services.tool_services.MongoService import mgService
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
            if data['IMG_URL'] != "":
                data['IMG_URL'] = data['IMG_URL'].split(';')[:3]
            else:
                data['IMG_URL'] = random.sample(images, 1)
            data['IMG_URL'] = ";".join(data['IMG_URL'])
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
    def get_news_by_domain(self, domain, orderBy="PUBTIME", page=1, limit=10):
        if domain is None:
            domain = {}
        else:
            domain = {
                'DomainTag': domain
            }
        return mgService.query_sort(query_cond=domain, table=self._table, db=self._schema, sort_by=orderBy,
                                    ascending=-1,
                                    page=page, size=limit, projection={
                "ID": 1,
                "TITLE": 1,
                "PUBTIME": 1,
                "BRIEF": 1,
                "CONTENT": 1,
                "AUTHOR": 1,
                "URL": 1,
                "IMG_URL": 1,
                "SOURCE": 1,
                "Tag": 1
            })

    @random_image
    def get_news_by_tag(self, tag, orderBy="PUBTIME", page=1, limit=10):
        if tag is None:
            cond = {}
        else:
            cond = {
                "Tag": tag
            }
        return mgService.query_sort(query_cond=cond, table=self._table, db=self._schema, sort_by=orderBy, ascending=-1,
                                    page=page, size=limit, projection={
                "ID": 1,
                "TITLE": 1,
                "PUBTIME": 1,
                "BRIEF": 1,
                "CONTENT": 1,
                "AUTHOR": 1,
                "URL": 1,
                "IMG_URL": 1,
                "SOURCE": 1,
                "Tag": 1
            })

    @random_image
    def get_news(self, orderBy="PUBTIME", page=1, limit=10):
        return mgService.query_sort(query_cond={}, table=self._table, db=self._schema, sort_by=orderBy, ascending=-1,
                                    page=page, size=limit, projection={
                "ID": 1,
                "TITLE": 1,
                "PUBTIME": 1,
                "BRIEF": 1,
                "CONTENT": 1,
                "AUTHOR": 1,
                "URL": 1,
                "IMG_URL": 1,
                "SOURCE": 1,
                "Tag": 1
            })