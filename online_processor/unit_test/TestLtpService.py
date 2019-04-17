from services.tool_services.LtpService import ltpService
import unittest


class TestLtpService(unittest.TestCase):
    def test_ltp(self):
        sencentes = "我说话你不要插嘴，好不啦"
        words = ltpService.segment(sencentes)
        tags = ltpService.postag(words)
        entities = ltpService.recognize(words, tags)
        parsers =ltpService.parse(words, tags)

        print(words)
        print(tags)
        print(entities)
        print(parsers)