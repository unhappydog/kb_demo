from utils.Tags import Singleton
from data_access.controller.CVController4Mongo import CVController4Mongo


@Singleton
class DataService:
    def __init__(self):
        self.cv_controller = CVController4Mongo()

    def save(self, cv):
        self.cv_controller.insert_data(cv)


dataService = DataService()
