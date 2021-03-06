from utils.Logger import logging
import resources
from data_access.controller.KBAcademyController4Mongo import KBAcademyController4Mongo
from data_access.controller.KBCompanyController4Mongo import KBCompanyController4Mongo
from core.linker.CompanyNameMapper import CompanyNameMapper

import re


class Linker:
    def __init__(self):
        self.academy_controller = KBAcademyController4Mongo()
        self.company_controller = KBCompanyController4Mongo()

    def link_academy(self, cv):
        """
        linking school names in cv to data in databases
        :param cv:
        :return:
        """
        academy = cv.highestEducationAcademy
        education_experiences = cv.educationExperience
        schools = []
        schools.append(academy)
        for educationExperience in education_experiences:
            school = educationExperience.educationSchool
            schools.append(school)
        result = {}
        print(schools)
        for school in schools:
            original_school = school
            school = re.sub("大学.*$", '大学', school) if '大学' in school else re.sub("学院.*$", "学院",
                                                                                 school) if '学院' in school else school
            if not school:
                continue
            data = self.academy_controller.get_data_by_name(school)
            if data:
                result[original_school] = data[0].__dict__
            else:
                # Logger.waring("{0} is not in database.".format(school))
                logging.warning("{0} is not in database".format(school))
        return result

    def link_company(self, cv):
        """
        linking companys in cv to data in databases
        :param cv:
        :return:
        """
        companys = []
        for workExperience in cv.workExperience:
            companys.append(workExperience.workCompany)
        result = {}
        for company in companys:
            data = self.company_controller.get_data_by_name(CompanyNameMapper.get_full_name(company))
            if ("大学" in company or "学院" in company) and not data:
                data = self.academy_controller.get_data_by_name(company)
            # if company.
            if not data:
                data = self.process_add_hoc(company)
            if data:
                result[company] = data[0].__dict__
            else:
                # Logger.waring("{0} is not in database.".format(company))
                # logging.warning("{0} is not in database".format(company))
                with open('company.txt','a+', encoding='utf8') as f:
                    f.write("{0}\n".format(company))
        return result

    def get_company_info(self, company):
        result = {}
        data = self.company_controller.get_data_by_name(company)
        if data:
            result[company] = data[0].__dict__
        else:
            # Logger.waring("{0} is not in database.".format(company))
            logging.warning("{0} is not in database".format(company))
        return result

    def process_add_hoc(self, company):
        add_hoc_words = ['阿里巴巴','阿里', '百度', '京东', '新浪', '搜狐', '腾讯', '华为', '小米','三星']
        for word in add_hoc_words:
            if word in company:
                data = self.company_controller.get_data_by_sub_name(word)
                return data
        return None

