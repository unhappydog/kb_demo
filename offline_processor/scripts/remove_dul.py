from services.tool_services.MongoService import mgService


def re_dul():
    # datas = mgService.query({'$or': [{'ISBAD': 1}, {'ISREPLICATE': 1}]}, 'kb_demo', 'kb_talent')
    # datas = mgService.re
    datas = mgService.remove_dul("companyName", 'kb_demo', 'kb_company')
    print(len(datas))
    for data in datas:
        # print("deleting {0}".format(data['id']))
        print(data)
        mgService.delete({'_id':data['_d_id']}, 'kb_demo', 'kb_company')


if __name__ == '__main__':
    re_dul()
