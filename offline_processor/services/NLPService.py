from utils.Tags import Singleton
from services.tool_services.LtpService import ltpService
from data_access.controller.KBStopWordsController import KBStopWordsController
import re
from zhon import hanzi
import string

@Singleton
class NLPService:
    def __init__(self):
        self.stop_words = {}
        self.word_list = []
        self.stop_words_controller = KBStopWordsController()
        self.load_stopwords()

    def load_stopwords(self):
        words = self.stop_words_controller.get_datas()
        word_list = [word.name for word in words]
        self.stop_words['cn'] = set(word_list)

    def seg_words(self, doc):
        return [word for word in ltpService.segment(doc) if word not in self.stop_words['cn']]

    def tag_words(self, words):
        return [tag for tag in ltpService.postag(words)]

    def recongize(self, words, tags):
        return [entity_tag for entity_tag in ltpService.recognize(words, tags)]

    def sentencesize(self, doc):
        """
        分割文本为一个个的句子
        :param doc:
        :return:
        """
        doc_origin = re.sub(r' +|	+|　+', '', doc.replace('\n', ' '))
        doc_origin = re.sub(r"[%s]+" % (hanzi.non_stops + string.punctuation), "", doc_origin)
        docs = [doc for doc in re.split(r'[%s]+' % (hanzi.stops), doc_origin) if len(doc) >= 1]
        return docs


nlpService = NLPService()

