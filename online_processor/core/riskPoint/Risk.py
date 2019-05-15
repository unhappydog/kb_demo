from core.riskPoint.basicdata import basicdata
import numpy as np
from core.riskPoint.util import util
import re
from utils import Utils
"""
异常类型设计：
     工作时间异常；教育时间异常；毕业高校异常；工作跳槽频繁；薪资异常
"""

class riskPoint(object):
    def __init__(self):
        self.cv_data = ''
        self.workStrattime, self.workEndtime, self.eduStarttime, self.eduEndtime = [], [], [], []
        self.acadmyschool = basicdata().academydata()
        self.updatetime = ''



    # 时间异常情况

    def identification(self,cvdata):
                 self.cv_data=cvdata
                 print(self.cv_data['name'])
                 self.updatetime =self.cv_data['updateTime']
                 try:
                         self.workStrattime, self.workEndtime, self.eduStarttime, self.eduEndtime = basicdata().clopsetime(
                             self.cv_data)
                         totaldict = []
                         timclash = self.timeclash()
                         edutime = self.edutimeerror(self.cv_data)
                         worktimeError = self.worktimeError(self.cv_data)
                         edutimegap = self.edutimegap(self.cv_data)
                         worktimegap = self.worktimegap(self.cv_data)
                         salaryerror = self.salaryerror(self.cv_data)
                         if not isinstance(timclash, bool):
                             totaldict.extend(timclash)
                         if not isinstance(worktimeError, bool):
                             totaldict.extend(worktimeError)
                         if not isinstance(edutime, bool):
                             totaldict.extend(edutime)
                         if not isinstance(salaryerror, bool):
                             totaldict.append(salaryerror)
                         if not isinstance(edutimegap, bool):
                             totaldict.append(edutimegap)
                         if not isinstance(worktimegap, bool):
                             totaldict.extend(worktimegap)
                         genera_use = self.genera_use(self.cv_data)
                         if not isinstance(genera_use, bool):
                             totaldict.append(genera_use)

                 except:
                         totaldict = []
                         edutime = self.edutimeerror(self.cv_data)
                         if not isinstance(edutime, bool):
                             totaldict.extend(edutime)
                         edutimegap = self.edutimegap(self.cv_data)
                         if not isinstance(edutimegap, bool):
                             totaldict.append(edutimegap)
                         genera_use = self.genera_use(self.cv_data)
                         if not isinstance(genera_use, bool):
                             totaldict.append(genera_use)
                 print(totaldict)
                 return totaldict
    #时间异常情况
    def timeclash(self):
        timeclash = []
        worksmalltime = min(self.workStrattime)
        edumaxtime = max(self.eduEndtime)
        if not isinstance(util().time_difference(edumaxtime,worksmalltime),bool):
            year, month = util().time_difference(edumaxtime,worksmalltime)
            if year > 0 and year<10:
                temp={}
                temp["label"] = "工作时间异常"
                if month == 0:
                    temp['error'] = '候选人第一段工作经历晚于毕业时间' + str(year) + '年'
                else:
                    temp['error'] = '候选人第一段工作经历晚于毕业时间' + str(year) + '年' + str(month) + '月'
                timeclash.append(temp)
            elif month > 6:
                temp={}
                temp['error'] = '候选人第一段工作经历晚于毕业时间' + str(month) + '月'
                timeclash.append(temp)
        count=0
        for ws, we in zip(self.workStrattime, self.workEndtime):
            for es, ew in zip(self.eduStarttime, self.eduEndtime):
                if util().overlapping(ws, we, es, ew):
                    count+=1
        if count>0:
                    timeerror = {}
                    timeerror['label'] = '时间逻辑异常'
                    timeerror['error'] = '候选人工作经历与教育经历的时间冲突'
                    timeclash.append(timeerror)
        if len(timeclash) > 0:
            return timeclash
        else:
            return False

    #教育异常情况
    def edutimeerror(self,singaldata):
        educationDegree,eduname,edumajor=basicdata().educationdata(singaldata)
        school=basicdata().academydata()
        eduerror=[]
        count=0
        for es,ew,ed,en,em in  zip(self.eduStarttime,self.eduEndtime,educationDegree,eduname,edumajor):
            count+=1
            year,month=util().time_difference(es,ew)
            if ed=='本科':
                temp={}
                if  year<=3 and month<11:
                    temp['label']='本科异常'
                    temp['error'] = '候选人本科不足4年'
                    eduerror.append(temp)
            if ed=='硕士':
                    temp={}
                    if "香港" in en or bool(re.search('[a-z]', en)):
                        if year<1:
                          temp['label']='硕士异常'
                          temp['error']='候选人硕士读了不到'+str(month)+'个月'
                          eduerror.append(temp)
                    else:
                        if (year<=1 and month<6) :
                            temp['label']='硕士异常'
                            temp['error']='候选人硕士读了不到2年'
                            eduerror.append(temp)
                        elif year>3:
                            temp['label']='硕士异常'
                            temp['error']='候选人读了'+str(year)+'硕士'
                            eduerror.append(temp)
            if ed=='其他':
                temp={}
                temp['label']='学历异常'
                temp['error']='候选人学历不明'
                eduerror.append(temp)
            if em == '其他':
                temp = {}
                temp['label'] = '专业不明'
                temp['error'] = '候选人第' +str(count) + '段教育经历的专业不明'
                eduerror.append(temp)
            if '（' in en :
                en="".join(re.findall('(.*)（',en))
                print(en)
            else:
                en=en
            if en.strip(' ') not in [i for i in school]:
                    if '香港' in en or '莫斯科'in en:
                        continue
                    temp = {}
                    temp['label'] = '高校异常'
                    temp['error'] = '候选人在第' +str(count) + '段教育经历所就读的高校可能填写有误'
                    eduerror.append(temp)

        if '大专' in educationDegree and len(educationDegree)>1:
            temp={}
            temp['label']='专升本'
            temp['error']='候选人本科之前读了专科'
            eduerror.append(temp)
        if len(eduerror) > 0:
            return eduerror
        else:
            return False

    #薪资情况
    def salaryerror(self,singaldata):
        exsalary,worksalary=basicdata().salarydata(singaldata)
        mid=[]
        if exsalary!='':
            for ws in worksalary:
                if len(ws.split('-'))>1:
                    start=int(ws.split('-')[0])
                    end=int(ws.split('-')[1].strip('元/月'))
                    mid.append(start+(end-start)//2)
                else:
                    continue
            if len(exsalary.split('-'))>1:
                exstart=int(exsalary.split('-')[0])
                exsal=exstart+(int(exsalary.split('-')[1].strip('元/月'))-exstart)//2
                if exsal<np.mean(mid):
                    temp = {}
                    temp['label']='薪资异常'
                    temp['error']='候选人期望薪资低于工作经历的平均薪资'
                    return temp
                else:
                    return False
            else:
                return False
        else:
            return  False

    #跳槽频繁情况
    def worktimeError(self,singaldata):
        worktime=basicdata().worktimedata(singaldata)
        status=singaldata['expectedStatus']
        count=0
        hopping=[]
        if len(worktime)>0:
            for si,wt in zip(singaldata['workExperience'],worktime):

                if '年' in wt:
                    continue
                else:
                    mon="".join(re.compile('\d+').findall(wt))
                    if '在校生' in status or '应届生' in status:
                        continue
                    elif int(mon)<6:
                        count += 1
            if count>0:
                temp = {}
                temp['label'] = '跳槽频繁'
                temp['error'] = '候选人的工作经历不足半年'
                hopping.append(temp)
            if len(hopping)>0:
                return hopping
            else:
                return False
        else:
            return False



    #时间间隔（教育时间间隔，工作时间间隔）
    def edutimegap(self,singaldata):
        edugapdata=singaldata['educationExperience']
        eduyeargap,edumongap=util().gap(edugapdata,self.updatetime,0)
        if len(eduyeargap) > 0:
            temp = {}
            maxgap = max(eduyeargap)
            if maxgap > 0:
                temp['label'] = '教育间隔'
                temp['error'] = '候选人的教育经历时间有' + Utils.int_to_hanzi(maxgap) + '年的间隔'
                return temp
            else:
                return False
        else:
            return False

    def worktimegap(self, singaldata):
        workdata = singaldata['workExperience']
        try:
            workyear=singaldata['workYear']
            if workyear:
                workyeargap, workmongap = util().gap(workdata, self.updatetime, 1)
                jobhopping = []
                if workyear != 0:
                    year, month = util().time_difference(min(self.workStrattime), max(self.workEndtime))
                    if month > 6:
                        year = year + 1
                    if workyear>2:
                        if self.eduEndtime[0]>singaldata['updateTime']:
                            temp={}
                            temp['label']='工作经验异常'
                            temp['error']='候选人尚未毕业但已有'+str(workyear)+'年工作经验'
                            jobhopping.append(temp)
                count = len(workdata) + 1
                if len(workdata) > 1:
                    for wy, wk in zip(workyeargap, workmongap):
                        count -= 1
                        strsum = count - 1
                        if wy != 0:
                            temp = {}
                            temp['label'] = '工作间隔'
                            temp['error'] = '候选人在第' + Utils.int_to_hanzi(strsum) + '段工作经历与第' + Utils.int_to_hanzi(count) + '段工作经历之间的空档期为' + str(
                                wy) + '年'
                            jobhopping.append(temp)
                        elif wy == 0 and wk > 6:
                            temp = {}
                            temp['label'] = '工作间隔'
                            temp['error'] = '候选人在第' +Utils.int_to_hanzi(strsum)+ '段工作经历与第' + Utils.int_to_hanzi(count) + '段工作经历之间的空档期超过半年'
                            jobhopping.append(temp)
                    if util().iszero(workyeargap) and util().iszero(workmongap):
                        temp = {}
                        temp['label'] = '工作间隔'
                        temp['error'] = '候选人在工作经历中没有任何空档期'
                        jobhopping.append(temp)
                if len(jobhopping) > 0:
                    return jobhopping
                else:
                    return False
        except:
            return False
    #滥用精通
    def genera_use(self,sigaldata):
        try:
            skill = sigaldata['skill']

            if isinstance(skill, list):
                if len(skill)>1:
                    for sk in skill:
                        skill += sk[1]
                else:
                    skill="".join(skill)
            else:
                skill = skill
        except:
            skill = ''
        try:
            selfeval = sigaldata['selfEvaluation']
        except:
            selfeval = ''
        text = skill + selfeval
        if text != '':
            wordcount = len(re.compile('精通').findall(text))
            if wordcount >= 3:
                temp = {}
                temp['label'] = '滥用精通'
                temp['error'] = '候选人在技能能力中出现了' + str(wordcount) + '个精通'
                return temp
            else:
                return False
        else:
            return False

if __name__=='__main__':
    cvdata=basicdata().get_cvdata()[0]
    riskPoint().identification(cvdata)
