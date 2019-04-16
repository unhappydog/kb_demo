from data_access.base.BaseController import BaseController
from data_access.models.New import New
from utils.MapTags import DataMap, sql, sql_as_gen
from utils.Tags import return_type
import settings


@DataMap(_schema=settings.mysql_db, _table="kb_news")
class NewController(BaseController):

    @return_type(New, generate=True)
    @sql_as_gen("select * from _table")
    def get_news_as_gen(self): pass
