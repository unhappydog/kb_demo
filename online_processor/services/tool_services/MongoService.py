import pymongo
from utils.Tags import Singleton
from settings import mongo_host, mongo_port, mongo_db


@Singleton
class MongoService:
    def __init__(self, ip=mongo_host, port=mongo_port, db=mongo_db):
        self.client = pymongo.MongoClient("mongodb://{0}:{1}/".format(ip, port))
        self.db = db

    def insert(self, doc, db, table):
        """
        插入操作
        :param doc:文档字典
        :param db:数据库
        :param table:表格名称
        :return:
        """
        self.client[db][table].insert(doc, continue_on_error=True)

    def update(self, spec, doc, db, table):
        self.client[db][table].update_one(spec, {"$set": doc})

    def delete(self, query_cond, db, table):
        self.client[db][table].delete_many(query_cond)

    def query(self, query_cond, db, table, projection=None):
        """
        查询数据库
        :param query_cond:
        :param db:
        :param table:
        :param projection: 保留字段，字典类型
        :return:
        """
        if query_cond is None or query_cond == {}:
            query_result = self.client[db][table].find(projection=projection)
        else:
            query_result = self.client[db][table].find(query_cond, projection=projection)
        x = [doc for doc in query_result]
        return x

    def query_sort(self, query_cond, table, db, sort_by='', ascending=-1, page=1,
                   size=10):
        """
        按顺序返回
        :param query_cond:
        :param table:
        :param db:
        :param sort_by:
        :param ascending:
        :param page:
        :param size:
        :return:
        """
        skip = (page - 1) * size
        if query_cond is None or query_cond == {}:
            query_result = self.client[db][table].find().sort(sort_by, ascending).skip(skip).limit(size)
        else:
            query_result = self.client[db][table].find(query_cond).sort(sort_by, ascending).skip(skip).limit(size)
        x = [doc for doc in query_result]
        return x

    def count_tag(self, tag_column, db, table, limit=10, cond=None):
        """
        统计标签出现的次数
        :param tag_column:
        :param db:
        :param table:
        :param limit:未使用到
        :param cond: 条件
        :return:
        """
        if cond == None:
            query_result = self.client[db][table].aggregate([{"$unwind": "${0}".format(tag_column)},
                                                             {"$group": {"_id": "${0}".format(tag_column),
                                                                         "num": {"$sum": 1}}},
                                                             {"$project": {"_id": 0, tag_column: "$_id", "num": 1}},
                                                             {"$sort": {"num": -1}}])
        else:
            query_result = self.client[db][table].aggregate([{"$match": cond},
                                                             {"$unwind": "${0}".format(tag_column)},
                                                             {"$group": {"_id": "${0}".format(tag_column),
                                                                         "num": {"$sum": 1}}},
                                                             {"$project": {"_id": 0, tag_column: "$_id", "num": 1}},
                                                             {"$sort": {"num": -1}}])
        x = [doc for doc in query_result]
        return x

    def count_column_with_cond(self, cond, column_name, db, table):
        query_result = self.client[db][table].aggregate([
            {"$match": cond},
            {"$group": {
                "_id": "${0}".format(column_name),
                "num": {"$sum": 1}}},
            {"$project": {"_id": 0, column_name: "$_id", "num": 1}},
            {"$sort": {"num": -1}}])
        x = [doc for doc in query_result]
        return x

    def remove_dul(self, dul_col, db, table):
        dul_ids = self.client[db][table].aggregate([
            {"$group": {
                "_d_id": {"$min": '$_id'},
                "_id": {"id": "${0}".format(dul_col)},
                "num": {"$sum": 1},
            }}
            # {"$project": {"_id": 0, dul_col: "$_id", "num": 1}}
        ])
        x = [doc for doc in dul_ids]
        return x


mgService = MongoService()

if __name__ == '__main__':
    # data = {"name": 'tabao', 'alexa': 100, 'url': 'https://www.baidu.com', 'type': 3}

    ms = MongoService()
    # ms.insert(data)
    # ms.update({'Author': 'qq_43312436'},{'Author':'test111'})
    # print(ms.query({'Author': 'qq_43312436'})[0])
    # print(ms.count_tag("tags"))
    import time

    a = time.time()

    # data = mgService.query({"schoolName": "武汉大学"},
    #                        'kb_demo',
    #                        'kb_academy')
    # data = mgService.remove_dul('id', 'kb_demo', 'kb_terminology')
    import datetime

    a = datetime.datetime(2018, 1, 1)
    doc = {'test_time1': a, 'cn_code': "我是中国人".encode("gbk").decode("gbk"),
           'cn_utf8': "我不是日本人".encode("utf8").decode("utf8")}

    mgService.insert(doc, 'kb_demo','datetime_test')

    # print(data)

