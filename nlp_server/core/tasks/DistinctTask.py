from threading import Lock
from core.base.data.LSHBasedFixSizeHash import LSHBasedFixSizeHash
from datasketch import MinHash
from services.NLPService import NLPService


class DistinctTask:
    _lock = Lock()
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.data = LSHBasedFixSizeHash()
        self.nlp_service = NLPService.instance()

    def add(self, data, min_score=0.7):
        docs = self.nlp_service.sentencesize(data)
        words = [word for doc in docs for word in self.nlp_service.seg_words(doc)]
        m = MinHash()
        for word in words:
            m.update(word.encode())
        m_score = self.data.get_max_similar(m)
        self.data.add(m)
        if m_score > min_score:
            return False
        else:
            return True

