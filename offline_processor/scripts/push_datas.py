import sys
sys.path.append(".")
from core.processors.news_processor import newsProcessor
from core.processors.weixin_processor import weixinProcessor
from core.processors.talent_processor import talentProcessor
from data_access.controller.NewController4Mongo import NewController4Mongo
from data_access.controller.WeixinController4Mongo import WeixinController4Mongo
from data_access.controller.TalentController4Mongo import TalentController4Mongo
from data_access.controller.CommonController4Mongo import CommonController4Mongo
from core.common.DataSources import DataSources
from services.tool_services.RedisServiceV2 import RedisService
from utils.Encoder import JSONEncoder
import click
import json
import time
redisService = RedisService.instance()


@click.command()
@click.option("--data_source", default='news', help='which datasource to push')
def push(data_source):
    source_dict = {'all':[DataSources.new, DataSources.talent, DataSources.weixin, DataSources.cv],
                   'news': DataSources.new,
                   'talent': DataSources.talent,
                   'weixin': DataSources.weixin,
                   'cv': DataSources.cv}
    source_name_dict = {v:k for k,v in source_dict.items() if k != 'all'}
    pusher = redisService.channel('scrapy','p')
    if data_source != 'all':
        data_source_types = [source_dict.get(data_source)]
    else:
        data_source_types = source_dict.get(data_source)

    for data_source_type in data_source_types:
        for data in get_datas(data_source_type):
            data['_meta'] = dict()
            data['_meta']['dataType'] = source_name_dict.get(data_source_type)
            data = json.dumps(data,ensure_ascii=False, cls=JSONEncoder)
            pusher(data)
            print(data)
            time.sleep(1)

def get_datas(data_source):
    controllers = {
            DataSources.new: NewController4Mongo(),
            DataSources.weixin: WeixinController4Mongo(),
            DataSources.talent: TalentController4Mongo(),
        DataSources.cv: CommonController4Mongo(schema="kb_demo", table="kb_CV_2019")
        }
    if type(data_source) == list:
        for every_data_source in data_source:
            controller = controllers.get(every_data_source)
            yield from controller.get_datas_as_gen()

    else:
        controller = controllers.get(data_source)
        yield from controller.get_datas_as_gen()

if __name__ == '__main__':
    push()