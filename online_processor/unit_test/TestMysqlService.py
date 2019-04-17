from services.tool_services.mysql_service import mysqlService
import unittest


class TestMongoService(unittest.TestCase):
    def test_query(self):
        import time

        a = time.time()
        print(mysqlService.execute("show databases;"))
        print(mysqlService.execute("use jiaotong;", "show tables;"))
        print(time.time() - a)