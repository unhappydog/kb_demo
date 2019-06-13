import unittest
# from services.tool_services.LtpService import ltpService
from services.AimlService import aimlService
from settings import BASE_DIR
import os


class TestAiml(unittest.TestCase):
    def test_aiml(self):
        texts = ['本科以上学历，计算机相关专业',
                 '硕士及以上学历，计算、图像、数据挖掘相关专业，熟悉机器学习算法',
                 'hello']
        for text in texts:
            print(aimlService.parse_info(text))


if __name__ == '__main__':
    unittest.main()
