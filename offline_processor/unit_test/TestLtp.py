import unittest
from services.tool_services.LtpService import ltpService
from settings import BASE_DIR
import os


class TestLtp(unittest.TestCase):
    def test_seg(self):
        word = "我来自北京青岛，我是中国人，我爱中国"
        words = ltpService.segment(word)
        tags = ltpService.postag(words)
        parses = ltpService.parse(words, tags)
        entitys = ltpService.recognize(words, tags)
        labels = ltpService.label(words, tags, parses)
        word_tags = zip(words, tags)
        for wrod, tag in word_tags:
            print("w{0}:{1}".format(wrod, tag))

        print("words:\n")
        for word in words:
            print(word)
        print("tags: \n")
        for tag in tags:
            print(tag)

        for parse in parses:
            print(parse)

        for entity in entitys:
            print(entity)

        for label in labels:
            print(label)


if __name__ == '__main__':
    unittest.main()
