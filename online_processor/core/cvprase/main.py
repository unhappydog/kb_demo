import os
from data_access.models.CV import CV
from core.cvprase.cvword.praseword import cvword
from core.cvprase.cvpdf.extract import cvprase
from core.cvprase.cvhtml.prasehtml import htmlparse
from core.cvprase.Util.util import util
class CV_main(object) :
    def __init__(self, root):
        self.cv = None
        self.root = root
        self.predicates = ['name', 'updateTime', 'id', 'gender', 'age', 'birthday', 'workYear', 'highestEducationBackground', 'currentAddress',
                       'domicilePlace', 'politicsStatus', 'marital', 'selfEvaluation',
                        'expectedWorkplace', 'expectedSalary', 'expectedStatus', 'expectedOccupation', 'expectedIndustry',
                        'workExperience','projectExperience', 'educationExperience', 'certificate', 'trainingExperience', 'award',
                        'associationExperience','skill', 'hobby']

    def main_prase(self):
            print(self.root)
            dict={}
            if self.root.endswith('html'):
                dict = htmlparse().parsemain(self.root)
            if self.root.endswith('docx'):
                dict = cvword().mainwordprase(self.root)
            if self.root.endswith('doc'):
                util().doc2docx(self.root)
                os.remove(self.root)
                dict = cvword().mainwordprase(self.root.replace('doc', 'docx'))
            if self.root.endswith('pdf'):
                dict = cvprase().prase(self.root)
            for pre in self.predicates:
                   try:
                      dict[pre]
                   except:
                        dict[pre]=''
            print(dict)
            self.cv = CV(name=dict['name'],
                         updateTime=dict['updateTime'],
                         _id=dict['id'],
                         gender=dict['gender'],
                         age=dict['age'],
                         birthday=dict['birthday'],
                         workYear=dict['workYear'],
                         highestEducationBackground=dict['highestEducationBackground'],
                         currentAddress=dict['currentAddress'],
                         domicilePlace=dict['domicilePlace'],
                         politicsStatus=dict['politicsStatus'],
                         marital=dict['marital'],
                         selfEvaluation=dict['selfEvaluation'],
                         expectedWorkplace=dict['expectedWorkplace'],
                         expectedSalary=dict['expectedSalary'],
                         expectedStatus=dict['expectedStatus'],
                         expectedOccupation=dict['expectedOccupation'],
                         expectedIndustry=dict['expectedIndustry'],
                         workExperience=dict['workExperience'],
                         projectExperience=dict['projectExperience'],
                         educationExperience=dict['educationExperience'],
                         certificate=dict['certificate'],
                         trainingExperience=dict['trainingExperience'],
                         award=dict['award'],
                         associationExperience=dict['associationExperience'],
                         skill=dict['skill'],
                         hobby=dict['hobby'])
            return self.cv


if __name__=='__main__':


        h=CV_main('/tmp/pycharm_141/core/cvprase/file/智联招聘_陈先生_中文_20190415_1555294308533.docx')
        data=h.main_prase()





