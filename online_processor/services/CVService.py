from utils.Tags import Singleton
from core.parser.CVParser import CVParser
from core.cvprase.main import CV_main

@Singleton
class CVService:
    def __init__(self):
        self.parser = CVParser()

    def parse(self, cv_json):
        return self.parser.parse(cv_json)

    def parse_from_local(self, path):
        cv_main = CV_main(path)
        return cv_main.main_prase()


cv_service = CVService()
