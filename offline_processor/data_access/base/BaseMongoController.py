from utils.MongoMapTags import insert, update, query, delete, query_as_gen
from utils.Logger import logging
from pymongo.errors import DuplicateKeyError
from services.tool_services.MongoService import mgService
import math


class BaseMongoController:
    @query(by={"_id": "_id"})
    def get_data_by_id(self, _id=''):
        pass

    @query(by=None)
    def get_datas(self):
        pass

    @insert()
    def insert_data(self, data):
        pass

    @update()
    def update_by_id(self, data):
        pass

    @delete()
    def delete_by_id(self, _id):
        pass

    @query_as_gen()
    def get_datas_as_gen(self, data):
        pass

    def update_datas_from_df(self, df, key_column="_id"):
        if df is None or df.empty:
            return
        for index, row in df.iterrows():
            columns = list(row.index)
            if key_column not in columns:
                logging.exception("key_column missed")
                return
            data = {}
            for column in columns:
                # if row[column] is None or row[column] == "":
                #     continue
                if type(row[column]) is float:
                    if math.isnan(row[column]):
                        continue
                    else:
                        data[column] = row[column]
                else:
                    data[column] = row[column]
            try:
                cond = {key_column: data[key_column]}
                del data[key_column]
                mgService.update(cond, data, self._schema, self._table)
            except Exception as e:
                logging.exception(e)

    def insert_datas_from_df(self, df):
        if df is None or df.empty:
            return
        for index, row in df.iterrows():
            columns = list(row.index)
            data = {}
            for column in columns:
                # if row[column] is None or row[column] == "":
                #     continue
                if type(row[column]) is float:
                    if math.isnan(row[column]):
                        continue
                    else:
                        data[column] = row[column]
                else:
                    data[column] = row[column]
            try:
                self.insert_data(data)
            except DuplicateKeyError as e:
                logging.warning("data {0} is duplicated, trying to update".format(data.get("_id", "")))
                if "_id" not in data.keys():
                    logging.exception("_id is not in data")
                else:
                    cond = {"_id": data["_id"]}
                    mgService.update(cond, data, self._schema, self._table)

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
