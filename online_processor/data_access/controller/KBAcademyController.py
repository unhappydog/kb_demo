from utils.MapTags import DataMap, sql
from utils.Tags import return_type
from data_access.base.BaseController import BaseController
from data_access.models.KB_Academy import kb_academy
from settings import mysql_db


@DataMap(_schema=mysql_db, _table="kb_academy")
class KB_AcademyController(BaseController):

    @return_type(kb_academy)
    @sql("select * from kb_academy")
    def get_datas(self): pass

    @return_type(kb_academy)
    @sql("select * from kb_academy where id={0}", '_id')
    def get_data_by_id(self, _id=0): pass


if __name__ == '__main__':
    kkk = KB_AcademyController()
    # print(kkk._id)
    print(kkk.get_datas())
    print(kkk.get_data_by_id(_id=341))
