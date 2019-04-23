from utils.Tags import Singleton
from core.linker.Linker import Linker
from core.parser.CVParser import CVParser
from core.linker.TerminologyLinker import TerminologyLinker
from core.riskPoint.Risk import riskPoint


@Singleton
class LinkerService:

    def __init__(self):
        self.linker = Linker()
        self.parser = CVParser()
        self.terminology = TerminologyLinker()

    def link_academy(self, cv):
        return self.linker.link_academy(cv)

    def link_company(self, cv):
        return self.linker.link_company(cv)

    def link_terminology(self, cv):
        return self.terminology.link(cv)

    def parse(self, cv_json):
        return self.parser.parse(cv_json)

    def recongnize_terminology(self, word_list, language='cn'):
        return self.terminology.recongnize_termnology(word_list,language)

    def risk_recongnize(self, cv_dict):
        temp_object = riskPoint()
        risk_points = temp_object.identification(cv_dict)
        del temp_object
        return risk_points


linkerService = LinkerService()
