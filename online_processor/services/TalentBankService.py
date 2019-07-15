from utils.Tags import Singleton
from core.talent_bank.talent_bank import TalentBank
from threading import Lock

_lock = Lock()
@Singleton
class TalentBankService:

    def __init__(self):
        self.talent_bank = TalentBank()

    def save(self, cv, talent_bank_id=None, save_tag=False):
        with _lock:
            self.talent_bank.save(cv,talent_bank_id=talent_bank_id, save_tag=save_tag)

    def search_by_keyword(self, keyword, location=None, experience=None, educationDegree=None, page=1, size=10,talent_bank_id=None, sort_by=None):
        return self.talent_bank.search_by_keyword(keyword, location, experience, educationDegree,page, size,talent_bank_id=talent_bank_id, sort_by=sort_by)

    def get_datas_by(self, keyword=None, location=None, update_time=None, experience=None, educationDegree=None, source=None, source_method=None, job_title=None, searchword=None, company=None, academy=None, skill_tag=None, tag=[], page=1, size=10, talent_bank_id=None, sort_by=None):
        return self.talent_bank.get_datas_by(keyword,location, update_time, experience, educationDegree, source,source_method,job_title,searchword,company, academy, skill_tag, tag, page, size, talent_bank_id=talent_bank_id,sort_by=sort_by)

    def get_by_id(self, id,talent_bank_id=None):
        return self.talent_bank.get_by_id(id,talent_bank_id=talent_bank_id)

    def delete_by_id(self, id,talent_bank_id=None):
        self.talent_bank.delete_by_id(id,talent_bank_id=talent_bank_id)

    def update(self, cv,talent_bank_id=None):
        with _lock:
            self.talent_bank.update(cv,talent_bank_id=talent_bank_id)

    def get_datas(self, page, size, mode, name=None,talent_bank_id=None):
        return self.talent_bank.get_datas(page, size, mode, name,talent_bank_id=talent_bank_id)

    def add_to_favorite(self, cv, user_id, talent_bank_id=None):
        with _lock:
            # cv = self.get_by_id(cv_id,talent_bank_id=talent_bank_id)
            if cv:
                cv['tag'] = cv['tag'] + [user_id] if cv.get('tag', None) else [user_id]
                cv['tag'] = list(set(cv['tag']))
                self.talent_bank.save(cv,save_tag=True,talent_bank_id=talent_bank_id)
                return True
            else:
                return False

    def remove_from_favorite(self, cv_id, user_id, talent_bank_id=None):
        with _lock:
            cv = self.get_by_id(cv_id,talent_bank_id=talent_bank_id)
            if cv:
                cv = cv[0]
                cv['tag'] = list(set(cv.get('tag', [])))
                if user_id in cv['tag']:
                    cv['tag'].remove(user_id)
                self.talent_bank.save(cv, save_tag=True, talent_bank_id=talent_bank_id)
                return True
            else:
                return False

    def get_favorite(self, user_id, location=None,update_time=None, experience=None, educationDegree=None, source=None, source_method=None, job_title=None, searchword=None, page=1, size=10, talent_bank_id=None, sort_by=None):
        return self.get_datas_by(None,location, update_time, experience, educationDegree,source, source_method, job_title, searchword,None,None, None, user_id, page, size, talent_bank_id=talent_bank_id, sort_by=sort_by)

    def count_column(self, column_name, talent_bank_id=None):
        """
        统计不同标签的个数
        """
        return self.talent_bank.count_column(column_name, talent_bank_id=talent_bank_id)

    def gen_map(self, company_name):
        return self.talent_bank.gen_map(company_name)

    def gen_chart_data(self, company_name, in_office, job_type, job_title):
        return self.talent_bank.gen_chart_data(company_name,in_office, job_type, job_title)

    def get_all_cv(self, company, academy, skill_tag, sort_by="updateTime", ascending=-1, page=1, size=10):
        return self.talent_bank.get_all_cv(company, academy, skill_tag, sort_by="updateTime", ascending=-1, page=1, size=10)

    def get_map_cv(self, company_name, in_office):
        return self.talent_bank.get_map_cv(company_name, in_office)

    def move_cv_to_kanban(self, cv_id, kanban_tag, talent_bank_id=None):
        data = {'_id': cv_id,
                "kanban_tag":kanban_tag}
        self.talent_bank.update(data, talent_bank_id=talent_bank_id)
        # verify
        cv = self.get_by_id(cv_id, talent_bank_id=talent_bank_id)
        if cv:
            if cv[0]['kanban_tag'] == kanban_tag:
                return True
        else:
            return False

    def get_cv_by_kanban(self, kanban_tag, job_title, page,size, talent_bank_id=None):
        return self.talent_bank.get_cv_by_kanban(kanban_tag, job_title, page, size)


tbService = TalentBankService()
