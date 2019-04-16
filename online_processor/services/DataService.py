from utils.Tags import Singleton
from data_access.controller.CVController import CVController


@Singleton
class DataService:
    def __init__(self):
        self.cv_controller = CVController()

    def save(self, cv):
        self.cv_controller.insert_data(cv)


dataService = DataService()
