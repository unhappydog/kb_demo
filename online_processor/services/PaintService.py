from utils.Tags import Singleton
from core.data_process.CVPaint import CVPaint
from data_access.controller.CVController4Mongo import CVController4Mongo


@Singleton
class PaintService:
    def __init__(self):
        self.cv_controller = CVController4Mongo()
        self.cv_paint_instance = CVPaint()

    def paint_cv(self, _id):
        cv = self.cv_controller.get_data_by_id(_id=_id)[0]
        return self.cv_paint_instance.cv_paint(cv)


paintService = PaintService()
