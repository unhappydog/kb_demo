from data_access.controller.CVController4Mongo import CVController4Mongo
from services.LinkerService import linkerService
from services.DataService import dataService
from services.TalentBankService import tbService
from services.tool_services.MongoService import mgService

# from core.parser.CVParser import CVParser


if __name__ == '__main__':
    cv_controller = CVController4Mongo()
    # datas = cv_controller.get_datas()
    # datas = mgService.query({}, 'kb_demo', 'kb_CV_origin')
    # for data in datas:
    #     cv = linkerService.parse(data)
    #     # print(cv.__dict__)
    #     # dataService.save(cv)
    #     tbService.save(cv)
    print(tbService.search_by_name("机器学习", 2, 10))
