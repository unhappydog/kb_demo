from data_access.base.BaseController import BaseController
from data_access.models.Words import Words
from utils.MapTags import DataMap, sql
from utils.Tags import return_type
import settings


@DataMap(_schema=settings.mysql_db, _table="kb_stop_words_cn")
class KBStopWordsController(BaseController):
    @return_type(Words)
    @sql("select * from _table")
    def get_datas(self): pass


if __name__ == '__main__':
    kb = KBStopWordsController()
    for data in kb.get_datas():
        print(data)
    print(kb.get_datas())
