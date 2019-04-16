import json
from data_access.models.CV import CV
from data_access.models.properties.WorkExperience import WorkExperience
from data_access.models.properties.EducationExperience import EducationExperience
from data_access.models.properties.ProjectExperience import ProjectExperience
from data_access.models.properties.TrainingExperience import TrainingExperience
from data_access.models.properties.AssociationExperience import AssociationExperience
import re

class_dict = {
    'educationExperience': EducationExperience,
    'workExperience': WorkExperience,
    'projectExperience': ProjectExperience,
    'trainingExperience': TrainingExperience,
    'associationExperience': AssociationExperience
}


class CVParser:
    @staticmethod
    def parse(json_str):
        data = json.loads(json_str)
        if "id" in data.keys():
            del data["id"]
        cv = CV(**data)
        for key, value in class_dict.items():
            experience_list = cv.__dict__[key]
            cv.__dict__[key] = []
            if experience_list:
                for experience in experience_list:
                    cv.__dict__[key].append(value(**experience))
        return cv

    @staticmethod
    def parse_zhilian(json_str):
        data = json.loads(json_str)
        # data = json_str
        cv = CV(name=data.get('userName', None),
                gender=data.get('gender', None),
                jobTitle=data.get('jobTitle', None),
                highestEducationBackground=data.get('eduLevel', None),
                age=data.get('age', None),
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
            educationExperience = EducationExperience(educationStartTime=experience.get('DateStart', None),
                                                      educationEndTime=experience.get('DateEnd', None),
                                                      educationDegree=experience.get('EducationLevel', None),
                                                      educationSchool=experience.get('SchoolName', None),
                                                      educationMajor=experience.get('MajorName', None),
                                                      majorBigType=experience.get('MajorBigType', None),
                                                      majorSmallType=experience.get('MajorSmallType', None))
            educationExperiences.append(educationExperience)
        workExperiences = []
        for experience in data["workExperience"]:
            company_name = experience.get('CompanyName', "")
            company_name = re.sub('\(.+\)$|（.+）$', '', company_name)
            workExperience = WorkExperience(workStartTime=experience.get('DateStart', None),
                                            workEndTime=experience.get('DateEnd', None),
                                            workCompany=company_name,
                                            workPosition=experience.get('JobTitle', None),
                                            workDepartment=experience.get('ResideDepartment', None),
                                            workSalary=experience.get('Salary', None),
                                            workDescription=experience.get('WorkDescription', None))
            workExperiences.append(workExperience)

        cv.workExperience = workExperiences
        cv.educationExperience = educationExperiences
        return cv
