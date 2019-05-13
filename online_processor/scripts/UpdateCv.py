from data_access.controller.CVController4Mongo import CVController4Mongo
from services.LinkerService import linkerService
from services.DataService import dataService
from services.TalentBankService import tbService
from services.tool_services.MongoService import mgService

# from core.parser.CVParser import CVParser


if __name__ == '__main__':
    cv_controller = CVController4Mongo()
    datas = cv_controller.get_datas()
    datas = mgService.query({}, 'kb_demo', 'kb_CV_origin')
    for data in datas:
        cv = linkerService.parse(data)
        word_experiences = cv.workExperience
        if len(word_experiences) <= 0:
            continue
        word_experiences = sorted(word_experiences, key=lambda x: x.workStartTime, reverse=True)
        cv.recentPosition = word_experiences[0]['workPosition']
        # print(cv.__dict__)
        # dataService.save(cv)
        cv.source = "zhilian"
        cv.source_method='zhilian'
        tbService.save(cv)

    datas = mgService.query({}, 'kb_demo','kb_CV')
    for data in datas:
        print(data)
        cv = linkerService.parse(data)
        cv.highestEducationDegree = cv.highestEducationBackground
        word_experiences = cv.workExperience
        if len(word_experiences) <=0:
            continue
        word_experiences = sorted(word_experiences, key=lambda x: x.workStartTime, reverse=True)
        cv.recentPosition = word_experiences[0]['workPosition']
        cv.source = 'zhilian'
        cv.source_method = 'upload'
        tbService.save(cv)
    # print(tbService.search_by_name("机器学习算法工程师", 2, 10))
