from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo
from data_access.controller.KBCompanyController4Mongo import KBCompanyController4Mongo
from threading import Lock
from tools.Jieba import Jieba

class JiebaService:
    _instance = None
    _lock = Lock()

    @classmethod
    def instance(cls):
        if JiebaService._instance is None:
            with JiebaService._lock:
                if JiebaService._instance is None:
                    JiebaService._instance = cls()
        return JiebaService._instance

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

        self.kb_company_controller = KBCompanyController4Mongo()
        company_names = self.kb_company_controller.get_datas()
        for data in company_names:
            if data['companyName']:
                user_dict.append(data['companyName'])
            if data['entName']:
                user_dict.append(data['entName'])
        self.jieba = Jieba()

    def segment(self, doc):
        return self.jieba.segment(doc)

    def postag(self, doc):
        if type(doc) == list:
            doc = "".join(doc)
        words = self.jieba.postag(doc)
        tags = [flag for word, flag in words]
        return tags

