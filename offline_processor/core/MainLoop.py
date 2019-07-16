from services.tool_services.RedisServiceV2 import RedisService
from redis.exceptions import RedisError, ConnectionError, TimeoutError
from core.common.DataSources import DataSources
from utils.Logger import logging
import json
# from data_access.controller.NewController4Mongo import NewController4Mongo
# from data_access.controller.WeixinController4Mongo import WeixinController4Mongo
# from data_access.controller.TalentController4Mongo import TalentController4Mongo
# from data_access.controller.CommonController4Mongo import CommonController4Mongo
from core.processors.news_processor import newsProcessor
from core.processors.weixin_processor import weixinProcessor
from core.processors.talent_processor import talentProcessor
from core.processors.cv_processor import cvProcessor
from core.processors.company_processor import companyProcessor
from core.processors.baidu_processor import baiduProcessor
from multiprocessing import Queue, Process
import pandas as pd
import pickle
import time

redisService = RedisService.instance()
processors = {
    DataSources.new: newsProcessor,
    DataSources.weixin: weixinProcessor,
    DataSources.talent: talentProcessor,
    DataSources.cv: cvProcessor,
    DataSources.company: companyProcessor,
    DataSources.baidubaipin: baiduProcessor

}
# controllers = {
#     DataSources.new: NewController4Mongo(),
#     DataSources.weixin: WeixinController4Mongo(),
#     DataSources.talent: TalentController4Mongo(),
#     DataSources.cv: CommonController4Mongo(schema="kb_demo", table="kb_CV_2019"),
#     DataSources.company: CommonController4Mongo(schema="kb_demo", table="kb_company")
# }

data_types = {
    'news': DataSources.new,
    'weixin': DataSources.weixin,
    'talent': DataSources.talent,
    "cv": DataSources.cv,
    "company": DataSources.company,
    'baipin_firm_basic': DataSources.baidubaipin
}


def main_loop(n_processor=8):
    sub = redisService.channel("scrapy", 's')
    multiProcessorBag = MultiProcessorBag(n_processor=n_processor)
    multiProcessorBag.start_processors()
    try:
        while True:
            try:
                data_origin = sub()
            except ConnectionError as e:
                logging.error("redis connection closed for some reason, try to reconnect after 1 s")
                time.sleep(1)
                sub = redisService.channel("scrapy", 's')
                continue
            except TimeoutError as e:
                logging.error("redis connection time out, try to reconnect after 1 s")
                time.sleep(1)
                sub = redisService.channel("scrapy", 's')
                continue

            data = json.loads(data_origin[-1].decode())
            multiProcessorBag.put(data)
    finally:
        multiProcessorBag.stop_all()

class DataBag:
    def __init__(self, max_length=5):
        self.bag = dict()
        self.max_length = max_length

    def put(self, data, data_type):
        self.bag[data_type] = self.bag.get(data_type, []) + [data]
        if len(self.bag.get(data_type)) >= 5:
            datas = self.bag.get(data_type)
            try:
                self.process(datas, data_type)
            except Exception as e:
                logging.exception("exception occured")
            self.bag[data_type] = []
        return True

    def process(self, datas, datasource):
        processor = processors[datasource]
        # controller = controllers[datasource]
        data = pd.DataFrame(datas)
        try:
            data = processor.start_process(data)
        except Exception as e:
            logging.error("some thing wrong")
            logging.exception("except as ", e)
        # controller.update_datas_from_df(data)

class MultiProcessorBag:
    def __init__(self, n_processor=4, batch=5):
        self.n_processor = 4
        self.batch = 5
        self.queue = Queue()
        self.processors = []

    def start_processors(self):
        for i in range(self.n_processor):
            process = Process(target=self.process, args=[self.queue])
            self.processors.append(process)
            process.start()

    def put(self, data):
        self.queue.put(data)

    def process(self, queue):
        dataBag = DataBag()
        while True:
            data = queue.get()
            if '_meta' not in data:
                logging.error('data has no meta info')
                continue
            _meta_data = data['_meta']
            del data['_meta']
            data_type = _meta_data.get('dataType', None)
            data_type = data_types.get(data_type, None)
            if data_type is None:
                logging.error("unknow type {0}".format(_meta_data['dataType']))
                continue
            dataBag.put(data, data_type)

    def stop_all(self):
        for p in self.processors:
            p.terminate()


