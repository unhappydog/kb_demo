import unittest
from services.LinkerService import linkerService
from services.KgizeService import kgService
from settings import BASE_DIR
from utils.Utils import parse_data_to_dict
# from services.DataService import dataService
from services.tool_services.MongoService import mgService
import os


class TestRealCv(unittest.TestCase):

    def test_link(self):
        datas = mgService.query({}, 'kb_demo', 'kb_CV_origin')
        # if data:
        #     data = data[0]
        # else:
        #     print("Failed")
        for data in datas:
            self.cv = linkerService.parse(data)
            print(self.cv.__dict__)
            print(self.cv._id)
            result_academy = linkerService.link_academy(self.cv)
            print(result_academy)
            result_company = linkerService.link_company(self.cv)
            print(result_company)
            result_linked = linkerService.link_terminology(self.cv)
            print(result_linked)
            result_risks = linkerService.risk_recongnize(cv_dict=parse_data_to_dict(self.cv))
            print(result_risks)
            result = kgService.kgsizer(self.cv, result_linked, result_academy, result_company)
            print(result)
            result = kgService.kgsizer_4tupe(self.cv, result_linked, result_academy, result_company)
            print(result)
