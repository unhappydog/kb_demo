from utils.Tags import Singleton
from core.kgnize.Kgnizer import Kgnizer


@Singleton
class KgizeService:
    def __init__(self):
        self.kgsizer_instance = Kgnizer()

    def kgsizer(self, cv, linked_info):
        return self.kgsizer_instance.kgnize(cv, linked_info)


kgService = KgizeService()
