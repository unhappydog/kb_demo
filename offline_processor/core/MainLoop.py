from services.tool_services.RedisServiceV2 import RedisService
from core.common.DataSources import DataSources
from utils.Logger import logging
import json
from core.processors.news_processor import newsProcessor
from core.processors.weixin_processor import weixinProcessor
from core.processors.talent_processor import talentProcessor
import pickle

redisService = RedisService.instance()
processors = {
    DataSources.new: newsProcessor,
    DataSources.weixin: weixinProcessor,
    DataSources.talent: talentProcessor
}
controllers = {
    DataSources.new: NewController4Mongo(),
    DataSources.weixin: WeixinController4Mongo(),
    DataSources.talent: TalentController4Mongo()
}

data_type = {
    'new': DataSources.new,
    'weixin': DataSources.weixin,
    'talent': DataSources.talent
}


def main_loop(length=5):
    sub = RedisService.channel("scrapy", 's')
    try:
        with open('temp.data','rb') as cache_file:
            dataBag = pickle.load(cache_file)
    except:
        dataBag = DataBag()

    try:
        while True:
            data_origin = sub()
            data = json.loads(data_origin[-1].decode())
            _meta_data = data['_meta']
            del data['_meta']
            data_type = data_type.get(_meta_data['dataType'], None)
            if data_type is None:
                logging.error("unknow type {0}".format(_meta_data['dataType']))
                continue
            dataBag.put(data, data_type)
    finally:
        with open('temp.data', 'wb') as cache_file:
            pickle.dump(dataBag, cache_file, fix_imports=True)


class DataBag:
    def __init__(self, max_length=5):
        self.bag = {}
        self.max_length = max_length

    def put(self, data, data_type):
        self.bag = self.bag.get(data_type, []) + [data]
        if len(self.bag.get(data_type)) >= 5:
            datas = self.bag.get(data_type)
            try:
                self.process(datas, data_type)
            except Exception as e:
                logging.exception()
            self.bag[data_type] = []
        return True

    def process(self, datas, datasource):
        processor = processors[datasource]
        controller = controllers[datasource]
        data = pd.DataFrame(datas)
        data = processor.start_process(data)
        controller.update_datas_from_df(data)
