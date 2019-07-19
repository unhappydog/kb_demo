import re
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
from threading import Lock
from collections import Counter

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
        in_office_position_count = TalentMap.count_position(in_offices)
        off_office_position_count = TalentMap.count_position(off_offices)

        in_office_map, in_office_ava_count = TalentMap.count_job_type(in_office_position_count)
        off_office_map, off_office_ava_count = TalentMap.count_job_type(off_office_position_count)

        result = {
            "in_offices":{"count":in_office_ava_count,
                          "value": in_office_map},
            "off_offices":{"count":off_office_ava_count,
                           "value":off_office_map}
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
    def count_job_type(cls, data):
        type_names = ["通用软件", "软件测试", "项目经理", "通用销售", "通用研发","工程监督", "人力资源", "产品经理"]
        result = {}
        for type_name in type_names:
            result[type_name] = {'count':0, 'value':[]}

        for job_title, counts in data.items():
            if '测试' in job_title:
                result['软件测试']['count'] += counts
                result['软件测试']['value'] += [{job_title:counts}]
            elif '经理' in job_title:
                result['项目经理']['count'] += counts
                result['项目经理']['value'] += [{job_title:counts}]
            elif "软件" in job_title:
                result['通用软件']['count'] += counts
                result['通用软件']['value'] += [{job_title:counts}]
            elif "人力" in job_title or 'hr' in job_title:
                result['人力资源']['count'] += counts
                result['人力资源']['value'] += [{job_title:counts}]
            elif "产品" in job_title:
                result['产品经理']['count'] += counts
                result['产品经理']['value'] += [{job_title:counts}]
            elif "销售" in job_title:
                result['通用销售']['count'] += counts
                result['通用销售']['value'] += [{job_title:counts}]

        avalibale_count = 0
        for type_name in type_names:
            value = result[type_name]['value']
            value = sorted(value, key=lambda x: list(x.values())[0], reverse=True)[:9]
            count = 0
            for item in value:
                count += list(item.values())[0]
            avalibale_count += count
            result[type_name] = {'value': value, 'count':count}
        return result, avalibale_count


    @classmethod
    def is_in_office(cls, data):
        """
        判断是否在职
        """
        # import pdb; pdb.set_trace()
        experience = data.get("workExperience", [])
        if experience:
            if experience.get("workEndTime") is None:
                return True
        return False

    @classmethod
    def is_in_office_v2(cls, company, data):
        experience = data.get("workExperience", [])
        if experience:
            experience = sorted(experience, key=lambda x: x['workStartTime'], reverse=True)
            result = experience[0]
            if company not in result['workCompany']:
                return False
            if result.get('workEndTime', None) is None:
                return True
        return False


    @classmethod
    def extract_company_experience(cls, company, experiences):
        result = []
        for experience in experiences.get('workExperience', []):
            if company in experience['workCompany']:
                result.append(experience)
        if result:
            result = sorted(result, key=lambda x: x['workStartTime'], reverse=True)
            result = result[0]
        return result

    def get_map_cv(self, company, in_office=None, job_type=None, job_title=None):
        datas = self.controller.get_datas_by_company(company)
        count = 3
        if in_office is None:
            count -= 1
        if job_type is None:
            count -= 1
        if job_title is None:
            count -= 1
        if count >=2:
            return {'result':'failed', 'log':'only one of the in_office, job_type, job_title shuould not be None'}
        elif count <=0:
            return {'result':'failed','log':'at least one of the in_office, job_type, job_title should not be None'}
        # import pdb; pdb.set_trace()


        if in_office == True:
            datas = [data for data in datas if TalentMap.is_in_office_v2(company, data)]
        else:
            datas = [data for data in datas if not TalentMap.is_in_office_v2(company, data)]

        return datas

    def gen_chart_data(self, company, in_office=None, job_type=None, job_title=None):
        """
        gen data
        """
        datas = self.controller.get_datas_by_company(company)
        count = 3
        if in_office is None:
            count -= 1
        if job_type is None:
            count -= 1
        if job_title is None:
            count -= 1
        if count >=2:
            return {'result':'failed', 'log':'only one of the in_office, job_type, job_title shuould not be None'}
        elif count <=0:
            return {'result':'failed','log':'at least one of the in_office, job_type, job_title should not be None'}
        # import pdb; pdb.set_trace()


        if in_office == True:
            datas = [data for data in datas if TalentMap.is_in_office_v2(company, data)]
            result = {'school': TalentMap._gen_school_map(datas),
                  'education':TalentMap._gen_highest_education_map(datas),
                  'jump_direction':[],
                  'location':TalentMap._gen_location_map(datas),
                  'salary':TalentMap._gen_salary_map(datas),
                  'workYear':TalentMap._gen_work_year_map(datas)}

        elif in_office == False:
            datas = [data for data in datas if not TalentMap.is_in_office_v2(company, data)]
            result = {'school': TalentMap._gen_school_map(datas),
                  'education':TalentMap._gen_highest_education_map(datas),
                  'jump_direction':TalentMap._gen_jump_direction_map(company, datas),
                  'location':TalentMap._gen_location_map(datas),
                  'salary':TalentMap._gen_salary_map(datas),
                  'workYear':TalentMap._gen_work_year_map(datas)}

        # result = {'school': TalentMap._gen_school_map(datas),
        #           'education':TalentMap._gen_highest_education_map(datas),
        #           'jump_direction':TalentMap._gen_jump_direction_map(company, datas),
        #           'location':TalentMap._gen_location_map(datas),
        #           'salary':TalentMap._gen_salary_map(datas),
        #           'workYear':TalentMap._gen_work_year_map(datas)}
        return result

    @classmethod
    def _gen_school_map(cls, datas):
        datas = [data for data in datas if data.get('educationExperience')]
        datas = [data['educationExperience'][0].get('educationSchool','') for data in datas]
        count_result = dict(Counter(datas).most_common(9))
        return count_result

    @classmethod
    def _gen_highest_education_map(cls, datas):
        datas = [data for data in datas if data.get('highestEducationDegree')]
        datas = [data['highestEducationDegree'] for data in datas]
        count_result = dict(Counter(datas).most_common(9))
        return count_result

    @classmethod
    def _gen_jump_direction_map(cls, company, datas):
        datas = [data for data in datas if data.get('workExperience')]
        datas = [TalentMap._extract_joump_to_experience(company, data) for data  in datas]
        datas = [data for data in datas if data]
        count_result = dict(Counter(datas).most_common(9))
        return count_result

    @classmethod
    def _gen_location_map(cls, datas):
        datas = [data for data in datas if data.get('currentAddress')]
        datas = [data['currentAddress'].split(' ')[0] for data in datas]
        count_result = dict(Counter(datas).most_common(9))
        return count_result

    @classmethod
    def _gen_salary_map(cls, datas):
        datas = [data for data in datas if data.get('workExperience')]
        datas = [TalentMap._extract_avarge_salary(data) for data  in datas]
        count_result = dict(Counter(datas).most_common(9))
        return count_result

    @classmethod
    def _gen_work_year_map(cls, datas):
        datas = [data for data in datas if data.get('workYear')]
        datas = [data['workYear'] for data  in datas]
        result = []
        for data in datas:
            if data <= 3:
                result.append('0-3年')
            elif data >3 and data <=5:
                result.append('3-5年')
            elif data >5 and data <= 7:
                result.append('5-7年')
            elif data >7 and data<= 10:
                result.append('7-10年')
            else:
                result.append('10年以上')
        count_result = dict(Counter(result).most_common(9))
        return count_result

    @classmethod
    def _extract_joump_to_experience(cls, company, data):
        # import pdb; pdb.set_trace()

        result = []
        work_experiences = data.get('workExperience', [])
        if work_experiences:
            work_experiences = sorted(work_experiences, key=lambda x:x['workStartTime'], reverse=False)
        flag = False
        for work_experience in work_experiences:
            if company in work_experience.get("workCompany", ""):
                flag = True
            elif flag:
                return work_experience.get('workCompany', "")
        return ""

    @classmethod
    def _extract_avarge_salary(cls, data):
        work_experiences = data.get('workExperience', [])
        avage = 0
        count = 0
        for work_experience in work_experiences:
            salary = work_experience.get("workSalary", "")
            # import pdb; pdb.set_trace()
            if not isinstance(salary, str):
                continue

            if re.match("^[0-9]{1,10}-[0-9]{1,10}$", salary):
                min_salary, max_salary = salary.split("-")
            elif re.match("^[0-9]{1,10}-[0-9]{1,10}元\/月$", salary):
                min_salary, max_salary = salary[:-3].split("-")
            else:
                continue

            avage += (int(min_salary) + int(max_salary))/2
            count += 1

        return int(avage/count) if count > 0 else 0


