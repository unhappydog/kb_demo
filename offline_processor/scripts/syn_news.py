from data_access.controller.NewController4Mongo import NewController4Mongo
from data_access.controller.NewController import NewController
from services.tool_services.mysql_service import mysqlService
from services.tool_services.MongoService import mgService


def syn_talent():
    for datas in mysqlService.execute("select * from kb_talent", generate=True):
        for data in datas:
            mgService.insert(data, 'kb_demo', 'kb_talent')
            print(data)


def syn_new():
    # for data in new_controller.get_news_as_gen():
    #     print(data)
    for datas in mysqlService.execute("select * from kb_news", generate=True):
        for data in datas:
            mgService.insert(data, 'kb_demo', 'kb_news')
            print(data)


if __name__ == '__main__':
    # syn_new()
    syn_talent()
