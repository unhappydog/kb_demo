from core.processors.news_processor import newsProcessor
from data_access.controller.NewController4Mongo import NewController4Mongo
from core.common.DataSources import DataSources
import pandas as pd


class ProcessorManager:
    def __init__(self):
        # self.newsProcessor = newsProcessor
        # self.controller = NewController4Mongo()
        self.processors = {
            DataSources.new: newsProcessor
        }

        self.controller = {
            DataSources.new: NewController4Mongo()
        }

    def execute_processor(self, datasource,  batch):
        processor = self.processors[datasource]
        controller = self.controller[datasource]
        for datas in controller.get_batch_data(batch=batch):
            data = pd.DataFrame([data for data in datas])
            data = processor.start_process(data)
            controller.update_datas_from_df(data)


if __name__ == '__main__':
    process = ProcessorManager()
    process.execute_processor(DataSources.new, 100)
