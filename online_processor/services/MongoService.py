import pymongo
from utils.Tags import Singleton
from online_processor.settings import mongo_host, mongo_port, mongo_db


@Singleton
class MongoService:
    def __init__(self, ip=mongo_host, port=mongo_port, db=mongo_db):
        self.client = pymongo.MongoClient("mongodb://{0}:{1}/".format(ip, port))
        self.db = db

    def insert(self, doc, db, table):
        self.client[db][table].insert(doc, continue_on_error=True)

    def update(self, spec, doc, db, table):
        self.client[db][table].update_one(spec, {"$set": doc})

    def delete(self, query_cond, db, table):
        self.client[db][table].delete_many(query_cond)

    def query(self, query_cond, db, table):
        if query_cond is None or query_cond == {}:
            query_result = self.client[db][table].find()
        else:
            query_result = self.client[db][table].find(query_cond)
        x = [doc for doc in query_result]
        return x

    def query_sort(self, query_cond,table, db, sort_by='', ascending=-1, page=1,
                   size=10):
        skip = (page - 1) * size
        if query_cond is None or query_cond == {}:
            query_result = self.client[db][table].find().sort(sort_by, ascending).skip(skip).limit(size)
        else:
            query_result = self.client[db][table].find(query_cond).sort(sort_by, ascending).skip(skip).limit(size)
        x = [doc for doc in query_result]
        return x

    def count_tag(self, tag_column, db, table, limit=10, cond=None):
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


mgservice = MongoService()

if __name__ == '__main__':
    # data = {"name": 'tabao', 'alexa': 100, 'url': 'https://www.baidu.com', 'type': 3}

    ms = MongoService()
    # ms.insert(data)
    # ms.update({'Author': 'qq_43312436'},{'Author':'test111'})
    # print(ms.query({'Author': 'qq_43312436'})[0])
    # print(ms.count_tag("tags"))
    import time

    a = time.time()
    # ms.delete_one({
    #     "datatype": "paper",
    #     "Source": "arxiv"
    # })
    # print(ms.query_sort({
    #     "datatype": "paper",
    #     "Source": "arxiv"
    # }, sort_by='pubtime', size=1))
    # print(ms.query({"_id": 1474022}))
    ms.delete_one({"tags": 'topic_172'})
    # print(ms.query_sort({"Pdf2Png": {"$exists": True}}, sort_by='pubtime'))
    print(ms.count_column_with_cond({"PaperClassification": "Conference"}, "Conference"))
    print(time.time() - a)
