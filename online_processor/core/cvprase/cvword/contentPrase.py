from collections import defaultdict
from datetime import datetime
from core.cvprase.Util.util import util
import re


class ContentParse(object):

    def basic_info(self, table, para, name):
            basicdict = {}
            basicdict['id'] = re.sub('[\u3000 ：]', '', para[0].text).replace('ID','')

            updatetime = []

            for el in table[0].rows:
                for cell in el.cells:

                    updatematch = re.compile('\d.*\d').findall(cell.text)
                    if updatematch:
                        updatetime = "".join(re.compile('\d.*\d').findall(cell.text)).replace('.', '-')

            basicdict['updateTime'] = datetime.strptime(updatetime, '%Y-%m-%d')
            basicdict['name'] = name.split(' ')[0].strip(' ')
            row_content = []
            for j in table[1:3]:
                for k, row in enumerate(j.rows):
                    s = []
                    for cell in row.cells:
                        if cell.text == '':
                            continue
                        else:
                            s.append(cell.text)
                    row_content.append(s)
            major = ['博士', '硕士', '本科', '大专']
            dict={'期望工作地区':'expectedWorkplace','期望月薪':'expectedSalary','目前状况':'expectedStatus','期望工作性质':'expectedWorkNature','期望从事职业':'expectedOccupation','期望从事行业':'expectedIndustry'}
            for line in row_content:

                strline = "".join(line)
                if '男' in strline or '女' in strline:
                    basicinfo = []
                    basicdict['gender'] = strline.split(' ')[0]
                    for j in strline.split(' '):
                        if len(j) > 1:
                            basicinfo.append(j)
                    for i in basicinfo:
                        if '岁' in i:
                            basicdict['age'] = int("".join(re.compile('(\d+)').findall(i)))
                        if re.compile('(\d+.\d+)月').findall(i):
                            birthday = "".join(re.compile('(\d+.\d+)月').findall(i)).replace('年', '-')
                            basicdict['birthday'] = datetime.strptime(birthday, "%Y-%m")
                        if '工作经验' in i:
                            basicdict['workYear'] = int("".join(re.compile('(\d+).*').findall(i)))
                        if '婚' in i:
                            basicdict['marital'] = re.sub('[\\xa0]', '', i)
                        if '现居住地' in i:
                            start = basicinfo.index(i)
                            address = list(set(basicinfo[start:-1]))
                            for i in address:
                                if '现居住地' in i:
                                    basicdict['currentAddress'] = " ".join(address[address.index(i):]).split('：')[1].replace('户口','')
                        if '户口' in i:
                            basicdict['domicilePlace '] = i.split('：')[1]
                        majinfo = [x for x in major if x in i]
                        if majinfo:
                            basicdict['highestEducationBackground'] = "".join(majinfo)
                if len(line)>1:
                    for k,v in dict.items():
                        if line[0].strip('：')==k:
                            basicdict[v]=line[1].strip(' ')
            if para[3].text:
                basicdict['selfEvaluation'] =  para[3].text
            return basicdict

    def work(self,worinfo):
        workdict=defaultdict(list)
        worsplit=util().listsplit(worinfo)
        for pro in range(0,len(worsplit)):
            temp={}
            if pro<=len(worsplit)-2:
                newinfo=worinfo[worsplit[pro]:worsplit[pro+1]]
            else:

                newinfo = worinfo[worsplit[pro]:]
            if newinfo:
                strline = "".join(newinfo[0])
                wortitle = "".join(re.compile('\d{4}.\d{2} - .*').findall(strline))
                if wortitle:
                    temp['workStartTime'] = datetime.strptime(wortitle.split('-')[0].strip(' ').replace('.', '-'), '%Y-%m')
                    worktime = "".join(re.compile('\d{4}.\d{2} - \d{4}.\d{2}').findall(strline))
                    if worktime:
                        temp['workEndTime'] = datetime.strptime(worktime.split('-')[1].strip(' ').replace('.', '-'),'%Y-%m')
                    else:
                        temp['workEndTime'] = ''
                    company = [i for i in strline.split('\xa0') if i != '']
                    if len(company) == 3:
                        temp['workCompany'] = company[-2]
                        temp['workTimePeriod'] ="".join(re.compile('\((.*)\)').findall(company[-1]))
                    else:
                        temp['workCompany'] = company[-1]

                if len("".join(newinfo[1]).split('|'))>1:
                    temp['workPosition']="".join(newinfo[1]).split('|')[0].strip(' ')
                    temp['workSalary']="".join(newinfo[1]).split('|')[1].strip(' ')
                else:
                    temp['workPosition']="".join(newinfo[1]).strip(' ')
                cominfo="".join(newinfo[2]).split('|')
                if len(cominfo)==1:
                    temp['workCompanyIndustry']="".join(cominfo).strip(' ')
                elif len(cominfo)==2:
                    temp['workCompanyIndustry']=cominfo[0].strip(' ')
                    temp['workCompanyNature']=cominfo[1].strip(' ')
                elif len(cominfo)==3:
                    temp['workCompanyIndustry'] = cominfo[0].strip(' ')
                    temp['workCompanyNature'] = cominfo[1].split("：")[1].strip(' ')
                    temp['workCompanyScale']=cominfo[2].split("：")[1].strip(' ')
                if len(newinfo)==3:
                    temp['workDescription']=re.sub('[\n\xa0]','',"".join(newinfo[2][1])).strip(' ')
                elif len(newinfo)==4:
                    temp['workDescription']=re.sub('[\n\xa0]','',"".join(newinfo[3][1])).strip(' ')
            else:
                continue
            workdict['work'].append(temp)
        return workdict['work']

    def project(self,proinfo):
        projectdict=defaultdict(list)
        prosplit=util().listsplit(proinfo)
        for pro in range(0,len(prosplit)):
            temp={}
            if pro<=len(prosplit)-2:
                newinfo=proinfo[prosplit[pro]:prosplit[pro+1]]
            else:
                newinfo = proinfo[prosplit[pro-1]:]
            for line in newinfo:
                         strline="".join(line)
                         protitle="".join(re.compile('\d{4}.\d{2} - (.*)').findall(strline))
                         if protitle:
                            protime="".join(re.compile('\d{4}.\d{2} - \d{4}.\d{2}').findall(strline))
                            if protime:
                                     temp['projectStartTime']=datetime.strptime(protime.split('-')[0].strip(' ').replace('.','-'),"%Y-%m")
                                     temp['projectEndTime']=datetime.strptime(protime.split('-')[1].strip(' ').replace('.','-'),'%Y-%m')
                                     temp['projectName'] ="".join(re.compile('.*\d(.*)').findall(strline)).strip(' ')
                            else:
                                     protime = "".join(re.compile('\d{4}.\d{2} - 至今').findall(strline))
                                     temp['projectStartTime'] = datetime.strptime(protime.split('-')[0].strip(' ').replace('.', '-'), "%Y-%m")
                                     temp['projectEndTime'] = ''
                                     temp['projectName'] = "".join(re.compile('至今(.*)').findall(strline)).strip(' ')
                         else:
                             dict={'项目描述':'projectDescription','责任描述':'projectDuty','软件环境':'peojectSoftwareEnv','硬件环境':'projectHardwareEnv','开发工具':'projectTool'}
                             for k,v in dict.items():
                                 if line[0]==k:
                                     temp[v]=re.sub('[\n \xa0]','',line[1])
            projectdict['project'].append(temp)
        return projectdict['project']

    def eduction(self,eduinfo):
        edudict = defaultdict(list)
        for edu in eduinfo:
            temp = {}
            strmatch = "".join(re.compile('\d{4}.\d{2} - \d{4}.\d{2}').findall(edu))
            if strmatch:
                temp['educationStartTime'] = datetime.strptime(strmatch.split('-')[0].strip(' ').replace('.', '-'),
                                                               '%Y-%m')
                temp['educationEndTime'] = datetime.strptime(strmatch.split('-')[1].strip(' ').replace('.', '-'),
                                                             '%Y-%m')
            eduplit = [i for i in edu.split('\xa0') if i != '']
            temp['educationSchool'] = eduplit[1]
            temp['educationMajor'] = eduplit[-2]
            temp['educationDegree'] = eduplit[-1]
            edudict['eduction'].append(temp)
        return edudict['eduction']


    def training(self,traininginfo):
        trainingdict=defaultdict(list)
        listsp =util().listsplit(traininginfo)
        dict={'培训机构':'trainingOrg','培训地点':'traininigPlace','培训描述':'trainingDescription','所获证书':'trainingCertificate'}
        for pro in range(0, len(listsp)):
            temp = {}
            if pro <= len(listsp) - 2:
                newinfo = traininginfo[listsp[pro]:listsp[pro + 1]]
            else:
                newinfo = traininginfo[listsp[pro - 1]:]
            for line in newinfo:
                if len(line)==1:
                    strline = [i for i in "".join(line).split('\xa0') if i != '']
                    temp['trainingStartTime'] = datetime.strptime(strline[0].split('-')[0].strip(' ').replace('.', '-'),'%Y-%m')
                    if '至今' in strline[0].split('-')[1]:
                        temp['trainingEndTime']=''
                    else:
                        temp['trainingEndTime'] = datetime.strptime(strline[0].split('-')[1].strip(' ').replace('.', '-'),'%Y-%m')
                    temp['trainingCourse'] = strline[1].strip(' ')
                else:
                    for k, v in dict.items():
                        if k == line[0].strip("："):
                            temp[v] = line[1].replace('\n', ';')
            trainingdict['trainingdict'].append(temp)
        return trainingdict['trainingdict']

    def certifi(self,certinfo):
        certifidict=defaultdict(list)
        for ce in certinfo:
            temp={}
            line=[i for i in ce.split('\xa0') if i!='']

            if len(line)>1:
                temp['time']=datetime.strptime(line[0].strip(' ').replace('.','-'),'%Y-%m')
                temp['name']=line[1].strip(' ')
            else:
                temp['name']=line[0].strip(' ')
            certifidict['certificate'].append(temp)
        return certifidict['certificate']


    def language(self,languageinfo):
        languagedict=defaultdict(list)
        for line in languageinfo:
                    temp={}
                    lau = "".join(line).split("：")
                    temp['languageKind'] = lau[0]
                    for i in lau[1].split('|'):
                        if '读写' in i:
                            temp['readingWritingLevel'] = "".join(re.compile('读写能力(.*)').findall(i)).strip(' ')
                        if '听说' in i:
                            temp['listeningSpeakingLevel'] = "".join(re.compile('听说能力(.*)').findall(i)).strip(' ')
                    languagedict['language'].append(temp)
        return languagedict['language']

    def asscciation(self,assoinfo):
            temp = {}
            for i in assoinfo:
                ass=[i for i in "".join(assoinfo[0]).split('\xa0') if i !='']
                temp['practiceStartTime']=datetime.strptime(ass[0].split('-')[0].strip(' ').replace('.','-'),'%Y-%m')
                temp['practiceEndTime']=datetime.strptime(ass[0].split('-')[1].strip(' ').replace('.','-'),'%Y-%m')
                temp['practiceName']=ass[1].strip(' ')
                if '实践描述' in i[0]:
                    temp['practiceDescription']=i[1].strip(' ')
            return temp
    def award(self,awardinfo):
        awardict=defaultdict(list)
        for i in awardinfo:
            stri="".join(i)
            if '活动描述' in stri:
                continue
            temp = {}
            if re.compile('\d{4}.\d{2}').findall("".join(stri)):
                temp['time']="".join(re.compile('\d{4}.\d{2}').findall("".join(stri)))
                awinfo=stri.split('\n')
                if '奖项描述' in awinfo[1]:
                    temp['awarddescription']=awinfo[1].split("：")[1].strip(' ')
            else:
                if '曾获' in stri:
                    temp['awardKind'] = "".join(re.compile('曾获(.*)').findall(stri)).replace(' ', '')
            awardict['award'].append(temp)
        return awardict['award']

    def skill(self,skllinfo):
        skilldict=defaultdict(list)
        for i in skllinfo:
            temp={}
            skstr=i.split('：')
            temp['name']=skstr[0]
            temp['skillMastery']=skstr[1]
            skilldict['skill'].append(temp)
        if skilldict['skill']:
            return skilldict['skill']
        else:
            return "\n".join(skllinfo)
    def job(self,joninfo):
        return "".join(joninfo).strip(' ')
