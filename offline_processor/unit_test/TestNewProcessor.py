import unittest
from core.processors.news_processor import newsProcessor
# from services.tool_services.mysql_service import mysqlService
from services.tool_services.MongoService import mgService
import pandas as pd


class TestNewProcessor(unittest.TestCase):
    def test_preprocess(self):
        # data = my
        data = mgService.query(query_cond=None, db="kb_demo",table="kb_news", skip=0, limit=100)
        data = pd.DataFrame(data)
        data = newsProcessor.start_process(data)
        print(data)


if __name__ == '__main__':
    unittest.main()
