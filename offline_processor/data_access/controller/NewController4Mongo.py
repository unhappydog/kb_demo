from data_access.base.BaseMongoController import BaseMongoController
from utils.MongoMapTags import DataMap, query, query_as_gen
from settings import mongo_db
from utils.Tags import return_type
from data_access.models.New import New


@DataMap(_schema=mongo_db, _table="kb_news")
class NewController4Mongo(BaseMongoController):

    @query_as_gen(by=None)
    def get_datas_as_gen(self, data): pass

    def get_batch_data(self, batch=100):
        result = []
        count = 0
        cusor = self.get_datas_as_gen()
        for data in cusor:
            result.append(data)
            count += 1
            if count == batch:
                yield result
                result = []
                count = 0
        cusor.close()
        if count != 0:
            yield result

