import sys
sys.path.append(".")
import unittest
import requests
import json
import os
from settings import BASE_DIR
#host="rembern.com"
host="localhost"

class TestKB(unittest.TestCase):

    def test_expand(self):
        print("testing expand ")
        result = requests.get("http://{0}:18082/online/kb/expand_entity/{1}/{2}/{3}/{4}".format(host, "major", "英语", 'none', 100))
        self.assertEqual(result.status_code, 200)

    def test_demo(self):
        print("testing demo")
        result = requests.get("http://{0}:18082/online/kb/demo_entity/{1}/{2}/{3}".format(host, "true", "true", 'true'))
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
