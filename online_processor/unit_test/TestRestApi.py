import unittest
import requests
from rest_apps import create_app
import json
import os
from settings import BASE_DIR


class TestRestApi(unittest.TestCase):

    def test_init(self):
        result = requests.get("http://localhost:18081/hellow")
        self.assertEqual(result.text, 'hellow')

    def test_link(self):
        with open(os.path.join(BASE_DIR, "resources", "one_cv.json"), 'r', encoding='utf8') as f:
            self.json_str = f.read()
        # json.loads(self.json_str, encoding='utf8')
        result = requests.post('http://localhost:18081/online/link', data={'json': self.json_str})
        print(result.json())

    def test_paint(self):
        # with open(os.path.join(BASE_DIR, "resources", "one_cv.json"), 'r', encoding='utf8') as f:
        #     json_str = f.read()
        # json_data = json.loads(json_str)
        result = requests.post('http://localhost:18081/online/paint', data={'_id': 'N7p7DBeE6lKOrYKUoDC(WA'})
        print(result.text)


if __name__ == '__main__':
    unittest.main()
