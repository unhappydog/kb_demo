from data_access.base.BaseController import BaseController
from data_access.models.KB_Company import kb_Company
from utils.Tags import return_type
from utils.MapTags import DataMap, sql
import settings


@DataMap(_schema=settings.mysql_db, _table="kb_company")
class KBCompanyController(BaseController):
    @return_type(kb_Company)
    @sql("select * from _table")
    def get_datas(self): pass
