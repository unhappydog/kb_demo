from data_access.controller.CVController4Mongo import CVController4Mongo
from services.LinkerService import linkerService
from services.DataService import dataService
# from core.parser.CVParser import CVParser


if __name__ == '__main__':
    cv_controller = CVController4Mongo()
    datas = cv_controller.get_datas()
    for data in datas:
        cv = linkerService.parse(data)
        # print(cv.__dict__)
        dataService.save(cv)
