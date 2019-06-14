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
# host="rembern.com"

class TestUser(unittest.TestCase):

    def test_follow(self):
        print("testing follow")
        result = requests.get("http://{0}:18082/online/user/follow/{1}/{2}/{3}/{4}".format(host, "1",'华为','北京师范大学','模式识别'))
        print(result.json())
        self.assertEqual(result.status_code, 200)
        result = requests.get("http://{0}:18082/online/user/follow/{1}/{2}/{3}/{4}".format(host, "2",'none','首都经济贸易大学','none'))
        print(result.json())
        self.assertEqual(result.status_code, 200)

        print("testing unfollow")
        result = requests.get("http://{0}:18082/online/user/unfollow/{1}/{2}/{3}/{4}".format(host, "1",'华为','北京师范大学','模式识别1'))
        self.assertEqual(result.status_code, 200)

    def test_get_interest(self):
        print("testing get interests")
        result = requests.get("http://{0}:18082/online/user/get_interests/{1}/{2}/{3}/{4}".format(host, "2",1,1,1))
        print(result.json())
        self.assertEqual(result.status_code, 200)
        result = requests.get("http://{0}:18082/online/user/get_interests/{1}/{2}/{3}/{4}".format(host, "1",1,1,1))
        print(result.json())
        self.assertEqual(result.status_code, 200)

    # def test_link_v2(self):
    #     print('testing link v2')
    #     with open(os.path.join(BASE_DIR, "resources", "one_cv.json"), 'r', encoding='utf8') as f:
    #         self.json_str = f.read()
    #     # json.loads(self.json_str, encoding='utf8')
    #     result = requests.post('http://{0}:18082/online/linkv2/1'.format(host), data={'json': self.json_str})
    #     # print(result.json())    # 
    #     with open("link_result.txt", 'w', encoding='utf8') as f:
    #         f.write(json.dumps(result.json(), ensure_ascii=False))
    #     self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
