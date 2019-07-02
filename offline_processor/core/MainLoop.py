from services.tool_services.RedisServiceV2 import RedisService
from core.common.DataSources import DataSources
from utils.Logger import logging
import json
from data_access.controller.NewController4Mongo import NewController4Mongo
from data_access.controller.WeixinController4Mongo import WeixinController4Mongo
from data_access.controller.TalentController4Mongo import TalentController4Mongo
from data_access.controller.CommonController4Mongo import CommonController4Mongo
from core.processors.news_processor import newsProcessor
from core.processors.weixin_processor import weixinProcessor
from core.processors.talent_processor import talentProcessor
from core.processors.cv_processor import cvProcessor
import pandas as pd
import pickle

redisService = RedisService.instance()
processors = {
    DataSources.new: newsProcessor,
    DataSources.weixin: weixinProcessor,
    DataSources.talent: talentProcessor,
    DataSources.cv: cvProcessor

}
controllers = {
    DataSources.new: NewController4Mongo(),
    DataSources.weixin: WeixinController4Mongo(),
    DataSources.talent: TalentController4Mongo(),
    DataSources.cv: CommonController4Mongo(schema="kb_demo", table="kb_CV_2019")
}

data_types = {
    'news': DataSources.new,
    'weixin': DataSources.weixin,
    'talent': DataSources.talent,
    "cv": DataSources.cv
}


def main_loop(length=5):
    sub = redisService.channel("scrapy", 's')
    try:
        with open('temp.data','rb') as cache_file:
            dataBag = pickle.load(cache_file)
    except:
        dataBag = DataBag()

    try:
        while True:
            data_origin = sub()
            data = json.loads(data_origin[-1].decode())
            if '_meta' not in data:
                logging.error("data has no meta info")
                continue
            _meta_data = data['_meta']
            del data['_meta']
            data_type = _meta_data.get('dataType', None)
            data_type = data_types.get(data_type, None)
            if data_type is None:
                logging.error("unknow type {0}".format(_meta_data['dataType']))
                continue

            dataBag.put(data, data_type)
    finally:
        with open('temp.data', 'wb') as cache_file:
            pickle.dump(dataBag, cache_file, fix_imports=True)


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
        controller = controllers[datasource]
        data = pd.DataFrame(datas)
        data = processor.start_process(data)
        # controller.update_datas_from_df(data)
