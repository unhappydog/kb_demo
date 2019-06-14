import sys
sys.path.append(".")
from data_access.controller.CVController4Mongo import CVController4Mongo
from services.LinkerService import linkerService
from services.DataService import dataService
from services.TalentBankService import tbService
from services.tool_services.MongoService import mgService
from services.PersonJobFitService import PersonJobFitService
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo
from tqdm import tqdm

personJobFitService = PersonJobFitService.instance()

# from core.parser.CVParser import CVParser


if __name__ == '__main__':
    keyword_dict = KBPostController4Mongo().get_prefix_dict()
    keyword_dict['自然语言处理工程师'].remove('知识图谱')
    word_to_title = {}
    for job_title, keywords in keyword_dict.items():
        for keyword in keywords:
            if keyword in word_to_title.keys():
                word_to_title[keyword].append(job_title)
            else:
                word_to_title[keyword] = [job_title]
    word_to_title['知识图谱'] = ['知识图谱工程师']


    cv_controller = CVController4Mongo()
    datas = cv_controller.get_datas()
    datas = mgService.query({}, 'kb_demo', 'kb_CV_2019')
    for data in tqdm(datas):
        cv = linkerService.parse(data)
        word_experiences = cv.workExperience
        if len(word_experiences) <= 0:
            continue
        word_experiences = sorted(word_experiences, key=lambda x: x.workStartTime, reverse=True)
        cv.recentPosition = word_experiences[0]['workPosition']
        cv.source = "zhilian"
        cv.source_method='zhilian'
        cv.skill_tag = linkerService.gen_skill_tag(cv)

        job_title = word_to_title.get(cv.keyword)
        if not job_title:
            continue
        job_title = job_title[0]
        position = dataService.get_position_by(job_title)
        if not position:
            continue
        position = position[0]
        score = personJobFitService.score(cv, position)
        cv['score'] = score
        cv['jobTitle'] = job_title
        tbService.save(cv,'1')

    datas = mgService.query({}, 'kb_demo','kb_CV')
    for data in tqdm(datas):
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
        cv.skill_tag = linkerService.gen_skill_tag(cv)
        job_title = word_to_title.get(cv.keyword)
        if not job_title:
            continue
        job_title = job_title[0]
        position = dataService.get_position_by(job_title)
        if not position:
            continue
        position = position[0]
        score = personJobFitService.score(cv, position)
        cv['score'] = score
        tbService.save(cv,'1')
    # print(tbService.search_by_name("机器学习算法工程师", 2, 10))
