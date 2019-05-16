import re
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
import datetime
from utils.Utils import remove_null


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
        #     data['projectExperience'][0]['projectEndTime'] = "至今"
    remove_null(data)

    return data


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
        self.contoller = KBTalentBankController4Mongo()

    def save(self, cv):
        data = self.contoller.get_data_by_id(_id=cv._id)
        if data:
            self.contoller.update_by_id(cv)
        else:
            self.contoller.insert_data(cv)

    @filter_data
    def search_by_name(self, name, page, limit, mode, keyword):
        # reg_pattern = "({0})".format("|".join(self.post_prefix))
        # if re.match(".+" + reg_pattern + "$", name):
        #     name = re.sub(reg_pattern,'', name)
        return self.contoller.get_datas_by_name(keyword=name, page=page, size=limit, mode=mode, name=keyword)

    @filter_data
    def search_by_education(self, education, page, limit, mode, name):
        # return self.
        return self.contoller.get_datas_by_education(education, page=page, size=limit, mode=mode, name=name)
        pass

    @filter_data
    def search_by_source(self, source, page, limit, mode, name):

        return self.contoller.get_datas_by_source(source=source, page=page, size=limit, mode=mode, name=name)

    @filter_data
    def search_by_keyword(self, keyword, page, limit):
        reg_pattern = "({0})".format("|".join(self.post_prefix))
        if re.match(".+" + reg_pattern + "$", keyword):
            keyword = re.sub(reg_pattern, '', keyword)
        return self.contoller.search_datas_by_keyword(keyword=keyword, page=page, size=limit)

    @filter_data
    def get_by_id(self, _id):
        data = self.contoller.get_data_by_id(_id=_id)
        if data:
            return data
        else:
            return []

    def delete_by_id(self, _id):
        self.contoller.delete_by_id(_id)

    def update(self, cv):
        # cv.updateTime = datetime.datetime.now()
        self.contoller.update_by_id(cv)

    @filter_data
    def get_datas(self, page, limit, mode, name):
        return self.contoller.get_datas_order_by(page=page, size=limit, mode=mode, name=name)

    def count_datas(self, cond):
        return self.contoller.count_datas(cond)

    def count_datas_update_after(self, time):
        return self.contoller.count_datas(cond={"updateTime": {"$gt": time}})

    def count_tags(self):
        return self.contoller.count_tags()
