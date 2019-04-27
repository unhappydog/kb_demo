import unittest
import requests
from rest_apps import create_app
import json
import os
from settings import BASE_DIR

host = "centos1"
# host = "localhost"


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
        print(result.text)

    def test_kgize(self):
        result = requests.post('http://{0}:18081/online/kgize'.format(host), data={'_id': 'N7p7DBeE6lKOrYKUoDC(WA'})
        print(result.json())

    def test_bank_search(self):
        result = requests.get('http://{0}:18081/online/talent_bank/search/{1}/{2}/{3}'.format(host, "机器学习算法工程师", 1, 10))
        print(result.text)

    def test_similar(self):
        result = requests.get('http://{0}:18081/online/similar_jd/{1}/{2}/{3}'.format(host, "数据挖掘工程师", 2, 10))
        print(result.json())

    def test_experience(self):
        result = requests.get('http://{0}:18081/online/project_experience/{1}/{2}/{3}'.format(host, "图像算法", 1, 10))
        print(result.json())

    def test_company_job(self):
        result = requests.get('http://{0}:18081/online/get_company_by_job_title/{1}/{2}/{3}'.format(host, "数据挖掘工程师", 1, 10))
        print(result.json())


if __name__ == '__main__':
    unittest.main()
