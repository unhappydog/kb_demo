from core.riskPoint.basicdata import basicdata
import numpy as np
from core.riskPoint.util import util
import re

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

    def identification(self, cvdata):
        self.cv_data = cvdata
        self.updatetime = self.cv_data['updateTime']
        self.workStrattime, self.workEndtime, self.eduStarttime, self.eduEndtime = basicdata().clopsetime(self.cv_data)
        totaldict = []
        timclash = self.timeclash()
        edutime = self.edutimeerror(self.cv_data)
        salaryerror = self.salaryerror(self.cv_data)
        worktimeError = self.worktimeError(self.cv_data)
        edutimegap = self.edutimegap(self.cv_data)
        worktimegap = self.worktimegap(self.cv_data)
        # genera_use = self.genera_use(self.cv_data)
        if not isinstance(timclash, bool):
            totaldict.append(timclash)
        if not isinstance(edutime, bool):
            totaldict.extend(edutime)
        if not isinstance(salaryerror, bool):
            totaldict.append(salaryerror)
        if not isinstance(worktimeError, bool):
            totaldict.extend(worktimeError)
        if not isinstance(edutimegap, bool):
            totaldict.append(edutimegap)
        if not isinstance(worktimegap, bool):
            totaldict.extend(worktimegap)
        # if not isinstance(genera_use, bool):
        #     totaldict.append(genera_use)
        return totaldict

    # 时间异常情况

    def timeclash(self):
        temp = {}
        worksmalltime = min(self.workStrattime)
        edumaxtime = max(self.eduEndtime)
        year, month = util().time_difference(worksmalltime, edumaxtime)
        if year > 0:
            temp["label"] = "工作时间异常"
            if month == 0:
                temp['error'] = '候选人第一段工作经历晚于毕业时间' + str(year) + '年'
            else:
                temp['error'] = '候选人第一段工作经历晚于毕业时间' + str(year) + '年' + str(month) + '月'
        elif month > 6:
            temp['error'] = '候选人第一段工作经历晚于毕业时间' + str(month) + '月'
        count = 0
        for ws, we in zip(self.workStrattime, self.workEndtime):
            count += 1
            ecount = 0
            for es, ew in zip(self.eduStarttime, self.eduEndtime):
                ecount += 1
                if util().overlapping(ws, we, es, ew):
                    temp = {}
                    temp['label'] = '时间逻辑异常'
                    temp['error'] = '候选人第' + str(count) + '段工作经历与第' + str(ecount) + '段教育经历的时间冲突'
        if len(temp) > 0:
            return temp
        else:
            return False

    # 教育异常情况
    def edutimeerror(self, singaldata):
        educationDegree, eduname, edumajor = basicdata().educationdata(singaldata)
        school = basicdata().academydata()
        eduerror = []
        count = 0
        for es, ew, ed, en, em in zip(self.eduStarttime, self.eduEndtime, educationDegree, eduname, edumajor):
            count += 1
            year, month = util().time_difference(es, ew)
            if ed == '本科':
                temp = {}
                if year <= 3 and month < 11:
                    temp['label'] = '本科异常'
                    temp['error'] = '候选人本科读了' + str(year + 1) + '年'
                    eduerror.append(temp)
            if ed == '硕士':
                temp = {}
                if "香港" in en or bool(re.search('[a-z]', en)):
                    if year < 1:
                        temp['label'] = '硕士异常'
                        temp['error'] = '候选人硕士读了不到' + str(month) + '个月'
                        eduerror.append(temp)
                else:
                    if (year <= 1 and month < 11):
                        temp['label'] = '硕士异常'
                        temp['error'] = '候选人硕士读了不到2年'
                        eduerror.append(temp)
            if ed == '其他':
                temp = {}
                temp['label'] = '学历异常'
                temp['error'] = '候选人学历不明'
                eduerror.append(temp)
            if em == '其他':
                temp = {}
                temp['label'] = '专业不明'
                temp['error'] = '候选人第' + str(count) + '段教育经历的专业不明'
                eduerror.append(temp)
            if en not in [i for i in school]:
                if '香港' in en:
                    continue
                temp = {}
                temp['label'] = '高校异常'
                temp['error'] = '候选人在第' + str(count) + '段教育经历所就读的高校可能不存在'
                eduerror.append(temp)
        if '本科' in educationDegree:
            temp = {}
            temp['label'] = '专升本'
            temp['error'] = '候选人本科之前读了专科'
            eduerror.append(temp)
        if len(eduerror) > 0:
            return eduerror
        else:
            return False

    # 薪资情况
    def salaryerror(self, singaldata):
        exsalary, worksalary = basicdata().salarydata(singaldata)
        mid = []
        for ws in worksalary:
            if len(ws.split('-')) > 1:
                start = int(ws.split('-')[0])
                end = int(ws.split('-')[1].strip('元/月'))
                mid.append(start + (end - start) // 2)
            else:
                continue
        if len(exsalary.split('-')) > 1:
            exstart = int(exsalary.split('-')[0])
            exsal = exstart + (int(exsalary.split('-')[1].strip('元/月')) - exstart) // 2
            if exsal < np.mean(mid):
                temp = {}
                temp['label'] = '薪资异常'
                temp['error'] = '候选人期望薪资低于工作经历的平均薪资'
                return temp
            else:
                return False
        else:
            return False


    #跳槽频繁情况
    def worktimeError(self,singaldata):
        worktime=basicdata().worktimedata(singaldata)
        status=singaldata['expectedStatus']
        count=0
        hopping=[]
        if len(worktime)>0:
            for si,wt in zip(singaldata['workExperience'],worktime):
                count+=1
                if '年' in wt:
                    continue
                else:
                    mon="".join(re.compile('\d+').findall(wt))
                    if '在校生' in status or '应届生' in status:
                        continue
                    elif int(mon)<6:
                        temp={}
                        temp['label']='跳槽频繁'
                        temp['error']='候选人的第'+str(count)+'段工作经历不足半年'
                        hopping.append(temp)
            if len(hopping)>0:
                return hopping
            else:
                return False
        else:
            return False

    # 时间间隔（教育时间间隔，工作时间间隔）
    def edutimegap(self, singaldata):
        edugapdata = singaldata['educationExperience']
        eduyeargap, edumongap = util().gap(edugapdata, self.updatetime, 0)
        if len(eduyeargap) > 0:
            temp = {}
            maxgap = max(eduyeargap)
            if maxgap > 0:
                temp['label'] = '教育间隔'
                temp['error'] = '候选人的教育经历时间有' + str(maxgap) + '年的间隔'
                return temp
            else:
                return False
        else:
            return False

    def worktimegap(self, singaldata):
        workdata = singaldata['workExperience']
        try:
            workyear = singaldata['workYear']
            if len(workyear) > 0:
                workyeargap, workmongap = util().gap(workdata, self.updatetime, 1)
                jobhopping = []
                if workyear != 0:
                    year, month = util().time_difference(min(self.workStrattime), max(self.workEndtime))
                    if month > 6:
                        year = year + 1
                    if workyear != year:
                        temp = {}
                        temp['label'] = '工作年限异常'
                        temp['error'] = '候选人工作经验的年限与工作经历的时间不符'
                        jobhopping.append(temp)
                count = len(workdata) + 1
                if len(workdata) > 1:
                    for wy, wk in zip(workyeargap, workmongap):
                        count -= 1
                        strsum = count - 1
                        if wy != 0:
                            temp = {}
                            temp['label'] = '工作间隔'
                            temp['error'] = '候选人在第' + str(strsum) + '段工作经历与第' + str(count) + '段工作经历之间的空档期为' + str(
                                wy) + '年'
                            jobhopping.append(temp)
                        elif wy == 0 and wk > 6:
                            temp = {}
                            temp['label'] = '工作间隔'
                            temp['error'] = '候选人在第' + str(strsum) + '段工作经历与第' + str(count) + '段工作经历之间的空档期超过半年'
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

    # 滥用精通
    def genera_use(self, sigaldata):
        try:
            skill = sigaldata['skill']
            if isinstance(skill, list):
                for sk in skill:
                    skill += sk[1]
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
    cvdata={"phone": "",
        "birthday": "",
        "age": "NumberInt(27)",
        "gender": "男",
        "name": "宋先生",
        "nativePlace": "",
        "photo": "",
        "email": "",
        "blogs": "",
        "nation": "",
        "domicilePlace": "",
        "currentAddress": "北京-昌平区",
        "marital": "",
        "IDcard": "",
        "contactAddress": "",
        "highestEducationDegree": "",
        "highestEducationAcademy": "北京联合大学",
        "highestEducationMajor": "计算机科学与技术",
        "graduationDate": "",
        "startWorkingDate": "",
        "workYear": "NumberInt(4)",
        "recentCompany": "",
        "recentIndustry": "",
        "recentPosition": "",
        "currentSalary": "",
        "politicsStatus": "",
        "expectedOccupation": "教育产品开发;培训策划;教学/教务管理人员",
        "expectedSalary": "15000-25000元/月",
        "expectedWorkplace": "北京",
        "expectedCompanyNature": "",
        "expectedWorkNature": "全职",
        "expectedIndustry": "",
        "expectedStatus": "离职",
        "expectedEntryDate": "",
        "selfEvaluation": "",
        "educationExperience": [{
            "educationTimePeriod": "",
            "educationStartTime": "2012-09-01 00:00:00",
            "educationEndTime": "2016-06-01 00:00:00",
            "educationSchool": "北京联合大学",
            "educationMajor": "计算机科学与技术",
            "educationDegree": "4",
            "educationMajorDescription": "",
            "educationScore": ""
        }],
        "workExperience": [{
            "workTimePeriod": "",
            "workStartTime": "2018-03-01 00:00:00",
            "workEndTime": "",
            "workTime": "",
            "workCompany": "北京立思辰科技股份有限公司",
            "workCompanyCity": "",
            "workDepartment": "",
            "workPosition": "教育方案设计（人工智能）",
            "workCompanyIndustry": "",
            "workCompanyNature": "",
            "workCompanyScale": "",
            "workSalary": "1000115000",
            "workDescription": "1.负责人工智能教育整体方案设计: 课程，实验室，培训，竞赛，企业实践等等。2.完成高中阶段，人工智能课程的大致讲义PPT的编辑与整理优化。3.人工智能方面的技术点划分归类总结，不同阶段，不同教育环节的分配及侧重。4.配合其他部门，从技术热门及落地等层面，给予具体的建议参考，以及关键点的梳理。形成方案：《人工智能教育整体规划方案》课程，实验室，教师培训，学生竞赛等《人工智能高中具体规划》包含哪些章节，具体怎么安排，有什么内容等《人工智能课程高中初步讲义PPT》概念理论，热门算法及应用等 275页《人工智能教育市场化分析及落地》调研对比有方教育，商汤，科大讯飞《人工智能具体教学设计》课程标准，章节安排，教案及讲义案例等等",
            "workDuty": "",
            "workPerformance": "",
            "workSummary": "",
            "workSubordinate": "",
            "workResignationReason": ""
        }, {
            "workTimePeriod": "",
            "workStartTime": "2016-03-01 00:00:00",
            "workEndTime": "2018-02-01 00:00:00",
            "workTime": "",
            "workCompany": "北京奥鹏远程教育中心有限公司",
            "workCompanyCity": "",
            "workDepartment": "",
            "workPosition": "内容产品研发运营",
            "workCompanyIndustry": "",
            "workCompanyNature": "",
            "workCompanyScale": "",
            "workSalary": "0800110000",
            "workDescription": "负责慕课网技能提升类课程产品项目的市场调研，规划设计，研发制作，后期维护等，广受用户好评。完成制作上线互联网课程产品总计80余门，其中安卓，测试免费课50余门，学习人数总计超10万。安卓，Java，测试，人工智能付费课程20余门，学习人数总计超1万，完成课程收入近200万。在同等职位下，业绩排第二。沟通课程产品的讲师，总计达到50余个讲师，基本主要都是来自BAT的工程师。完成课程时长总计达到500小时以上。负责过人工智能，Java，Android，测试等方向的课程产品研发制作，如人工智能框架Tensorflow原理到项目实践，Java SSM电商项目前后端，SSM在线教育项目，Springboot博客系统，Java秒杀优化等，Android智能管家第三方项目，视频sdk封装组件化项目，IM即时通讯项目，打车定位项目架构优化，热修复与插件化项目，Web自动化测试selenium从原理到实践，Python接口到自动化测试，性能测试Jmeter,Loadrunner等等。具体负责课程项目代码研发，调研用户对于课程产品的反馈，修改完善代码，改进自己的课程产品。此外，管理课程项目进度，与其他部门合作沟通，维护自己的课程产品，营销推广课程产品到各大平台。 现在已有超10万用户，观看过课程视频，体验过自己的项目，评价都很不错。",
            "workDuty": "",
            "workPerformance": "",
            "workSummary": "",
            "workSubordinate": "",
            "workResignationReason": ""
        }, {
            "workTimePeriod": "",
            "workStartTime": "2015-08-01 00:00:00",
            "workEndTime": "2016-02-01 00:00:00",
            "workTime": "",
            "workCompany": "北京达内时代科技有限公司",
            "workCompanyCity": "",
            "workDepartment": "",
            "workPosition": "GSD1510安卓助教",
            "workCompanyIndustry": "",
            "workCompanyNature": "",
            "workCompanyScale": "",
            "workSalary": "0400106000",
            "workDescription": "达内时代科技集团有限公司，安卓开发班担任助教兼技术班长，负责学员技术答疑及技术知识点讲解。现为高级软件工程师，安卓高级工程师。熟练掌握了安卓四大组件Activity,Service,BroadcastReceiver,ContentProvider的使用，线程的优化和安卓多种动画的实现，以及手机安卓的网络与SQLite数据库的开发使用，开发媒体播放器和手机打击类游戏的基本开发流程，在最后考核中获得满分。同时顺应行业发展趋势，熟悉JavaScript，html5，css3的混合编程，使其跨平台开发。",
            "workDuty": "",
            "workPerformance": "",
            "workSummary": "",
            "workSubordinate": "",
            "workResignationReason": ""
        }, {
            "workTimePeriod": "",
            "workStartTime": "2015-04-01 00:00:00",
            "workEndTime": "2015-08-01 00:00:00",
            "workTime": "",
            "workCompany": "北京云景科技有限公司",
            "workCompanyCity": "",
            "workDepartment": "",
            "workPosition": "安卓开发工程师",
            "workCompanyIndustry": "",
            "workCompanyNature": "",
            "workCompanyScale": "",
            "workSalary": "0200104000",
            "workDescription": "负责移动app开发测试，编写相关需求文档，以及设计文档，及后期产品维护。主要应用AppCan和Unity开发一些移动应用app或者移动版3d游戏。其作品多次获得国家级，市级科技奖项。",
            "workDuty": "",
            "workPerformance": "",
            "workSummary": "",
            "workSubordinate": "",
            "workResignationReason": ""
        }, {
            "workTimePeriod": "",
            "workStartTime": "2012-09-01 00:00:00",
            "workEndTime": "2015-08-01 00:00:00",
            "workTime": "",
            "workCompany": "北京联合大学就业服务中心",
            "workCompanyCity": "",
            "workDepartment": "",
            "workPosition": "电子屏制作播放专员",
            "workCompanyIndustry": "",
            "workCompanyNature": "",
            "workCompanyScale": "",
            "workSalary": "0000001000",
            "workDescription": "在北京联合大学就业服务中心勤工俭学三年，担任电子屏制作播放专员，兼办公室数据统计，共参与组织招聘会四十余场，服务毕业生上万人次，每场主要负责电子屏制作播放，以及招聘会会场组织与服务，受到负责老师的一致认可与好评。",
            "workDuty": "",
            "workPerformance": "",
            "workSummary": "",
            "workSubordinate": "",
            "workResignationReason": ""
        }],
        "projectExperience": [],
        "trainingExperience": [],
        "associationExperience": [],
        "publishPaper": [],
        "publishBook": [],
        "publishPatent": [],
        "skill": [],
        "certificate": [],
        "language": [],
        "award": [],
        "hobby": [],
        "advantage": "",
        "_id": "N7p7DBeE6lKOrYKUoDC(WA",
        "insertTime": "",
        "updateTime": "2019-04-02 00:00:00",
        "source": "",
        "fileFormat": "",
        "filePath": "",
        "attachmentPath": "",
        "plainText": "",
        "sameCVid": "",
        "md5": "",
        "jobTitle": "教育方案设计（人工智能）",
        "highestEducationBackground": "本科",
        "zhilianLabels": ["智联白领"]
    }
    print(riskPoint().identification(cvdata))
