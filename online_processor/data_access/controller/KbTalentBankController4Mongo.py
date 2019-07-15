from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo
from contextlib import contextmanager
from threading import Lock
from datetime import datetime, timedelta
degrees =['中专', '大专', '本科', '硕士', '博士']
degree_dict = {
    '不限': degrees,
    '中专': degrees,
    '大专': degrees[1:],
    '本科': degrees[2:],
    '硕士': degrees[3:],
    '博士': degrees[4:]
}

@DataMap(_schema="kb_talent_banks", _table="kb_talent_bank")
class KBTalentBankController4Mongo(BaseMongoController):
    _switch_lock = Lock()


    def __init__(self):
        self.keyword_dict = KBPostController4Mongo().get_prefix_dict()
        self.keyword_dict['自然语言处理工程师'].remove('知识图谱')
        self.word_to_title = {}
        for job_title, keywords in self.keyword_dict.items():
            for keyword in keywords:
                if keyword in self.word_to_title.keys():
                    self.word_to_title[keyword].append(job_title)
                else:
                    self.word_to_title[keyword] = [job_title]
        self.word_to_title['知识图谱'] = ['知识图谱工程师']

    @contextmanager
    def switch_to_table(self, _table="kb_talent_bank"):
        self._switch_lock.acquire()
        try:
            self._table = _table
            yield
        finally:
            self._switch_lock.release()


    def get_datas_order_by(self, sort_by="updateTime", ascending=-1, page=1, size=10, mode=None, name=None):
        if not mode:
            cond = {}
        else:
            cond = {"source_method": mode}
        if name:
            cond['name'] = {"$regex": name}
        return mgservice.query_sort(cond, self._table, self._schema, sort_by, ascending, page, size)

    def count_tag(self, tag_column, cond=None):
        return mgservice.count_tag(tag_column, self._schema, self._table, cond=cond)

    def count_column(self, column_name, cond=None):
        return mgservice.count_column_with_cond(cond, column_name, self._schema, self._table)

    def get_datas_by(self,keyword=None, location=None, update_time=None, experience=None, educationDegree=None, source=None, source_method=None, job_title=None,searchword=None, company=None, academy=None, skill_tag=None,
                     tag=None ,ascending=-1, page=1, size=10, sort_by="updateTime"):
        cond = {}
        if keyword:
            cond = {'$or':[{'jobTitle':{'$regex':keyword}},{'workExperience.workCompany':{'$regex':keyword}},{'workExperience.workPosition':{'$regex':keyword}},{'name':keyword}]}
        if location:
            location = location.split('-')[1]
            cond['currentAddress'] = {'$regex': location}
        if experience:
            low, high = experience.split('-')
            cond['workYear'] = {'$gt': int(low), '$lt': int(high)}
        if educationDegree:
            cond['highestEducationDegree'] = {'$in': degree_dict.get(educationDegree, [])}
        if source:
            cond['source'] = source
        if source_method:
            cond['source_method'] = source_method
        if job_title:
            cond['jobTitle'] = job_title
        if update_time:
            update_time = datetime.now() - timedelta(days=int(update_time))
            cond['updateTime'] = {'$gt':update_time}
        if tag:
            cond['tag'] = tag
        if sort_by is None:
            sort_by = 'updateTime'

        if company:
            cond['workExperience.workCompany'] = company

        if academy:
            cond['educationExperience.educationSchool'] = academy

        if skill_tag:
            cond['skill_tag'] = skill_tag
        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)


    def search_datas_by_keyword(self, keyword="", sort_by="updateTime", location=None, experience=None,
                                educationDegree=None, ascending=-1, page=1, size=10):
        cond = {
            "keyword": {"$regex": keyword}
        }
        # import pdb; pdb.set_trace()
        if location:
            location = location.split('-')[1]
            cond['currentAddress'] = {'$regex': location}
        if experience:
            low, high = experience.split('-')
            cond['workYear'] = {'$gt': int(low), '$lt': int(high)}
        if educationDegree:
            cond['highestEducationDegree'] = {'$in': degree_dict.get(educationDegree, [])}
        if sort_by is None:
            sort_by = "updateTime"

        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)

    def get_datas_by_company(self, company):
        if company:
            cond = {
                'workExperience.workCompany': {"$regex":company}
            }
        else:
            return []
        return mgservice.query(cond, db=self._schema, table=self._table)

    def get_datas_by_kanban(self, kanban, job_title, sort_by="updateTime", ascending=-1, page=1, size=100):
        if kanban:
            cond = {
                'kanban_tag':kanban
            }
        else:
            return []
        if job_title:
            cond['jobTitle'] = job_title

        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)


    def get_all_cv(self, company, academy, skill_tag, sort_by="updateTime", ascending=-1, page=1, size=10):
        cond = {}
        if company is not None:
            cond['workExperience.workCompany'] = {'$in': company}
        if academy is not None:
            cond['educationExperience.educationSchool'] = {'$in':academy}
        if skill_tag is not None:
            cond['skill_tag'] = {'$in': skill_tag}

        return mgservice.query_sort(query_cond=cond,
                                    table=self._table,
                                    db=self._schema,
                                    sort_by=sort_by,
                                    ascending=ascending,
                                    page=page,
                                    size=size)

if __name__ == '__main__':
    controller = KBTalentBankController4Mongo()
    # controller.get_datas_order_by("")
    # controller.delete_by_id("")
    print(controller.get_datas())
