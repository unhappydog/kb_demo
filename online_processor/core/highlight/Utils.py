from data_access.controller.CVController4Mongo import CVController4Mongo
from data_access.controller.KBAcademyController4Mongo import KBAcademyController4Mongo
from data_access.controller.JDCompanyController4Mongo import JDCompanyController4Mongo
from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo
class basicinfo(object):
    def __init__(self):
        self.cvinfo = CVController4Mongo()
        self.academy = KBAcademyController4Mongo()
        self.jdcompany=JDCompanyController4Mongo()
        self.terminology=KBTerminologyController4Mongo()
    def get_company(self):
        companydata=self.jdcompany.get_datas()
        return companydata
    def get_academy(self):
        academydata=self.academy.get_datas()
        return academydata
    def get_cvdata(self):
        # data=self.cvinfo.get_data_by_id( _id='felUB(QMusmOrYKUoDC(WA')
        data = self.cvinfo.get_datas()
        return data
    # def get_terminology(self):
    #     termindata=self.terminology.get_datas()
    #     frontend=[]#前端
    #     backend=[]#后端
    #     ai=[]#人工智能
    #     database=[]#数据库
    #     for ter in termindata:
    #         if ter['fieldId']is not None:
    #              name = []
    #              if ter['cnName'] is not None:
    #                  name.extend(ter['cnName'])
    #              elif ter['engName'] is not None:
    #                  name.extend(ter['engName'])
    #              if 'Web开发' in ter['fieldId']:
    #                  frontend.extend(name)
    #              if 'Server后端' in ter['fieldId'] or '编程语言' in ter['fieldId']:
    #                  backend.extend(name)
    #              if 'AI通用' in ter['fieldId'] or '深度学习' in ter['fieldId'] or '机器学习' in ter['fieldId']:
    #                  ai.extend(name)
    #              if '数据库' in ter['fieldId']:
    #                 database.extend(name)
    #
    #     return frontend,backend,ai,database

if __name__=='__main__':
    basicinfo().get_terminology()