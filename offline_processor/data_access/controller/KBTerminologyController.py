from data_access.base.BaseController import BaseController
from data_access.models.KB_Terminology import KB_Terminology
from utils.MapTags import DataMap, sql
from utils.Tags import return_type
import settings

@DataMap(_schema=settings.mysql_db, _table="kb_terminology")
class KBTerminologyController(BaseController):

    @return_type(KB_Terminology)
    @sql("select * from _table where id = {0}", "_id")
    def get_data_by_id(self, _id): pass

    @return_type(KB_Terminology)
    @sql("select * from _table")
    def get_datas(self): pass

    @sql("select id, cnName, engName from _table")
    def get_id_name(self): pass

    @sql("select ")
    def get_name_by_att(self):pass