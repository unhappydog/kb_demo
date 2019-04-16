from core.processors.BaseProcessor import BaseProcessor
from data_access.controller.NewController4Mongo import NewController4Mongo
import pandas as pd


class NewsProcessor(BaseProcessor):
    def __init__(self):
        super(NewsProcessor, self).__init__()
        self.new_controller = NewController4Mongo()

    def get_news(self, batch=None):
        """
        if batch is None, return data one by none.
        if batch is a number, return data one batch  by one batch,
        :param batch
        :return: a dataframe
        """
        if batch is not None:
            result = []
            for i in range(batch):
                for new in self.new_controller.get_datas_as_gen():
                    result.append(new)
            yield pd.DataFrame([new.__dict__ for new in result])
        else:
            for new in self.new_controller.get_datas_as_gen():
                yield pd.DataFrame([new.__dict__])
    pass
