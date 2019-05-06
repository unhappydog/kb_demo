import json
import os
from settings import  BASE_DIR
from data_access.models.CV import CV
from data_access.models.properties.EducationExperience import EducationExperience
from data_access.models.properties.WorkExperience import WorkExperience
from data_access.controller.CVController4Mongo import CVController4Mongo

career = os.path.join(BASE_DIR, "resources", "careers.json")
summary_path = os.path.join(BASE_DIR, "resources", "summary.json")
print(career)
fp = open(career,'r',encoding='utf8')
fp_summary = open(summary_path, 'r', encoding='utf8')
json_data = json.load(fp)
json_summary = json.load(fp_summary)
datas = json_data['data']['dataList']
summarys = json_summary['data']
data_summarys = zip(datas, summarys)
cv_controller = CVController4Mongo()
for data, summary in data_summarys:
   cv = CV(name=data['userName'],
      gender=data['gender'],
      jobTitle=data['jobTitle'],
      highestEducationBackground=data['eduLevel'],
      age=data['age'],
      currentAddress=data['city'],
      expectedSalary=data['desiredSalary'],
      updateTime=data['modifyDate'],
      workYear=data['workYears'],
      highestEducationAcademy=data['school'],
      expectedWorkNature=data['employment'],
      highestEducationMajor=data['major'],
      expectedStatus=data['careerStatus'],
      expectedOccupation=data['jobType'],
      expectedWorkplace=data['desireCity'],
      _id=data["id"],
      zhilianLabels=data['label'])
   educationExperiences = []
   for experience in summary["educationExperience"]:
        educationExperience = EducationExperience(educationStartTime=experience['DateStart'],
                                                  educationEndTime=experience['DateEnd'],
                                                  educationDegree=experience['EducationLevel'],
                                                  educationSchool=experience['SchoolName'],
                                                  educationMajor=experience['MajorName'],
                                                  majorBigType=experience['MajorBigType'],
                                                  majorSmallType=experience['MajorSmallType'])
        educationExperiences.append(educationExperience)
   workExperiences = []
   for experience in summary["workExperience"]:
       workExperience = WorkExperience(workStartTime=experience['DateStart'],
                                       workEndTime=experience['DateEnd'],
                                       workCompany=experience['CompanyName'],
                                       workPosition=experience['JobTitle'],
                                       workDepartment=experience['ResideDepartment'],
                                       workSalary=experience['Salary'],
                                       workDescription=experience['WorkDescription'])
       workExperiences.append(workExperience)

   cv.workExperience = workExperiences
   cv.educationExperience = educationExperiences
   cv_controller.insert_data(cv)


   print(cv.__dict__)
   # break

