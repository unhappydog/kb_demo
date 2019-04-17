from services.tool_services.MongoService import mgService
import unittest


class TestMongoService(unittest.TestCase):
    def test_query(self):
        import time

        a = time.time()

        data = mgService.query({"schoolName": "武汉大学"},
                               'kb_demo',
                               'kb_academy')
        print(data)
        print(time.time() - a)