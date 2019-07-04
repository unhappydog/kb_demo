from utils.Tags import Singleton
from data_access.controller.KBStopWordsController import KBStopWordsController
from tools.BertTool import BertTool
from services.tool_services.LtpService import LtpService
from services.tool_services.JiebaService import JiebaService
import re
from zhon import hanzi
import string
from settings import nlp_core
from threading import Lock


@Singleton
class NLPService:
    _instance = None
    _lock = Lock()

    @classmethod
    def instance(cls):
        if NLPService._instance is None:
            with NLPService._lock:
                if NLPService._instance is None:
                    NLPService._instance = cls()
        return NLPService._instance

    def __init__(self):
        self.stop_words = {}
        self.word_list = []
        self.stop_words_controller = KBStopWordsController()
        self.load_stopwords()
        if nlp_core == "ltp":
            self.nlp_core = LtpService.instance()
        elif nlp_core == 'jieba':
            self.nlp_core = JiebaService.instance()

    def load_stopwords(self):
        words = self.stop_words_controller.get_datas()
        word_list = [word.name for word in words]
        self.stop_words['cn'] = set(word_list)

    def seg_words(self, doc, remove_stop_words=True):
        if remove_stop_words:
            return [word for word in self.nlp_core.segment(doc) if word not in self.stop_words['cn']]
        else:
            return [word for word in self.nlp_core.segment(doc)]

    def tag_words(self, words):
        return [tag for tag in self.nlp_core.postag(words)]

    def recongize(self, words, tags):
        return [entity_tag for entity_tag in self.nlp_core.recognize(words, tags)]

    def sentencesize(self, doc):
        """
        分割文本为一个个的句子
        :param doc:
        :return:
        """
        if not type(doc) == str:
            return
        doc_origin = re.sub(r' +|	+|　+', '', doc.replace('\n', ' '))
        doc_origin = re.sub(r"[%s]+" % (hanzi.non_stops + string.punctuation), "", doc_origin)
        docs = [doc for doc in re.split(r'[%s]+' % (hanzi.stops), doc_origin) if len(doc) >= 1]
        return docs

    def ner_recong(self, doc):
        docs = self.sentencesize(doc)
        result = []

        for doc in docs:
            words = self.seg_words(doc, False)
            tags = self.tag_words(words)
            ners = self.recongize(words, tags)
            result.extend(zip(words, ners))
        result = [word for word in result if word[1] != 'O']
        final_result = []
        temp_word = []
        for word in result:
            word_pos, word_tag = word[1].split('-')
            temp_word.append(word[0])
            if word_pos == 'S' or word_pos == 'E':
                final_result.append(("".join(temp_word), word_tag))
                temp_word = []
        return final_result

    def ner_recong_with_bert(self, doc):
        docs = self.sentencesize(doc)
        result = []
        for doc in docs:
            tags = BertTool.ner(doc)
            words = list(doc)
            result.extend(zip(words, tags))
        final_result = []
        temp_word = []
        for word in result:
            if '-' not in word[1]:
                continue
            word_pos, word_tag = word[1].split('-')
            temp_word.append(word[0])
            if word_pos == 'S' or word_pos == 'E':
                final_result.append(("".join(temp_word), word_tag))
                temp_word = []
        return final_result

nlpService = NLPService()
