from services.tool_services.MongoService import mgService


if __name__ == '__main__':
    data = mgService.query({'name':'刘先生', 'source_method':'upload', 'age':22},table='kb_talent_bank', db='kb_demo')[0]
    print(data['workExperience'])
