import unittest
import requests
from rest_apps import create_app
import json
import os
from settings import BASE_DIR

# host = "rembern.com"


host = "localhost"


class TestRestApi(unittest.TestCase):

    def test_link(self):
        with open(os.path.join(BASE_DIR, "resources", "one_cv.json"), 'r', encoding='utf8') as f:
            self.json_str = f.read()
        # json.loads(self.json_str, encoding='utf8')
        result = requests.post('http://{0}:18081/online/link'.format(host), data={'json': self.json_str})
        print(result.json())

    def test_paint(self):
        # with open(os.path.join(BASE_DIR, "resources", "one_cv.json"), 'r', encoding='utf8') as f:
        #     json_str = f.read()
        # json_data = json.loads(json_str)
        result = requests.post('http://{0}:18081/online/paint'.format(host), data={'_id': 'N7p7DBeE6lKOrYKUoDC(WA'})
        print(result.json())

    def test_kgize(self):
        result = requests.post('http://{0}:18081/online/kgize'.format(host), data={'_id': 'N7p7DBeE6lKOrYKUoDC(WA'})
        print(result.json())

    def test_bank_search(self):
        for mod in ['none','zhilian','upload']:
            print(mod)
            result = requests.get(
                'http://{0}:18081/online/talent_bank/search/{1}/{2}/{3}/{4}/{5}'.format(host, 'keyword', "机器学习算法工程师", 1, 10, mod))
            print(result.json())
            # print(result.text)
            result = requests.get(
                'http://{0}:18081/online/talent_bank/search/{1}/{2}/{3}/{4}/{5}'.format(host, 'education', "硕士", 1, 10, mod))
            print(result.json())
            result = requests.get(
                'http://{0}:18081/online/talent_bank/search/{1}/{2}/{3}/{4}/{5}'.format(host, 'source', "zhilian", 1, 10, mod))
            print(result.json())
            result = requests.get(
                'http://{0}:18081/online/talent_bank/search/{1}/{2}/{3}/{4}/{5}'.format(host, 'none', "none", 1, 10, mod))
            print(result.json())

    def test_similar(self):
        result = requests.get('http://{0}:18081/online/similar_jd/{1}/{2}/{3}'.format(host, "数据挖掘工程师", 2, 10))
        print(result.json())

    def test_experience(self):
        result = requests.get('http://{0}:18081/online/project_experience/{1}/{2}/{3}'.format(host, "数据挖掘工程师", 1, 10))
        print(result.json())

    def test_company_job(self):
        result = requests.get(
            'http://{0}:18081/online/get_company_by_job_title/{1}/{2}/{3}'.format(host, "数据挖掘工程师", 1, 10))
        print(result.json())

    def test_count_datas(self):
        result = requests.get("http://{0}:18081/online/count_talent_banks".format(host))
        print(result.json())

    def test_upload_data(self):
        files = {
            "file": open(os.path.join(BASE_DIR,'resources','智联招聘_常先生_中文_20190415_1555294995349.pdf'), 'rb')
        }
        result = requests.post("http://{0}:18081/online/upload/zhilian".format(host), files=files)
        print(result.text)

    def test_save_data(self):
        with open(os.path.join(BASE_DIR, "resources", "one_cv.json"), 'r', encoding='utf8') as f:
            self.json_str = f.read()
            # json.loads(self.json_str, encoding='utf8')
        result = requests.post('http://{0}:18081/online/save_to_bank'.format(host), data={'json': self.json_str})
        print(result.text)

    def test_count_tags(self):
        result = requests.get("http://{0}:18081/online/count_talent_tags".format(host))
        print(result.json())

    def test_jd_statics(self):
        result = requests.get("http://{0}:18081/online/jd_statics/{1}".format(host, '机器学习工程师'))
        print(result.json())

    def test_search_talent(self):
        result = requests.get("http://{0}:18081/online/sourcing/search_talent_bank/{1}/{2}/{3}".format(host,"机器学习", 1,10))
        print(result.json())

    def test_new_api(self):
        news_by_tag = requests.get("http://{0}:18081/online/get_news_by_tag/{1}/{2}/{3}".format(host,"数据挖掘工程师", 1,10))
        print(news_by_tag.json())
        news = requests.get("http://{0}:18081/online/get_news/{1}/{2}".format(host,1,10))
        print(news.json())
        news_by_domain = requests.get("http://{0}:18081/online/get_news_by_domain/{1}/{2}/{3}".format(host,"ai", 1,10))
        print(news_by_domain.json())

    def test_bank_search_with_name(self):
        for mod in ['none', 'zhilian', 'upload']:
            print(mod)
            result = requests.get(
                'http://{0}:18081/online/talent_bank/search_with_name/{6}/{1}/{2}/{3}/{4}/{5}'.format(host, 'keyword', "机器学习算法工程师", 1,
                                                                                        10, mod,'李先生'))
            print(result.json())
            # print(result.text)
            result = requests.get(
                'http://{0}:18081/online/talent_bank/search_with_name/{6}/{1}/{2}/{3}/{4}/{5}'.format(host, 'education', "硕士", 1, 10,
                                                                                        mod,'李先生'))
            print(result.json())
            result = requests.get(
                'http://{0}:18081/online/talent_bank/search_with_name/{6}/{1}/{2}/{3}/{4}/{5}'.format(host, 'source', "zhilian", 1,
                                                                                        10, mod,'李先生'))
            print(result.json())
            result = requests.get(
                'http://{0}:18081/online/talent_bank/search_with_name/{6}/{1}/{2}/{3}/{4}/{5}'.format(host, 'none', "none", 1, 10,
                                                                                        mod,'李先生'))
            print(result.json())


if __name__ == '__main__':
    unittest.main()
