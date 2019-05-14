from utils.Tags import Singleton
from core.kgnize.Kgnizer import Kgnizer
from utils.Logger import logging


@Singleton
class KgizeService:
    def __init__(self):
        self.kgsizer_instance = Kgnizer()

    def kgsizer_4tupe(self, cv, linked_info, linked_academy, linked_company):
        kg_data = self.kgsizer_instance.kgnize(cv, linked_info, linked_academy, linked_company)
        logging.info("the kgnized data is \n")
        logging.info(kg_data)
        kg_data = self.kgsizer_instance.json_to_4tupe(kg_data)
        logging.info("the json4tupe is \n")
        logging.info(kg_data)
        return kg_data

    def kgsizer(self, cv, linked_info, linked_academy, linked_company):
        return self.kgsizer_instance.kgnize(cv, linked_info, linked_academy, linked_company)


kgService = KgizeService()
