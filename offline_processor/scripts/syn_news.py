import sys
sys.path.append(".")
from data_access.controller.NewController4Mongo import NewController4Mongo
from data_access.controller.NewController import NewController
from services.tool_services.mysql_service import mysqlService
from services.tool_services.MongoService import mgService
from decimal import Decimal
from tqdm import tqdm


def syn_talent():
    for datas in mysqlService.execute("select * from kb_talent", generate=True):
        for data in datas:
            mgService.insert(data, 'kb_demo', 'kb_talent')
            print(data)


def syn_new():
    # for data in new_controller.get_news_as_gen():
    #     print(data)
    for datas in tqdm(mysqlService.execute_as_gen("select * from kb_news_2019 where PUBTIME > \"2019-07-08\"")):
        for data in datas:
            data['_id'] = data['ID']
            print("receving data {0}".format(data['_id']))
            try:
                mgService.insert(data, 'kb_demo', 'kb_news')
            except Exception as e:
                print(e)


def syn_weixin():
    for datas in mysqlService.execute_as_gen("select * from kb_weixin"):
        for data in datas:
            # doc = {}
            for k, v in data.items():
                if type(v) == Decimal:
                    data[k] = float(v)
            mgService.insert(data, 'kb_demo', 'kb_weixin')


def syn_talent():
    for datas in mysqlService.execute_as_gen("select * from kb_talent"):
        for data in datas:
            for k, v in data.items():
                if type(v) == Decimal:
                    data[k] = float(v)
            mgService.insert(data, 'kb_demo', 'kb_talent')

def syn_major():
    for datas in mysqlService.execute_as_gen("select * from kb_major"):
        for data in datas:
            for k, v in data.items():
                if type(v) == Decimal:
                    data[k] = float(v)
            mgService.insert(data, "kb_demo", "kb_major")


if __name__ == '__main__':
    syn_major()
    # syn_new()
    # syn_talent()
    # syn_weixin()
    # syn_talent()
    pass
