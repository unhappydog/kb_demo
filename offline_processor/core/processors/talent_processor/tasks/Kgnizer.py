from core.processors.talent_processor import talentProcessor
from core.base.BaseTask import BaseTask
from core.processors.talent_processor.tasks.KgPropertyList import KgPropertyList
from zhon import hanzi
from utils.Encoder import JSONEncoder
import json
import re


@talentProcessor.add_as_processors(stage=1, order=1, skill_column='skills', education_column='Education',
                                   jobDescription='JobDescription', salary='Salary', City='City',
                                   Experience='Experience', Welfare='Welfare', company='Company', graph_column='graph',
                                   jobName="Name", Duty="duty", Require="requirement")
class Kgnizer(BaseTask):
    pattern_dict = {
        "工作职责": {"负责": [{'pattern': "负责.*$",
                         'post': [2]}],
                 "参与": [{'pattern': "参与.*$",
                         'post': [2]}],
                 "设计": [{'pattern': "设计.*",
                         'post': [2]}]},
        "加分项": {
        },
        "经验要求": {
            "熟悉": [{'pattern': "熟悉.*",
                    'post': [2]}],
            "经验": [{'pattern': "具有.*经验",
                    'post': [2, -2]}]
        },
        "教育背景": {
            '专业': [{
                'pattern': ',.*专业',
                'post': [1, -2]
            }]
        },
        "优先条件": {
            "优先": [{'pattern': "熟悉.*优先",
                    'post': [2, -2]}]
        }
    }

    def __init__(self, skill_column, education_column, jobDescription, salary, City, Experience, Welfare, company,
                 graph_column, jobName, Duty, Require):
        self.skill_column = skill_column
        self.education_column = education_column
        self.jobDescription = jobDescription
        self.salary = salary
        self.City = City
        self.Experience = Experience
        self.Welfare = Welfare
        self.company = company
        self.graph = graph_column
        self.jobName = jobName
        self.duty = Duty
        self.require = Require

    def fit(self, data):
        data[self.duty] = data[self.jobDescription].apply(lambda x: self.preprocess_des(x)[0])
        data[self.require] = data[self.jobDescription].apply(lambda x: self.preprocess_des(x)[1])
        data[self.graph] = data.apply(lambda x: self.kgnize(x), axis=1)
        return data

    def preprocess_des(self, des):
        duty_key_words = ['岗位职责', '职位描述', '职责', '工作职责', '职责描述']
        required_key_words = ['任职要求', '任职资格', '岗位要求']

        duty_pattern = "|".join(duty_key_words)
        required_pattern = "|".join(required_key_words)
        pattern = r".*({0}).*({1}).*".format(duty_pattern, required_pattern)
        pattern_reverse = r".*({0}).*({1}).*".format(required_pattern, duty_pattern)
        if re.match(pattern, des):
            # duty_des, required_des = re.split(required_pattern, des)
            splited_des = re.split(required_pattern, des)
            if len(splited_des) == 2:
                duty_des, required_des = splited_des
                duty_des = re.split(duty_pattern, duty_des)[1]
                duty_des = duty_des.strip("：")
                required_des = required_des.strip("：")
            else:
                required_des = None
                duty_des = None
        elif re.match(pattern_reverse, des):
            # required_des, duty_des = re.split(duty_pattern, des)
            splited_des = re.split(duty_pattern, des)
            if len(splited_des) == 2:
                required_des, duty_des = splited_des
                required_des = re.split(required_pattern, required_des)[1]
                duty_des = duty_des.strip("：")
                required_des = required_des.strip("：")
            else:
                required_des = None
                duty_des = None
        else:
            required_des = None
            duty_des = None
        if required_des:
            required_des = "<br/>".join([doc for doc in re.split(r'[%s]+' % (hanzi.stops+";"), required_des) if len(doc) >= 1])
        if duty_des:
            duty_des = "<br/>".join([doc for doc in re.split(r'[%s]+' % (hanzi.stops +";"), duty_des) if len(doc) >= 1])
        return duty_des, required_des

    def kgnize(self, x):
        info = self.extract_info_from_des(x[self.jobDescription])
        print(info)
        cv = {
            "name": x[self.jobName],
            "_empty": [{"职位要求": {
                "_empty": [
                    {"加分项": info['加分项']},
                    {"优先条件": info['优先条件']},
                    {"经验要求": info['经验要求']},
                    {"技能": {
                        "_empty": x[self.skill_column]
                    }},
                    {"教育背景": info['教育背景']}]
            }},
                {"基础信息": {
                    "部门": "",
                    "城市": x[self.City],
                    "学历要求": x[self.education_column],
                    "工作经验": x[self.Experience],
                    "薪资": x[self.salary]
                }},
                {"职位福利": {
                    "_empty": x[self.Welfare].split(",") if x[self.Welfare] is not None else ""
                }},
                {"工作职责": info['工作职责']}]
        }
        result = self.json2tupe(cv)
        print(result)
        result = json.dumps(result, ensure_ascii=False, cls=JSONEncoder)
        return result

    def extract_info_from_des(self, des):
        des_list = re.split("。|;|；|\n|[0-9]{1,2}(， |\.|。|;|；|:|：| |、|,)", des.strip())
        pattern_name_list = ["工作职责", "优先条件", "教育背景", "经验要求", "加分项"]
        result = {
        }
        for doc in des_list:
            print(doc)
            if not doc:
                continue
            for name in pattern_name_list:
                if name not in result.keys():
                    result[name] = {}
                for k, v in self.pattern_dict[name].items():
                    for sub_v in v:
                        pattern = sub_v['pattern']
                        post = sub_v['post']
                        match_info = re.findall(pattern, doc)
                        if match_info:
                            for info in match_info:
                                if k in result[name].keys():
                                    result[name][k].append(self.extruct_info(post, info))
                                else:
                                    result[name][k] = [self.extruct_info(post, info)]
        return result

    def extruct_info(self, info_pos, info):
        if len(info_pos) <= 1:
            return info[info_pos[0]:]
        else:
            return info[info_pos[0]:info_pos[1]]

    def json2tupe(self, kg_jd):
        kg_property_list = KgPropertyList()
        root_id = kg_property_list.push_property(kg_jd['name'])
        for base_property in kg_jd.keys():
            if base_property == 'name':
                continue
            else:
                sub_value = kg_jd[base_property]
                if type(sub_value) == list or type(sub_value) == dict:
                    self.kgize_subitem_parse_line(kg_property_list, base_property, sub_value, root_id)
                else:
                    sub_id = kg_property_list.push_property(sub_value)
                    kg_property_list.push_path(sub_id, root_id, base_property, None)

        return {
            "ids": kg_property_list.id_table,
            # "edges": kg_property_list.property_list
            "edges": list(
                map(lambda x: (x[0], x[1], None, x[3]) if x[2] == "_empty" else x, kg_property_list.property_list))
        }
        pass

    def kgize_subitem_parse_line(self, kg_property_list, key, value, par_id):
        if type(value) == list:
            for item in value:
                self.kgize_subitem(kg_property_list, key, item, par_id)
        elif type(value) == dict:
            for base_property in value.keys():
                sub_value = value[base_property]
                if type(sub_value) == list or type(sub_value) == dict:
                    self.kgize_subitem(kg_property_list, base_property, sub_value, par_id)
                else:
                    sub_id = kg_property_list.push_property(sub_value)
                    kg_property_list.push_path(sub_id, par_id, base_property, None)

    def kgize_subitem(self, kg_property_list, key, value, par_id):
        if type(value) == list:
            for item in value:
                self.kgize_subitem(kg_property_list, key, item, par_id)
        elif type(value) == dict:
            for base_property in value.keys():
                sub_value = value[base_property]
                if type(sub_value) == dict:
                    sub_id = kg_property_list.push_property(base_property)
                    kg_property_list.push_path(sub_id, par_id, key, None)
                    self.kgize_subitem_parse_line(kg_property_list, base_property, sub_value, sub_id)
                elif type(sub_value) == list:
                    print("unexpected list got")
                else:
                    sub_id = kg_property_list.push_property(sub_value)
                    kg_property_list.push_path(sub_id, par_id, base_property, None)
        else:
            sub_id = kg_property_list.push_property(value)
            kg_property_list.push_path(sub_id, par_id, key, None)
