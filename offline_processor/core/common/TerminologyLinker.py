# from data_access.controller.KBTerminologyController import KBTerminologyController
from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo
from services.tool_services.LtpService import ltpService
from utils.Logger import logging
from utils.Constants import REGEX_CN
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
                    self.enname_to_id[name] = data['_id']
        print("if")

    def recongnize_termnology(self, word_list, language='cn'):
        if language == 'cn':
            return [word for word in word_list if word in self.name_to_id.keys()]
        elif language == 'en':
            return [word for word in word_list if word in self.enname_to_id.keys()]
        else:
            logging.error("unrecongnize language")
            return None


if __name__ == '__main__':
    test = TerminologyLinker()
    # a =['7',]
    print(test.enname_to_id['7'])
    print(test.enname_to_id['10'])
