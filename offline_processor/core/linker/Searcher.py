from utils.Logger import logging
import resources
from data_access.controller.KBAcademyController4Mongo import KBAcademyController4Mongo
from data_access.controller.KBCompanyController4Mongo import KBCompanyController4Mongo
from services.tool_services.MongoService import mgService
from threading import Lock

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


    def link_city(self, city):
        data = mgService.query({'city': city}, 'kb_graph_cities', 'kb_graph_news_processed')
        if data:
            return data[0]
        return None

    def link_academy(self, school):
        """
        linking school names in cv to data in databases
        """
        school = re.sub("大学.*$", '大学', school) if '大学' in school else re.sub("学院.*$", "学院", school) if '学院' in school else school

        if not school:
            return None
        data = mgservice.query({"schoolName": {'$regex':name}}, 'kb_demo','kb_academy')
        if data:
            return data[0]
        return None

    def link_company(self, company):
        """
        linking companys in cv to data in databases
        """
        data = mgservice.query({"$or":[{"companyName":name}, {"entName":name}]},'kb_demo','kb_company')
        # if company.
        if data:
            return data[0]
        return None


