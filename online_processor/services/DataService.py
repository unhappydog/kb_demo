from utils.Tags import Singleton
from data_access.controller.CVController4Mongo import CVController4Mongo


@Singleton
class DataService:
    def __init__(self):
        self.cv_controller = CVController4Mongo()

    def save(self, cv):
        if self.cv_controller.get_data_by_id(_id=cv._id):
            self.cv_controller.update_by_id(cv)
        else:
            self.cv_controller.insert_data(cv)

    def get(self, id):
        data = self.cv_controller.get_data_by_id(_id=id)
        if data:
            return data[0]
        else:
            return None

    def delete(self, id):
        return self.cv_controller.delete_by_id(_id=id)


dataService = DataService()
