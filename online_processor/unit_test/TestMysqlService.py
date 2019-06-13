from services.tool_services.mysql_service import mysqlService
import unittest
import time

class TestMongoService(unittest.TestCase):
    def test_query(self):


        a = time.time()
        print(mysqlService.execute("show databases;"))
        print(mysqlService.execute("use jiaotong;", "show tables;"))
        print(time.time() - a)