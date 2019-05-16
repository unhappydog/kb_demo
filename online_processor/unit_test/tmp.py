from services.tool_services.MongoService import mgService
from services.DataService import dataService
from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
from services.LinkerService import linkerService
from services.TalentBankService import tbService
if __name__ == '__main__':
    # data = mgService.query({'name':'刘先生', 'source_method':'upload', 'age':22},table='kb_talent_bank', db='kb_demo')[0]
    # print(data['workExperience'])
    controller = KBTalentBankController4Mongo()
    datas = controller.get_datas()
    count = 0
    error_count = 0
    for data in datas:
        try:
            cv = linkerService.parse(data)
            if len(cv.workExperience) < 1:
                print(cv._id)
                # tbService.delete_by_id(cv._id)

                count += 1
        except TypeError as error:
            print(data['_id'])
            # tbService.delete_by_id(data['_id'])
            error_count += 1
    print(count)
    print(error_count)
