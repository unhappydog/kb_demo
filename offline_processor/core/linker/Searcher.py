from utils.Logger import logging
import resources
from services.tool_services.MongoService import mgService
from threading import Lock
from core.linker.CompanyNameMapper import CompanyNameMapper

import re


class Searcher:
    _instance = None
    _lock = Lock()

    @classmethod
    def instance(cls):
        if Searcher._instance is None:
            with Searcher._lock:
                if Searcher._instance is None:
                    Searcher._instance = Searcher()
        return Searcher._instance


    def search_city(self, city):
        if not city.endswith("市") and not city.endswith("区"):
            city = city + "市"
        data = mgService.query({'city': city}, 'kb_graph_cities', 'kb_graph_news_processed')
        if data:
            return data[0]
        return None

    def search_project(self, project):
        data = mgService.query({'projectName':project}, 'kb_demo','kb_project_experience')
        if data:
            return data[0]
        return None

    def search_academy(self, school):
        """
        linking school names in cv to data in databases
        """
        school = re.sub("大学.*$", '大学', school) if '大学' in school else re.sub("学院.*$", "学院", school) if '学院' in school else school

        if not school:
            return None
        data = mgService.query({"schoolName": {'$regex':school}}, 'kb_demo','kb_academy')
        if data:
            return data[0]
        return None

    def search_company(self, company):
        """
        linking companys in cv to data in databases
        """
        company = CompanyNameMapper.get_full_name(company)
        data = mgService.query({"$or":[{"companyName":company}, {"entName":company}]},'kb_demo','kb_company',projection={
            "_id":1,
            "companyName":1,
            "establishedDate":1,
            'companyScale':1,
            'companyLocation':1,
            'brief':1,
            'dom':1,
            'companyType':1,
            'regCapital':1
        })
        if data:
            return data[0]
        return None

    def search_skill(self, term):
        data = mgService.query({"name": term}, 'kb_demo', 'kb_terminology')
        if data:
            return data[0]
        return None

    def search_major(self, major):
        data = mgService.query({"name":major}, 'kb_demo', 'kb_major')
        if data:
            return data[0]
        return None


