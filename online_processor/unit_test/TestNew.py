import sys
sys.path.append(".")
import unittest
from unittest import mock
import requests
from rest_apps import create_app
import json
import os
from settings import BASE_DIR

host="localhost"

class TestNews(unittest.TestCase):

    def test_get_by_tags(self):
        print("testing get by tags")
        result = requests.get("http://{0}:18082/online/get_news_by_tag/{1}/{2}/{3}".format(host, '模式识别',1,10))
        self.assertEqual(result.status_code, 200)

    def test_get_news(self):
        print("testing get news")
        result = requests.get("http://{0}:18082/online/get_news/{1}/{2}".format(host,1,10))
        self.assertEqual(result.status_code, 200)

    def test_get_by_domain(self):
        print("testing get by domain")
        result = requests.get("http://{0}:18082/online/get_news_by_domain/{1}/{2}/{3}".format(host, 'talent',1,10))
        self.assertEqual(result.status_code, 200)

    def test_get_by_company(self):
        print("testing get by company")
        result = requests.get("http://{0}:18082/online/get_news_by_company/{1}/{2}/{3}".format(host, '京东',1,10))
        self.assertEqual(result.status_code, 200)



if __name__ == '__main__':
    unittest.main()
