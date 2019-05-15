# from data_access.controller.KBTerminologyController import KBTerminologyController
from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo
from services.tool_services.LtpService import ltpService
from utils.Logger import logging
from utils.Constants import REGEX_CN
from core.linker.ACLinker import ACLinker
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

    def link(self, cv):
        """
        link property of cv
        :param cv:
        :param parser:
        :return:
        """
        result = dict()
        propertys = ['skills', 'selfEvaluation']
        for property in propertys:
            result[property] = self.link_in_property(cv, property)

        # education experience, work experience, project experience, training experience, association experience
        link_dict = {'educationExperience': ['educationMajorDescription'],
                     'workExperience': ['workDescription', 'workDuty', 'workSummary'],
                     'projectExperience': ['projectName', 'projectDuty', 'projectSummary', 'projectDescription'],
                     'trainingExperience': ['trainingCourse', 'trainingDescription'],
                     'associationExperience': ['practiceName', 'practiceDescription']}
        for k, v in link_dict.items():
            result[k] = self.link_in_sub_property(cv, k, v)
        return result

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
        if property_name not in target_object.__dict__.keys():
            return []
        if type(target_object.__dict__[property_name]) == list:
            for text in target_object.__dict__[property_name]:
                if type(text) == str:
                    # "link code"
                    term_list = self.simple_word_linker(text)
                    result.extend(term_list)
                else:
                    logging.warning("type of element in {0} is not str".format(property_name))
                pass
        elif type(target_object.__dict__[property_name]) == str:
            # "link code"
            term_list = self.simple_word_linker(target_object.__dict__[property_name])
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
             } for data in linked_tupe if data[2] >= 2
        ]
        return sorted(result, key=lambda x:x['start_index'], reverse=False)

    def simple_word_linker(self, text):
        # return self.linke_with_ac(text)
        result = self.linke_with_ac(text)
    # def simple_word_linker(self, text):
    #     """
    #     find the terminology in text
    #     :param text:
    #     :return: a list of terminology detail
    #     """
    #     result = []
    #
    #     # 中文直接进行字符串匹配
    #     for word in ltpService.segment(text):
    #         # for word in self.name_to_id.keys():
    #         if word in self.name_to_id.keys():
    #             start_index = text.rfind(word)
    #             end_index = start_index + len(word)
    #             # text[start_index:end_index] = ["s"]
    #             text = text[:start_index] + "_" * len(word) + text[end_index:]
    #             word_detail = self.kb_terminology_controller.get_data_by_id(self.name_to_id[word])
    #             if word_detail:
    #                 word_detail = word_detail[0].__dict__
    #             result.append({'name': word, 'start_index': start_index, 'end_index': end_index,
    #                            'terminology_detail': word_detail})
    #
        # 检查一个术语是否作为独立的单词存在
        text_en = text.lower()
        text_en_pure = re.sub(" *({0}|,|;|，|。|；|  |、|,|;|\n|\+|:)+ *".format(REGEX_CN), '__', text_en)
        text_en_pure_words = [word.strip() for word in text_en_pure.split("__")]
        text_en_pure_words = sorted(text_en_pure_words, key=lambda x: len(x), reverse=True)
        for en_word in text_en_pure_words:
            # en_word = en_word.strip(" ")
            if en_word in self.enname_to_id.keys():
                start_index = text_en.rfind(en_word)
                if start_index == -1:
                    continue
                end_index = start_index + len(en_word)
                text_en = text_en[:start_index] + "_" * len(en_word) + text_en[end_index:]

                word_detail = self.kb_terminology_controller.get_data_by_id(self.enname_to_id[en_word])
                if word_detail:
                    word_detail = word_detail[0].__dict__
                result.append({'name': en_word, 'start_index': start_index,
                               'end_index': end_index, 'terminology_detail': word_detail})

        result = sorted(result, key=lambda x: x['start_index'], reverse=False)
    #
        return result

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

