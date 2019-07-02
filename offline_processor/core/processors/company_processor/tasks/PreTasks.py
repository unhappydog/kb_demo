from core.processors.company_processor import companyProcessor
from core.base.BaseTask import BaseTask


@companyProcessor.add_as_processors(order=1, stage=1)
class PreProcessor(BaseTask):
    def __init__(self):
        pass

    def fit(self, data):
        return data
