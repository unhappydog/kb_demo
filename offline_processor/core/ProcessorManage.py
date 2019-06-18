import sys
sys.path.append(".")
from core.processors.news_processor import newsProcessor
from core.processors.weixin_processor import weixinProcessor
from core.processors.talent_processor import talentProcessor
from data_access.controller.NewController4Mongo import NewController4Mongo
from data_access.controller.WeixinController4Mongo import WeixinController4Mongo
from data_access.controller.TalentController4Mongo import TalentController4Mongo
from core.common.DataSources import DataSources
from multiprocessing import Queue, Process
import pandas as pd
import os


class ProcessorManager:
    def __init__(self):
        self.processors = {
            DataSources.new: newsProcessor,
            DataSources.weixin: weixinProcessor,
            DataSources.talent: talentProcessor,
            # DataSources.talent_bank:
        }

        self.controller = {
            DataSources.new: NewController4Mongo(),
            DataSources.weixin: WeixinController4Mongo(),
            DataSources.talent: TalentController4Mongo()
        }

    def execute_processor(self, datasource, batch):
        processor = self.processors[datasource]
        controller = self.controller[datasource]
        for datas in controller.get_batch_data(batch=batch):
            data = pd.DataFrame([data for data in datas])
            data = processor.start_process(data)
            controller.update_datas_from_df(data)
            # if_con = input("if coninue:")
            # if if_con == 'y':
            #     pass
            # else:
            #     return

    def multi_process_execute(self, datasource, batch, n_thread=2):
        processor = self.processors[datasource]
        controller = self.controller[datasource]
        q = Queue()
        threads = []
        for i in range(n_thread):
            p = Process(target=self.process, args=(q, datasource))
            print("starting thread {0}".format(i))
            p.start()

        for datas in controller.get_batch_data(batch=batch):
            q.put(datas)

    def process(self, q, datasource):
        processor = self.processors[datasource]
        controller = self.controller[datasource]
        while True:
            datas = q.get()
            print("{0} is processing data".format(os.getpid()))
            data = pd.DataFrame([data for data in datas])
            data = processor.start_process(data)
            controller.update_datas_from_df(data)


if __name__ == '__main__':
    process = ProcessorManager()
    # process.execute_processor(DataSources.new, 100)
    # process.execute_processor(DataSources.weixin, 100)
    process.execute_processor(DataSources.talent, 100)
    # process.multi_process_execute(DataSources.talent, 10)
