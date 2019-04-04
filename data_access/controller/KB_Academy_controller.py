from utils.MapTags import DataMap, sql, return_type
from data_access.models.KB_Academy import kb_academy


@DataMap(_schema="kb_demo", _table="kb_academy")
class kb_academy_controller:
    def __init__(self):
        pass

    @return_type(kb_academy)
    @sql("select * from kb_academy")
    def get_datas(self): pass

    @return_type(kb_academy)
    @sql("select * from kb_academy where id={0}", '_id')
    def get_data_by_id(self, _id=0): pass


if __name__ == '__main__':
    kkk = kb_academy_controller()
    # print(kkk._id)
    print(kkk.get_datas())
    print(kkk.get_data_by_id(_id=341))
