from utils.MapTags import DataMap, sql, update, insert


class BaseController:
    @sql("select * from _table where id = {0}", "_id")
    def get_data_by_id(self, _id): pass

    @sql("select * from _table")
    def get_datas(self): pass

    @insert()
    def insert_datas(self, data): pass

    @update()
    def update_by_id(self, data): pass

    @sql("delete from _table where id = {0}", "_id")
    def delete_by_id(self, _id): pass
