import re
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
from core.talent_bank.TalentMap import TalentMap
import datetime
from utils.Utils import remove_null
from threading import Lock


def filter_data(func):
    def wrapper(*args, **kwargs):
        datas = func(*args, **kwargs)
        return [is_good(data) for data in datas]

    return wrapper


def is_good(data, min_length=1):
    check_list = {'workExperience': ['workDescription', 'workDuty', 'workSummary'],
                  'projectExperience': ['projectName', 'projectDuty', 'projectSummary', 'projectDescription'],
                  'trainingExperience': ['trainingCourse', 'trainingDescription']}
    # 'associationExperience': ['practiceName', 'practiceDescription']}
    for k, v in check_list.items():
        if data.get(k, None) is not None and data.get(k, None) != []:
            for sub_item in v:
                temp = []
                for dat in data[k]:
                    if dat.get(sub_item, None) and len(dat[sub_item]) < min_length:
                        dat[sub_item] = None
                    temp.append(dat)
                data[k] = temp

    if data.get('workExperience', None):
        data['workExperience'] = sorted(data['workExperience'], key=lambda x: x['workStartTime'], reverse=True)
        # if data['workExperience'][0]['workEndTime'] is None or data['workExperience'][0]['workEndTime'] == "":
        #     data['workExperience'][0]['workEndTime'] = "至今"
        tem_experi = []
        for experi in data['workExperience']:
            if experi['workEndTime'] is None or experi['workEndTime'] == '':
                experi['workEndTime'] = '至今'
            tem_experi.append(experi)
        data['workExperience'] = tem_experi
    if data.get('projectExperience', None):
        data['projectExperience'] = sorted(data['projectExperience'], key=lambda x: x['projectStartTime'], reverse=True)
        tem_experi = []
        for experi in data['projectExperience']:
            if experi['projectEndTime'] is None or experi['projectEndTime'] == '':
                experi['projectEndTime'] = '至今'
            tem_experi.append(experi)
        data['projectExperience'] = tem_experi

        # if data['projectExperience'][0]['projectEndTime'] is None or data['projectExperience'][0]['projectEndTime'] == "":
        #     data['projectExperience'][0]['projectEndTime'] =a "至今"
    remove_null(data)

    return data


def _switch_table_tag(func):
    def _func(self, *args, **kwargs):
        if 'talent_bank_id' in kwargs:
            talent_bank_id = kwargs['talent_bank_id']
            del kwargs['talent_bank_id']
            if talent_bank_id:
                with self.controller.switch_to_table(name_talent(talent_bank_id)):
                    return func(self, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)
    return _func


def name_talent(id):
    return "talent_bank_%s" %id

class TalentBank:
    post_prefix = [
        "研究员",
        "科学家",
        "技术专家",
        "专家",
        "资深工程师",
        "架构师",
        "资深科学家",
        "资深研究员",
        "资深架构师",
        "专家工程师",
        "首席科学家",
        "资深专员",
        "leader",
        "总监",
        "负责人",
        "资深",
        "架构",
        "算法专家",
        "技术总",
        "算法工程师",
        "研发工程师",
        "工程师",
        "初级工程师",
        "高级工程师",
        "中级工程师",
        "技术专员",
        "开发工程师",
        "工程师",
        "开发",
        "专员",
        "高级算法工程师",
        "研究员",
        "高级",
        "算法研发",
        "算法",
        "研发",
        "主管",
        "工程师",
        "助理工程师"
    ]

    def __init__(self):
        self.controller = KBTalentBankController4Mongo()

    @_switch_table_tag
    def save(self, cv, save_tag=True):
        data = self.controller.get_data_by_id(_id=cv['_id'])
        if data:
            if not save_tag:
                cv['tag'] = data[0]['tag']
            self.controller.update_by_id(cv)
        else:
            self.controller.insert_data(cv)

    @_switch_table_tag
    @filter_data
    def search_by_keyword(self, keyword, location, experience, educationDegree, page, limit, sort_by):

        reg_pattern = "({0})".format("|".join(self.post_prefix))
        if re.match(".+" + reg_pattern + "$", keyword):
            keyword = re.sub(reg_pattern, '', keyword)
        return self.controller.search_datas_by_keyword(keyword=keyword, location=location, experience=experience, educationDegree=educationDegree, page=page, size=limit,sort_by=sort_by)

    @_switch_table_tag
    @filter_data
    def get_by_id(self, _id):
        data = self.controller.get_data_by_id(_id=_id)
        if data:
            return data
        else:
            return []

    @_switch_table_tag
    def delete_by_id(self, _id):
        self.controller.delete_by_id(_id)

    @_switch_table_tag
    def update(self, cv):
        # cv.updateTime = datetime.datetime.now()
        self.controller.update_by_id(cv)

    @_switch_table_tag
    @filter_data
    def get_datas(self, page, limit, mode, name):
        return self.controller.get_datas_order_by(page=page, size=limit, mode=mode, name=name)

    @_switch_table_tag
    @filter_data
    def get_datas_by(self,keyword=None, location=None, update_time=None, experience=None, educationDegree=None, source=None, source_method=None, job_title=None, searchword=None,company=None, academy=None, skill_tag=None, tag=[],page=1, size=10, sort_by=None):
        return self.controller.get_datas_by(keyword,location, update_time, experience, educationDegree,source,source_method, job_title, searchword, company, academy, skill_tag, tag, -1, page, size,sort_by)

    @_switch_table_tag
    @filter_data
    def get_all_cv(self, company, academy, skill_tag, sort_by="updateTime", ascending=-1, page=1, size=10):
        return self.controller.get_all_cv(company, academy, skill_tag, sort_by, ascending, page, size)


    @_switch_table_tag
    @filter_data
    def count_column(self, column_name, cond=None):
        datas = self.controller.count_column(column_name, cond)
        return [data for data in datas if data.get(column_name)]

    @_switch_table_tag
    def get_cv_by_kanban(self, kanban_tag, job_title,page,size):
        return self.controller.get_datas_by_kanban(kanban_tag, job_title,page=page, size=size)

    def gen_map(self, company_name):
        return TalentMap.instance(KBTalentBankController4Mongo()).gen_map(company_name)

    def get_map_cv(self, company_name, in_office):
        return TalentMap.instance(KBTalentBankController4Mongo()).get_map_cv(company_name, in_office)

    def gen_chart_data(self, company_name, in_office, job_type, job_title):
        return TalentMap.instance(KBTalentBankController4Mongo()).gen_chart_data(company_name, in_office, job_type, job_title)
