from utils.MongoMapTags import insert, update, query, delete


class BaseMongoController:
    @query(by={"_id": "_id"})
    def get_data_by_id(self, _id=''): pass

    @query(by=None)
    def get_datas(self): pass

    @insert()
    def insert_data(self, data): pass

    @update()
    def update_by_id(self, data): pass

    @delete()
    def delete_by_id(self, _id): pass
