import json
from data_access.models.CV import CV
from data_access.models.properties.WorkExperience import WorkExperience
from data_access.models.properties.EducationExperience import EducationExperience
from data_access.models.properties.ProjectExperience import ProjectExperience
from data_access.models.properties.TrainingExperience import TrainingExperience
from data_access.models.properties.Skill import Skill
from data_access.models.properties.AssociationExperience import AssociationExperience
from data_access.models.properties.Language import Language
from data_access.models.properties.Certificate import Certificate
from data_access.models.properties.Book import Book
from data_access.models.properties.Award import Award
from data_access.models.properties.Patent import Patent
from data_access.models.properties.Paper import Paper
from utils.Utils import convert_str_2_date
from utils.Logger import logging
import datetime
import re

class_dict = {
    'educationExperience': EducationExperience,
    'workExperience': WorkExperience,
    'projectExperience': ProjectExperience,
    'trainingExperience': TrainingExperience,
    'associationExperience': AssociationExperience,
    'skill': Skill,
    'certificate': Certificate,
    'language': Language,
    'publishBook':Book,
    'award':Award,
    'publishPatent':Patent,
    'publishPaper': Paper
}


class CVParser:
    @staticmethod
    def parse(json_str):
        if type(json_str) == str:
            data = json.loads(json_str)
        elif type(json_str) == dict:
            data = json_str
        else:
            logging.error("json str format cant recongnized {0}".format(json_str))

        if "id" in data.keys() and "_id" in data.keys() and (data["_id"] == "" or data["_id"] is None):
            data["_id"] = data["id"]
            del data["id"]
        elif "id" in data.keys() and "_id" not in data.keys():
            data["_id"] = data["id"]
            del data["id"]
        elif "id" in data.keys():
            del data["id"]

        cv = CV(**data)
        age = cv.age
        if type(age) == int:
            age = cv.age
            birthday = cv.birthday
        elif re.match('[0-9]{2} 岁（[0-9]{4}年[0-9]{1,2}月）', age):
            year = age.split('（')[1].split('年')[0]
            month = age.split('（')[1].split('年')[1].split('月')[0]
            birthday = datetime.datetime(year=int(year), month=int(month), day=1)
            age = int(age[:2])
        elif re.match('[0-9]{1,3}', age):
            age = int(age)
            birthday = cv.birthday
        else:
            age = 0
            birthday = cv.birthday
            logging.error("unrecongized age format {0}".format(age))
        cv.age = age
        cv.birthday = birthday

        for key, value in class_dict.items():
            experience_list = cv.__dict__[key]
            cv.__dict__[key] = []
            if experience_list and experience_list != "" and type(experience_list) == list:
                for experience in experience_list:
                    cv.__dict__[key].append(value(**experience))

        for educationExperience in cv.educationExperience:
            educationExperience.educationEndTime = CVParser.parse_time(educationExperience.educationEndTime)
            educationExperience.educationStartTime =CVParser.parse_time(educationExperience.educationStartTime)
        for workExperience in cv.workExperience:
            workExperience.workStartTime = CVParser.parse_time(workExperience.workStartTime)
            workExperience.workEndTime = CVParser.parse_time(workExperience.workEndTime)
        for projectExperience in cv.projectExperience:
            projectExperience.projectStartTime = CVParser.parse_time(projectExperience.projectStartTime)
            projectExperience.projectEndTime = CVParser.parse_time(projectExperience.projectEndTime)

        cv.updateTime = CVParser.parse_time(cv.updateTime)
        return cv

    @staticmethod
    def parse_zhilian(json_str):
        if type(json_str) == str:
            data = json.loads(json_str)

        print(data)
        # data = json_str
        age = data.get("age", "")
        if re.match('[0-9]{2} 岁（[0-9]{4}年[0-9]{1,2}月）', age):
            age = int(age[:2])
            year = age.split('(')[1].split('年')[0]
            month = age.split('(')[1].split('年')[1].split('月')[0]
            birthday = datetime.datetime(year=int(year), month=int(month))
        else:
            age = 0
            birthday = None
            logging.error("unrecongized age format {0}".format(age))

        cv = CV(name=data.get('userName', None),
                gender=data.get('gender', None),
                jobTitle=data.get('jobTitle', None),
                highestEducationBackground=data.get('eduLevel', None),
                # age=data.get('age', None),
                age=age,
                birthday=birthday,
                currentAddress=data.get('city', None),
                expectedSalary=data.get('desiredSalary', None),
                updateTime=data.get('modifyDate', None),
                workYear=data.get('workYears', None),
                highestEducationAcademy=data.get('school', None),
                expectedWorkNature=data.get('employment', None),
                highestEducationMajor=data.get('major', None),
                expectedStatus=data.get('careerStatus', None),
                expectedOccupation=data.get('jobType', None),
                expectedWorkplace=data.get('desireCity', None),
                _id=data["id"],
                zhilianLabels=data.get('label', None))
        educationExperiences = []
        for experience in data["educationExperience"]:
            school_name = experience.get('SchoolName', "")
            school_name = re.sub('\(.+\)$|（.+）$', '', school_name)
            educationExperience = EducationExperience(educationStartTime=CVParser.parse_time(experience.get('DateStart', None)),
                                                      educationEndTime=CVParser.parse_time(experience.get('DateEnd', None)),
                                                      educationDegree=experience.get('EducationLevel', None),
                                                      educationSchool=school_name,
                                                      educationMajor=experience.get('MajorName', None),
                                                      majorBigType=experience.get('MajorBigType', None),
                                                      majorSmallType=experience.get('MajorSmallType', None))
            educationExperiences.append(educationExperience)
        workExperiences = []
        for experience in data["workExperience"]:
            company_name = experience.get('CompanyName', "")
            # company_name = re.sub('\(.+\)$|（.+）$', '', company_name)
            workExperience = WorkExperience(workStartTime=CVParser.parse_time(experience.get('DateStart', None)),
                                            workEndTime=CVParser.parse_time(experience.get('DateEnd', None)),
                                            workCompany=company_name,
                                            workPosition=experience.get('JobTitle', None),
                                            workDepartment=experience.get('ResideDepartment', None),
                                            workSalary=experience.get('Salary', None),
                                            workDescription=experience.get('WorkDescription', None))
            workExperiences.append(workExperience)

        cv.workExperience = workExperiences
        cv.educationExperience = educationExperiences
        _skills = []
        if type(data["skill"] == str):
            cv.skill = data["skill"]
        else:
            for skill in data["skill"]:
                _skill = Skill(name=skill.get('name'),
                               skillMastery=skill.get('skillMastery'),
                               skillUseTime=skill.get('skillUseTime'))
                _skills.append(_skill)
            cv.skill = _skills
        return cv

    @staticmethod
    def parse_time(date):
        if date == '至今':
            return None
        if date:
            return convert_str_2_date(date)
        else:
            return None
