import unittest
# from services.LinkerService import linkerService
# from services.KgizeService import kgService
from services.TalentBankService import tbService
from settings import BASE_DIR
from utils.Utils import parse_data_to_dict
import os


class TestLBservice(unittest.TestCase):
    def test_search(self):
        print(tbService.search_by_keyword("知识图谱", 1,10))
        print(tbService.search_by_keyword("知识图谱工程师", 1, 10))

    def test_search_by_name(self):
        print(tbService.search_by_name("算法工程师", 2, 20, None))

    def test_count_tags(self):
        print(tbService.count_tags())

        count_num = tbService.count_tags()
        jobs = count_num['jobTitle']
        count = 0
        for k,v in jobs.items():
            count += v
        print(count)
