import sys
sys.path.append(".")
import unittest
from services.NLPService import nlpService
import os
from settings import BASE_DIR

class TestBert(unittest.TestCase):
    def test_ner(self):
        word = "我来自北京青岛，我是中国人，我爱中国"
        tags = nlpService.ner_recong_with_bert(word)
        print(tags)

if __name__ == '__main__':
    unittest.main()
