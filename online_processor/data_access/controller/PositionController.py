from utils.MapTags import DataMap, sql
from utils.Tags import return_type
from data_access.base.BaseController import BaseController
from data_access.models.KB_Academy import kb_academy
from settings import mysql_db


@DataMap(_schema="agent_test", _table="position")
class PositionController(BaseController):

    @sql("select * from _table where name= \"{0}\"", "_name")
    def _get_data_by_name(self, _name=""):pass

    def get_data_by_name(self, name=""):
        return self._get_data_by_name(_name=name)

    def get_datas(self):
        return super().get_datas()

    def get_data_by_id(self, _id=0):
        return super().get_data_by_id(_id=_id)

