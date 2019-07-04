from core.kb_core.KBCore import KBCore
from threading import Lock


class KBService:
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
        self.kbcore = KBCore()

    def find_entity(self, entity_label, entity_name=None, entity_id=None, limit=10):
        return self.kbcore.find_entity(entity_label, entity_name, entity_id, limit)

    def demo_entity(self, company, job, candidate, limit):
        return self.kbcore.demo_entity(company, job, candidate)
