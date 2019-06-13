from data_access.controller.TalentController4Mongo import TalentController4Mongo
from services.tool_services.MongoService import mgService
from data_access.controller.KBCompanyController4Mongo import KBCompanyController4Mongo
import re


def create():
    talent_controller = TalentController4Mongo()
    company_controller = KBCompanyController4Mongo()
    datas = talent_controller.get_datas_as_gen()
    for data in datas:
        company_name = data['Company']
        job_title = re.sub('\(.+\)|-.*$|（.+）', '', data['Name'])
        company_info = company_controller.get_data_by_name(company_name)
        if company_info:
            company_info = company_info[0]
            temp_dict = {}
            temp_dict['company'] = company_name
            temp_dict['startDate'] = data['Startdate']
            temp_dict['endDate'] = data['Enddate']
            temp_dict['number'] = data['Number']
            temp_dict['address'] = company_info.get('contactAddress')
            temp_dict['esdate'] = company_info.get('establishedDate')
            temp_dict['scope'] = company_info['companyScopeTags']
            temp_dict['scale'] = company_info['companyScale']
            temp_dict['frName'] = company_info.get('frName')
            temp_dict['regCapital'] = company_info['regCapital']
            temp_dict['des'] = company_info['brief']
            temp_dict['jobTitle'] = job_title
            # print(temp_dict)
            already_exist_data = mgService.query({"company": company_name, "jobTitle": job_title}, 'kb_demo',
                                                 'jd_company')
            if already_exist_data:
                # _id = already_exist_data['_id']
                print("duplicate")
            else:
                mgService.insert(temp_dict, 'kb_demo', 'jd_company')


if __name__ == '__main__':
    create()
