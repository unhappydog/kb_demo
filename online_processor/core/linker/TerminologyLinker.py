# from data_access.controller.KBTerminologyController import KBTerminologyController
from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo
from services.tool_services.LtpService import ltpService
from utils.Logger import logging
from utils.Constants import REGEX_CN
from core.linker.ACLinker import ACLinker
from string import punctuation as en_punc
from zhon.hanzi import punctuation as cn_punc
import re


class TerminologyLinker:
    def __init__(self):
        self.kb_terminology_controller = KBTerminologyController4Mongo()
        id_names = self.kb_terminology_controller.get_name_ids()
        self.name_to_id = {}
        self.enname_to_id = {}
        for data in id_names:
            if data['cnName']:
                for name in data['cnName']:
                    self.name_to_id[name] = data['_id']
            if data['engName']:
                for name in data['engName']:
                    self.enname_to_id[name.lower()] = data['_id']
        # name2id = dict(self.name_to_id, **self.enname_to_id)
        self.linker = ACLinker(self.name_to_id)
        self.linker_en = ACLinker(self.enname_to_id)

    def link(self, cv):
        """
        link property of cv
        :param cv:
        :param parser:
        :return:
        """
        result = dict()
        propertys = ['selfEvaluation']
        for property in propertys:
            result[property] = self.link_in_property(cv, property)

        if cv['skill']:
            if type(cv['skill']) == list:
                result['skill'] = self.link_in_sub_property(cv,'skill',['name'])
            else:
                result['skill'] = self.link_in_property(cv,'skill')

        # education experience, work experience, project experience, training experience, association experience
        link_dict = {'educationExperience': ['educationMajorDescription'],
                     'workExperience': ['workDescription', 'workDuty', 'workSummary'],
                     'projectExperience': ['projectName', 'projectDuty', 'projectSummary', 'projectDescription'],
                     'trainingExperience': ['trainingCourse', 'trainingDescription'],
                     'associationExperience': ['practiceName', 'practiceDescription']}
        for k, v in link_dict.items():
            result[k] = self.link_in_sub_property(cv, k, v)
        return result

    def _link(self, cv):
        """
        link property of cv
        :param cv:
        :param parser:
        :return:
        """
        result = dict()
        skill_tag = [] # get the skill tag of a cv
        propertys = ['selfEvaluation']
        for property in propertys:
            result[property] = self.link_in_property(cv, property)
            skill_tag += [data['name'] for  data in result[property]]

        if cv['skill']:
            if type(cv['skill']) == list:
                result['skill'] = self.link_in_sub_property(cv,'skill',['name'])
                skill_tag += [tag['name'] for data in result['skill'] for tag in data.get('name',[]) if 'name' in tag.keys()]
            else:
                result['skill'] = self.link_in_property(cv,'skill')
                skill_tag += [data['name'] for data in result['skill']]

        # education experience, work experience, project experience, training experience, association experience
        link_dict = {'educationExperience': ['educationMajorDescription'],
                     'workExperience': ['workDescription', 'workDuty', 'workSummary'],
                     'projectExperience': ['projectName', 'projectDuty', 'projectSummary', 'projectDescription'],
                     'trainingExperience': ['trainingCourse', 'trainingDescription'],
                     'associationExperience': ['practiceName', 'practiceDescription']}
        for k, v in link_dict.items():
            result[k] = self.link_in_sub_property(cv, k, v)
            for sub_property in v:
                skill_tag += [tag['name'] for data in result[k] for tag in data.get(sub_property,[]) if 'name' in tag.keys() and tag['name'] != '\n']
        return result, skill_tag

    def skill_tag(self, cv):
        _, skill_tags = self._link(cv)
        skill_tags = list(set(skill_tags))
        return skill_tags


    def link_in_sub_property(self, target_object, property_name, sub_propertys):
        """
        link terminology in sub class.et: workEperience
        :param target_object:
        :param property_name:
        :param sub_propertys:
        :return: list
        """
        result = []
        sub_object_list = target_object.__dict__[property_name]
        for sub_object in sub_object_list:
            temp_dict = {"tmp": "tmp"}
            for sub_property in sub_propertys:
                temp_dict[sub_property] = self.link_in_property(sub_object, sub_property)
            result.append(temp_dict)
        return result

    def link_in_property(self, target_object, property_name):
        """
        link terminology in property of target_object
        :param target_object:
        :param property_name:
        :return: a list of terminology detail
        """
        result = []
        if type(target_object) != dict:
            target_object = target_object.__dict__
        if property_name not in target_object.keys():
            return []
        if type(target_object[property_name]) == list:
            for text in target_object[property_name]:
                if type(text) == str:
                    # "link code"
                    term_list = self.simple_word_linker(text)
                    result.extend(term_list)
                else:
                    logging.warning("type of element in {0} is not str".format(property_name))
                pass
        elif type(target_object[property_name]) == str:
            # "link code"
            term_list = self.simple_word_linker(target_object[property_name])
            result.extend(term_list)
        else:
            logging.warning("type of {0} is neither str nor list".format(property_name))
        return result

    def linke_with_ac(self, text):
        linked_tupe = self.linker.link_text(text)
        result = [
            {'name': data[3][1],
             'start_index': data[0],
             'end_index': data[1]+1,
             'terminology_detail': self.kb_terminology_controller.get_data_by_id(data[3][0])[0].__dict__ if self.kb_terminology_controller.get_data_by_id(data[3][0]) else None
             } for data in linked_tupe if data[2] >= 1
        ]
        return sorted(result, key=lambda x:x['start_index'], reverse=False)

    def linke_with_ac_en(self, text):
        linked_tupe = self.linker_en.link_text(text)
        result = [
            {'name': data[3][1],
             'start_index': data[0],
             'end_index': data[1]+1,
             'terminology_detail': self.kb_terminology_controller.get_data_by_id(data[3][0])[0].__dict__ if self.kb_terminology_controller.get_data_by_id(data[3][0]) else None
             } for data in linked_tupe if data[2] >= 1
        ]
        result = [term for term in result if self.is_single_word(text,term)]
        return sorted(result, key=lambda x:x['start_index'], reverse=False)

    def is_single_word(self, text, term):
        word_dict = set(en_punc + cn_punc + " " + " ")
        start_index = term['start_index']
        end_index = term['end_index'] - 1
        if len(text) <= end_index + 1 or text[end_index+1] in word_dict or self.is_chinese(text[end_index+1]):
            if start_index == 0 or text[start_index - 1] in word_dict or self.is_chinese(text[start_index-1]):
                return True
        return False

    def is_chinese(self, word):

        return True if '\u4e00'<word<'\u9fff' else False


    def simple_word_linker(self, text):
        # return self.linke_with_ac(text)
        result = self.linke_with_ac(text)
        # 检查一个术语是否作为独立的单词存在
        text_en = text.lower()
        en_result = self.linke_with_ac_en(text_en)
        result = result + en_result

        result = sorted(result, key=lambda x: x['start_index'], reverse=False)
        # result = [term for term in result if self.is_good_result(term, result)]
        final_result = []
        for term in result:
            if self.is_good_result(term, final_result):
                final_result.append(term)
    #
        return final_result

    def recongnize_termnology(self, word_list, language='cn'):
        if language == 'cn':
            return [word for word in word_list if word in self.name_to_id.keys() and word != ""]
        elif language == 'en':
            return [word for word in word_list if word in self.enname_to_id.keys() and word != ""]
        else:
            logging.error("unrecongnize language")
            return None

    def recongnize_termnology_in_text(self, text):
        linked_tupe = self.linker.link_text(text)
        result = [data[3][1] for data in linked_tupe if data[2] >=2]
        return result

    def is_good_result(self, result_tupe, final_result):
        """
        如果该结果不和已知的结果中的每一个相交，那么这就是一个好的结果
        :param result_tupe:
        :param final_result:
        :return:
        """
        for final_result_tupe in final_result:
            if self.over_lap(result_tupe, final_result_tupe):
                return False
        return True

    def over_lap(self, a, b):
        """
        计算两个结果是否相交
        :param a:
        :param b:
        :return:
        """
        if a['start_index'] > b['end_index'] or a['end_index'] < b['start_index']:
            return False
        else:
            return True

