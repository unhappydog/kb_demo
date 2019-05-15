from services.DataService import dataService
import unittest
from data_access.models.CV import CV


class TestDataService(unittest.TestCase):
    # def test_save(self):
    #     # data= {'name':'test',
    #     #        'age':100,
    #     #        'test_data':'this is test',
    #     #        'test_data1': 'this is test',
    #     #        'test_data2': 'this is test',
    #     #        '_id':'111111'
    #     #        }
    #     cv = CV(_id='111111', phone='this is test', name='this is test', jobTitle='this is test')
    #
    #     dataService.save(cv)
    #     # dataService.ge
    #     print(dataService.get('111111'))
    #     dataService.delete('111111')

    # def test
    def test_jd_by_name(self):
        print(dataService.get_jd_by_name("数据挖掘", 1, 10))

    def test_new_related(self):
        print(dataService.get_news(1, 10))
        print(dataService.get_news_by_tag('数据挖掘工程师', 1, 10))
        print(dataService.get_news_by_domain("ai", 1, 10))
        print(dataService.get_news_by_domain('talent', 1, 10))
