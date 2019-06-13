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

    def get_company_info(self, name):
        return self.linker.get_company_info(name)

    def link_terminology(self, cv):
        return self.terminology.link(cv)

    def gen_skill_tag(self, cv):
        return self.terminology.skill_tag(cv)

    def link_terminology_in_text(self, text):
        return self.terminology.simple_word_linker(text)

    def parse(self, cv_json):
        return self.parser.parse(cv_json)

    def recongnize_terminology(self, word_list, language='cn'):
        return self.terminology.recongnize_termnology(word_list, language)

    def risk_recongnize(self, cv_dict):
        temp_object = riskPoint()
        risk_points = temp_object.identification(cv_dict)
        del temp_object
        return risk_points

    def link_jd(self, jd):
        columns = ["requirement", "duty"]
        return {
            column: self.link_terminology_in_text(jd[column]) for column in columns
        }


linkerService = LinkerService()
if __name__ == '__main__':
    print(linkerService.link_terminology_in_text(" canal+kafka+spark+mysql+es CNN 为算法组提供实时特征产"))
