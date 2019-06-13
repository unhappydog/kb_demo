import re
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
from threading import Lock

class TalentMap:
    _lock = Lock()
    _instance = None

    def __init__(self, controller):
        self.controller = controller

    @classmethod
    def instance(cls, *args, **kwargs):
        if TalentMap._instance is None:
            with TalentMap._lock:
                if TalentMap._instance is None:
                    TalentMap._instance = cls(*args, **kwargs)
        return TalentMap._instance


    def gen_map(self, company):
        datas = self.controller.get_datas_by_company(company)
        # import pdb; pdb.set_trace()
        in_offices = []
        off_offices = []
        if datas:
            datas = [{"workExperience":TalentMap.extract_company_experience(company, data)} for data in datas]
            for experience in datas:
                if TalentMap.is_in_office(experience):
                    in_offices.append(experience)
                elif experience.get("workExperience", []):
                    off_offices.append(experience)
        result = {
            "in_offices":{"count":len(in_offices),
                          "value":TalentMap.count_position(in_offices)},
            "off_offices":{"count":len(off_offices),
                           "value":TalentMap.count_position(off_offices)}
        }
        return result

    @classmethod
    def count_position(cls, datas):
        datas = [{"job_title":data['workExperience']['workPosition']} for data in datas]
        result = {}
        for data in datas:
            result[data['job_title']] = result.get(data['job_title'], 0) + 1
        return result

    @classmethod
    def is_in_office(cls, data):
        """
        判断是否在职
        """
        experience = data.get("workExperience", [])
        if experience:
            if experience.get("workEndTime") is None:
                return True
        return False


    @classmethod
    def extract_company_experience(cls, company, experiences):
        result = []
        for experience in experiences.get('workExperience', []):
            if experience['workCompany'] == company:
                result.append(experience)
        if result:
            result = sorted(result, key=lambda x: x['workStartTime'], reverse=True)
            result = result[0]
        return result
