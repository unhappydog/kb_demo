import os
import platform
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
# from utils.Logger import logging
from settings import BASE_DIR


class Ltp:
    def __init__(self, user_dict =None):
        LTP_DIR = os.path.join(BASE_DIR, 'resources', 'ltp_data_v3.4.0')
        self.segmentor = Segmentor()

        user_dict_path = os.path.join(BASE_DIR, 'resources', 'lexicon')
        # 确定所有技术词已经在词典中了
        if user_dict is not None:
            self.verify_dict(user_dict_path, user_dict)
        self.segmentor.load_with_lexicon(os.path.join(LTP_DIR, "cws.model"), user_dict_path)

        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

        self.labeller = SementicRoleLabeller()
        if platform.system() == 'Windows':
            self.labeller.load(os.path.join(LTP_DIR, 'pisrl_win.model'))
        else:
            self.labeller.load(os.path.join(LTP_DIR, "pisrl.model"))

    def reload_dict(self, user_dict):
        LTP_DIR = os.path.join(BASE_DIR, 'resources', 'ltp_data_v3.4.0')
        user_dict_path = os.path.join(BASE_DIR, 'resources', 'lexicon')
        # 确定所有技术词已经在词典中了
        if user_dict is not None:
            self.verify_dict(user_dict_path, user_dict)
        self.segmentor.load_with_lexicon(os.path.join(LTP_DIR, "cws.model"), user_dict_path)

    def segment(self, doc):
        return self.segmentor.segment(doc)

    def postag(self, word_list):
        return self.postagger.postag(word_list)

    def recognize(self, word_list, tag_list):
        return self.recognizer.recognize(word_list, tag_list)

    def parse(self, word_list, tag_list):
        return self.parser.parse(word_list, tag_list)

    def label(self,word_list, tag_list, arcs):
        """

        :param word_list:
        :param tag_list:
        :param arcs: 依存句法结果
        :return: 语义角色标注结果
        """
        return self.labeller.label(word_list, tag_list, arcs)

    # def verify_dict(self, user_dict_path, user_dict):
    #     with open(user_dict_path, 'w+', encoding='utf-8') as f:
    #         word_list = f.read().split('\n')
    #         word_not_in_dict = set(user_dict) - set(word_list)
    #         if word_not_in_dict:
    #             logging.warning("there is {0}s word not in dict, adding them".format(len(word_not_in_dict)))
    #             f.write("\n".join(word_not_in_dict))
    #     pass
