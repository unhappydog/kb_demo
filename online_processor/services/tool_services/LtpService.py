from utils.Tags import Singleton
from tools.Ltp import Ltp
from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo


class LtpService:
    def __init__(self):
        self.kb_terminology_controller = KBTerminologyController4Mongo()
        id_names = self.kb_terminology_controller.get_name_ids()
        user_dict = []
        for data in id_names:
            if data['cnName']:
                for name in data['cnName']:
                    user_dict.append(name)
            if data['engName']:
                for name in data['engName']:
                    user_dict.append(name)
        self.ltp = Ltp(user_dict=user_dict)

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
