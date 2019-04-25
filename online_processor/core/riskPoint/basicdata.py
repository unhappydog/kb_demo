from datetime import datetime
from data_access.controller.KBAcademyController4Mongo import KBAcademyController4Mongo
from data_access.controller. CVController4Mongo import  CVController4Mongo

class basicdata(object):
    def __init__(self):
        self.cvinfo = CVController4Mongo()
        self.academy=KBAcademyController4Mongo()

    def clopsetime(self, signaldata):
        print(signaldata['name'])
        workStrattime = []
        workEndtime = []
        eduStarttime = []
        eduEndtime = []

        for si in signaldata['workExperience']:
                workStrattime.append(si['workStartTime'])
                if isinstance(si['workEndTime'],datetime):
                    workEndtime.append(si['workEndTime'])
                else:
                    workEndtime.append(signaldata['updateTime'])
        for ed in signaldata['educationExperience']:
                eduStarttime.append(ed['educationStartTime'])
                if ed['educationEndTime'] != '':
                    eduEndtime.append(ed['educationEndTime'])
                else:
                    eduEndtime.append(signaldata['updateTime'])
        return workStrattime,workEndtime,eduStarttime,eduEndtime

    def educationdata(self,singaldata):
        educationDegree = []
        eduname = []
        edumajor=[]
        for si in singaldata['educationExperience']:
              educationDegree.append(si['educationDegree'].strip(' '))
              eduname.append(si['educationSchool'])
              edumajor.append(si['educationMajor'])
        return educationDegree,eduname,edumajor

    def academydata(self):
        academyname=[]
        data=self.academy.get_datas()
        for ac in data:
            if len(ac['schoolName'].split(' '))>1:
                academyname.append(ac['schoolName'].split(' ')[1].strip(' '))
            else:
                academyname.append(ac['schoolName'].strip(' '))
        return academyname


    def worktimedata(self,singaldata):
        worktimedata=[]
        for wo in singaldata['workExperience']:
            if wo['workTimePeriod']:
                 worktimedata.append(wo['workTimePeriod'])
        return worktimedata

    def salarydata(self,singaldata):
        exceptsalar=singaldata['expectedSalary']
        worksalar=[]
        for sa in singaldata['workExperience']:
            try:
                worksalar.append(sa['workSalary'].strip(' '))
            except:
                worksalar.append(' ')
        return exceptsalar,worksalar

    def get_cvdata(self):
        data = self.cvinfo.get_datas()
        return data

if __name__=='__main__':
    data=basicdata().get_cvdata()
    print(len(data))
    # basicdata().salarydata(data[0])