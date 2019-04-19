from utils.Tags import Singleton
from tools.Ltp import Ltp
from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo


class LtpService:
    def __init__(self):
        self.kb_terminology_controller = KBTerminologyController4Mongo()
        id_names = self.kb_terminology_controller.get_name_ids()
        self.user_dict = []
        for data in id_names:
            if data['cnName']:
                for name in data['cnName']:
                    self.user_dict.append(name)
            if data['engName']:
                for name in data['engName']:
                    self.user_dict.append(name)
        self.ltp = Ltp(user_dict=self.user_dict)

    def reload_dict(self, user_dict=[]):
        """
        使用提供的列表重新载入分词字典
        :param user_dict:
        :return:
        """
        self.user_dict= user_dict
        self.ltp.reload_dict(self.user_dict)

    def add_dict(self, user_dict=[]):
        """
        加入 新的 字典并重新载入
        :param user_dict:
        :return:
        """
        self.user_dict.extend(user_dict)
        self.ltp.reload_dict(self.user_dict)

    def segment(self, doc):
        return self.ltp.segment(doc)

    def postag(self, word_list):
        return self.ltp.postag(word_list)

    def recognize(self, word_list, tag_list):
        return self.ltp.recognize(word_list, tag_list)

    def parse(self, word_list, tag_list):
        return self.ltp.parse(word_list, tag_list)

    def label(self, word_list, tag_list, arcs):
        """

        :param word_list:
        :param tag_list:
        :param arcs: 依存句法结果
        :return: 语义角色标注结果
        """
        return self.ltp.label(word_list, tag_list, arcs)
        pass


ltpService = LtpService()
