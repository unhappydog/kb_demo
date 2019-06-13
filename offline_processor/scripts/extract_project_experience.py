from data_access.controller.KbTalentBankController4Mongo import KBTalentBankController4Mongo
from services.tool_services.MongoService import mgService
import datetime


def extract_expericen():
    controller = KBTalentBankController4Mongo()
    datas = controller.get_datas_as_gen()
    for data in datas:
        projectExperiences = data['projectExperience']
        keyword = data['keyword']
        workExperiences = data['workExperience']
        company_map = {}
        if workExperiences:
            for workExperience in workExperiences:
                company_map[workExperience['workCompany']] = {}
                if workExperience['workEndTime'] is None or workExperience['workEndTime'] == "":
                    end = datetime.datetime.now()
                else:
                    end = workExperience.get('workEndTime')
                start = workExperience.get('workStartTime')
                company_map[workExperience['workCompany']]['end'] = end
                company_map[workExperience['workCompany']]['start'] = start
        else:
            pass
        if projectExperiences:
            count = 0
            for projectExperience in projectExperiences:
                count +=1
                temp = {}
                temp['_id'] = data['_id'] + str(count)
                temp['projectStartTime'] = projectExperience['projectStartTime']
                temp['projectEndTime'] = projectExperience['projectEndTime']
                temp['projectName'] = projectExperience['projectName']
                temp['projectTimePeriod'] = projectExperience['projectTimePeriod']
                temp['projectDuty'] = projectExperience['projectDuty']
                temp['projectDescription'] = projectExperience['projectDescription']
                start = projectExperience['projectStartTime']
                temp['keyword'] = keyword
                if temp['projectEndTime'] is None or temp['projectEndTime'] == "":
                    end = datetime.datetime.now()
                else:
                    end = temp['projectEndTime']
                for company, v in company_map.items():
                    if v['start'] <= start and v['end']>=end:
                        temp['company'] = company
                save_experience(temp)


def save_experience(doc):
    try:
        mgService.insert(doc, 'kb_demo', 'kb_project_experience')
    except:
        mgService.update({'_id', doc['_id']},doc,'kb_demo','kb_project_experience')


if __name__ == '__main__':
    extract_expericen()
