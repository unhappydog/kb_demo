import re
from datetime import datetime
from collections import defaultdict
from core.cvprase.Util.util import util
class htmlparse(object):

    def parsemain(self,root):
        srthtml = self.gethtml(root)
        objhtml = htmlparse()
        totaldict = {}
        strsplit = re.compile('<div class="resume-preview-all">(.*?)</div>').findall(srthtml)
        compl = re.compile('<div class="resume-preview-dl">.*?<div class="resume-preview-all">').findall(srthtml)
        dict = objhtml.cvtop(srthtml)
        for sp in strsplit:
            if '求职意向' in sp:
                dict = util().integration(dict, objhtml.htmlintent(sp))
            if '自我评价' in sp:
                totaldict['selfEvaluation'] = objhtml.selfeval(sp)
            if "".join(re.compile('<h3.*>(.*)</h3>').findall(sp)) == '工作经历':
                complex = "".join([x for x in compl if '工作描述' in x])
                totaldict['workExperience'] = objhtml.work_exprience(sp, complex)
            if '项目经历' in sp:
                complex = "".join([x for x in compl if '项目描述' in x])
                totaldict['projectExperience'] = objhtml.project_exprience(sp, complex)
            if '教育经历' in sp:
                edustr = "".join([x for x in compl if '本科' in x or '硕士' in x])
                if edustr:
                    totaldict['educationExperience'] = objhtml.edu_exprience(edustr)
                else:
                    totaldict['educationExperience'] = objhtml.edu_exprience(sp)
            if '培训经历' in sp:
                totaldict['trainingExperience'] = objhtml.training_exprience(srthtml)
            if '语言能力' in sp:
                totaldict['language'] = objhtml.language(sp)
            if '证书' in sp:
                totaldict['certificate'] = objhtml.certificate(sp)
            if '专业技能' in sp:
                totaldict['skill'] = objhtml.skill(sp)
            if '在校学习情况' in sp:
                strcol = "".join([x for x in compl if '曾获' in x])
                totaldict['award'] = objhtml.study(sp + strcol)
            if '在校实践经验' in sp:
                strcol = "".join([x for x in compl if '实践描述' in x])
                totaldict['associationExperience'] = objhtml.exprience(sp + strcol)
            # if '受到奖励' in sp:
            #     print(sp)
            #     totaldict['受到奖励'] = objhtml.reward(sp)
            if '兴趣爱好' in sp or '个人爱好' in sp:
                if objhtml.job(re.sub('<br>', '', sp)):
                    totaldict['hobby'] = objhtml.job(re.sub('<br>', '', sp))
        res = util().integration(dict, totaldict)
        return res

    def gethtml(self, path):
        oricode = ''
        with open(path, 'r', encoding='utf-8') as f:
            for li in f:
                oricode += li.strip('\n ')
            f.close()
        return oricode

    def cvtop(self, html):
        # 简历开始模块
        totaidict = {}
        da = "".join(re.compile('<div class="resume-preview-title">(.*?)</div>').findall(html))
        updatetime = "".join(re.compile('<strong>(\d.*\d)</strong>').findall(da))
        cvidparent = "".join(re.compile('<div class="resume-preview-center">(.*?)</div>').findall(html))
        id = "".join(re.compile('<span class="resume-left-tips-id">(.*?)</span>').findall(cvidparent))
        totaidict['updateTime'] = datetime.strptime(updatetime.replace('.', '-'), "%Y-%m-%d")
        totaidict['id'] = id
        # 称呼
        name = "".join(re.compile('<div class="main-title-fl fc6699cc">(.*?)</div>').findall(html))
        totaidict['name'] = name
        # 个人信息
        summary = "".join(re.compile('<div class="summary">(.*)<div class="summary-bottom">').findall(html))
        basicinfo = "".join(re.compile('<span>(.*?)</span>').findall(summary))
        basicloc = "".join(re.compile('<br>(.*)</div>').findall(summary)).split('|')
        person = []
        for i in re.sub('[&nbsp;]', '#', basicinfo).strip('\t').split('#'):
            if i != '':
                person.append(i)
        totaidict['gender'] = person[0]
        totaidict['age'] = int("".join(re.compile('(\d{2})岁').findall(person[1])))
        strdate = re.sub("年", "-", "".join(re.compile('\d{4}.\d+').findall(person[1])))
        date_time = datetime.strptime(strdate, '%Y-%m')
        totaidict['birthday'] = date_time
        print(date_time)
        for i in person:
            if '工作经验' in i:
                totaidict['workYear'] = int("".join(re.compile('(\d+).*').findall(i)))

            if '婚' in i:
                totaidict['marital'] = i
        if '婚' in person[-1]:
            totaidict['highestEducationBackground'] = person[-2]
        else:
            totaidict['highestEducationBackground'] = person[-1]

        for lo in basicloc:
            if '现居住地' in lo:
                totaidict['currentAddress'] = lo.split('：')[1]
            elif '户口' in lo:
                totaidict['domicilePlace'] = lo.split('：')[1]
            else:
                totaidict['politicsStatus'] = lo
        return totaidict

    def htmlintent(self, strhtml):

        dict = {}
        intenttitle = re.compile('<td width="85" align="right">(.*?)</td>').findall(strhtml)
        intentinfo = re.compile('<td>(.*?)</td>').findall(strhtml)
        translate = {"期望工作地区": 'expectedWorkplace',
                     "期望月薪": 'expectedSalary',
                     "目前状况": 'expectedStatus',
                     "期望工作性质": 'expectedWorkNature',
                     "期望从事职业": 'expectedOccupation',
                     "期望从事行业": 'expectedIndustry'}
        for ti, fo in zip(intenttitle, intentinfo):
            for k, v in translate.items():
                if ti.strip('：') == k:
                    dict[v] = fo

        return dict

    def selfeval(self, html):
        selfeval = re.sub('[<br>\\t]', '',
                          "".join(re.compile('<div class="resume-preview-dl rd-break">(.*)').findall(html)))
        return selfeval

    def work_exprience(self, sp, html):
        work_split = sp + html
        work_dict = defaultdict(list)
        h2title = re.compile("<h2>(.*?)</h2>").findall(work_split)
        h5title = re.compile('<h5>(.*?)</h5>').findall(work_split)
        industry = re.compile('</h5><div class="resume-preview-dl">(.*?)</div>').findall(work_split)
        des = re.compile('<td>(.*?)</td>').findall(work_split)
        for ht, hi, ind, de in zip(h2title, h5title, industry, des):
            hh = []
            temp = {}
            for res in ht.split('&nbsp;'):
                if res != '':
                    hh.append(res)
            temp['workStartTime'] = datetime.strptime(hh[0].split('-')[0].replace('.', '-'), "%Y-%m")
            endtime = hh[0].split(' ')[1].strip(' ')
            if endtime == '至今':
                temp['workEndTime'] = ''
            else:
                temp['workEndTime'] = datetime.strptime(endtime.replace('.', '-'), '%Y-%m')
            temp['workCompany'] = hh[1]
            temp['workTimePeriod'] = "".join(re.compile('\((.*)\)').findall(hh[2]))
            if len(hi.split('|')) > 1:
                temp['workPosition'] = hi.split('|')[0]
                temp['workSalary'] = hi.split('|')[1]
            else:
                temp['workPosition'] = hi
            if len(ind.split('|')) == 1:
                temp['workCompanyIndustry'] = "".join(re.findall('(.*)<div',ind.split('|')[0]))
            elif len(ind.split('|')) != 1:
                if len(ind.split('|')) > 3:
                    temp['workCompanyIndustry'] = ind.split('|')[0]
                else:
                    try:
                        temp['workCompanyNature'] = ind.split('|')[1].split('：')[1]
                        if len(ind.split('|')) == 3:
                            temp['workCompanyScale'] = ind.split('|')[2]
                    except:
                        temp['workCompanyIndustry'] = ind

            else:
                if '<' in ind:
                    temp['workCompanyIndustry'] = "".join(re.compile('<.*>(.*)').findall(ind))
                else:
                    temp['workCompanyIndustry'] = ind
            temp['workDescription'] = re.sub('[<br>\\t]', '', de)
            work_dict['workExperience'].append(temp)
        return work_dict['workExperience']

    def project_exprience(self, sp, html):
        projectdict = defaultdict(list)
        project = sp + html
        h2title = re.compile('<h2>(.*?)</h2>').findall(project)
        desbody = re.compile('<tbody>(.*?)</tbody>').findall(project)
        mebody = []
        # 去重
        for me in desbody:
            if me not in mebody:
                mebody.append(me)
        for h, d in zip(h2title, mebody):
            temp = {}
            temp['projectStartTime'] = datetime.strptime(h.split(' ')[0].strip('-').replace('.', '-'), '%Y-%m')
            endtime = h.split(' ')[1]
            if endtime == '至今':
                temp['projectEndTime'] = ''
            else:
                temp['projectEndTime'] = datetime.strptime(
                    "".join(re.compile('\d{4}.\d{2}').findall(endtime)).replace('.', '-'), '%Y-%m')
            temp['projectName'] = "".join(h.split(' ')[2:])
            destitle = re.compile('<td width="60">(.*?)</td>').findall(d)
            desinfo = re.compile('<td>(.*?)</td>').findall(d)
            if len(destitle) == 1:
                temp["projectDescription"] = "".join(desinfo)
            else:
                dict = {"项目描述": 'projectDescription', "软件环境": 'projectSoftwareEnv', "硬件环境": 'projectHardwareEnv',
                        "开发工具": 'projectTool'}
                for rep, pde in zip(destitle, desinfo):
                    for k, v in dict.items():
                        if rep.strip('：') == k:
                            temp[v] = re.sub('[<br>\\t]', '', pde)
            projectdict['projectExperience'].append(temp)
        return projectdict['projectExperience']

    def edu_exprience(self, html):
        edudict = defaultdict(list)
        edu_split = re.compile('<div class="resume-preview-dl">(.*?)</div>').findall(html)
        if edu_split:
            edu_split = re.compile('<div class="resume-preview-dl">(.*?)</div>').findall(html)
        else:
            edu_split = re.compile('<div class="resume-preview-dl">(.*)').findall(html)
        stredu = "".join(edu_split)

        if len(edu_split) == 1:
            temp = {}
            edulist = []
            for i in stredu.split('&nbsp;'):
                if i != '':
                    edulist.append(i.strip('<br>'))
            temp['educationStartTime'] = datetime.strptime(edulist[0].split('-')[0].strip('-').replace('.', '-'),
                                                           '%Y-%m')
            endtime = edulist[0].split(' ')[1].strip(' ')
            if endtime == '至今':
                temp['educationEndTime'] = ''
            else:
                temp['educationEndTime'] = datetime.strptime(endtime.replace('.', '-'), '%Y-%m')
            try:
                temp['educationSchool'] = "".join(
                    re.compile('(.*大学)|(.*学院)').findall(edulist[1].strip('\t').strip(' ')))
            except:
                temp['educationSchool'] = edulist[1].strip('\t').strip(' ')
            temp['educationMajor'] = edulist[2]
            temp['educationDegree'] = edulist[-1]
            edudict['educationExperience'].append(temp)
        else:
            for es in edu_split:
                temp = {}
                edulist = []
                for i in es.split('&nbsp;'):
                    if i != '':
                        edulist.append(i.strip('<br>'))
                if len(edulist) < 3:
                    continue
                else:
                    temp['educationStartTime'] = datetime.strptime(
                        edulist[0].split('-')[0].strip('-').replace('.', '-'), '%Y-%m')
                    endtime = edulist[0].split(' ')[1].strip(' ')
                    if endtime == '至今':

                        temp['educationEndTime'] = ''
                    else:
                        temp['educationEndTime'] = datetime.strptime(endtime.replace('.', '-'), '%Y-%m')
                    temp['educationSchool'] = edulist[1]
                    temp['educationMajor'] = edulist[2]
                    temp['educationDegree'] = edulist[-1]
                    edudict['educationExperience'].append(temp)
        return edudict['educationExperience']

    def training_exprience(self, html):
        trainingdict = defaultdict(list)
        trainsplit = re.compile('<div class="resume-preview-top resume-line-height">(.*?)</div>').findall(html)
        title = re.compile('<h3 class="fc6699cc">(.*?)</h3>').findall(html)
        frontext = html.split('培训经历')[1]
        if title.index('培训经历') < len(title) - 1:
            behind = frontext.split('<h3 class="fc6699cc">' + title[title.index('培训经历') + 1] + '</h3>')[0]
        else:
            behind = frontext.split('<h3 class="fc6699cc">' + '培训经历' + '</h3>')[0]
        h2title = re.compile('<h2>(.*?)</h2>').findall(behind)
        dict = {"培训机构": 'trainingOrg', "培训地点": 'trainingPlace', '所获证书': 'trainingCertificate'}
        for h2, spl in zip(h2title, trainsplit):
            temp = {}
            h2split = [h for h in h2.split('&nbsp;') if h != '']
            temp['trainingStartTime'] = datetime.strptime(h2split[0].split('-')[0].strip(' ').replace('.', '-'),'%Y-%m')
            if '至今' in h2split[0].split('-')[1]:
                temp['trainingEndTime'] = ''
            else:
                temp['trainingEndTime'] = datetime.strptime(h2split[0].split('-')[1].strip(' ').replace('.', '-'),
                                                            '%Y-%m')
            temp['trainingCourse'] = h2split[1].strip(' ')
            contenttitle = re.compile('<td width="60">(.*?)</td>').findall(spl)
            content = re.compile('<td>(.*?)</td>').findall(spl)
            for ct, cn in zip(contenttitle, content):
                for k, v in dict.items():
                    if ct.strip('：') == k:
                        temp[v] = cn
            trainingdict['trainingExperience'].append(temp)
        return trainingdict['trainingExperience']

    def job(self, html):
        strjob = "".join(re.compile('<div class="resume-preview-dl">(.*)').findall(html))
        return strjob

    def language(self, html):
        laudict = defaultdict(list)
        splitlaulist = "".join(
            re.compile('<div class="resume-preview-dl resume-preview-line-height">(.*)').findall(html)).split('<br>')
        laulist = [i for i in splitlaulist if i != '']
        for lau in laulist:
            temp = {}
            temp['languageKind'] = lau.split('：')[0]
            for i in lau.split('：')[1].split('|'):
                if '读写' in i:
                    temp['readingWritingLevel'] = "".join(re.compile('读写能力(.*)').findall(i))
                elif '听说' in i:
                    temp['listeningSpeakingLevel'] = "".join(re.compile('听说能力(.*)').findall(i))
            laudict['language'].append(temp)
        return laudict['language']

    def skill(self, sp):
        skilldict = defaultdict(list)
        strskill = "".join(re.compile('<div class="resume-preview-dl">(.*)').findall(sp))
        splitskill = strskill.split('<br>')
        for line in splitskill:
            if len(line.split('：')) > 1:
                temp = {}
                temp['name'] = line.split('：')[0].strip(' ')
                temp['skillMastery'] = line.split('：')[1].strip(' ')
                skilldict['skill'].append(temp)
            else:
                continue
        if len(skilldict['skill']) > 1:

            return skilldict['skill']
        else:
            skilldict['skill'] = strskill.replace('<br>', '\n')
            return skilldict['skill']

    def certificate(self, sp):
        certidict = defaultdict(list)
        if '证书' in "".join(re.compile('<h3 class="fc6699cc">(.*)</h3>').findall(sp)):
            cert = re.compile('<h2>(.*?)</h2>').findall(sp)
            strcert = "".join(re.compile('<h2>(.*?)</h2>').findall(sp))
            if len(cert) == 1:
                temp = {}
                certinfo = [i for i in strcert.split('&nbsp;') if i != '']
                temp['time'] = datetime.strptime(certinfo[0].replace('.', '-'), '%Y-%m')
                temp['name'] = certinfo[1]
                certidict['certificate'].append(temp)
            else:
                for line in cert:
                    temp = {}
                    info = [i for i in "".join(line).split('&nbsp;') if i != '']
                    temp['time'] = datetime.strptime(info[0].replace('.', '-'), '%Y-%m')
                    temp['name'] = info[1]
                    certidict['certificate'].append(temp)
            return certidict['certificate']

    def study(self, sp):
        studydict = defaultdict(list)
        strsp = "".join(re.compile('<h3.*>.*?</h3>(.*)').findall(sp))
        for i in strsp.split('<h2>')[1:]:
            temp = {}
            h2title = "".join(re.compile('(.*?)</h2>').findall(i))
            if re.compile('\d+.*\d').findall(h2title):
                strtime = "".join(re.compile('(\d{4}.\d{2})曾').findall(h2title))
                temp['time'] = datetime.strptime(strtime.replace('.', '-'), '%Y-%m')
            name = [i for i in h2title.split(' ') if i != '']
            temp['awardKind'] = "".join(name[1:])
            # pro = re.compile('<div class="resume-preview-dl">(.*?)</div>').findall(i)
            # for po in pro:
            #     if po == '':
            #         continue
                # tdtitle = "".join(re.compile('<td width="60">(.*?)：</td>').findall(po))
                # if '活动描述' in tdtitle:
                #     temp['activedescription'] = re.sub('[<br>]', '', "".join(re.compile('<td>(.*?)</td>').findall(po)))
            studydict['award'].append(temp)
        return studydict['award']

    def reward(self, sp):
        strreward = "".join(re.compile('<div class="resume-preview-dl">(.*)').findall(sp))
        resreward = re.sub('[●	]', '', strreward.replace('<br>', ';'))
        return resreward

    def exprience(self, sp):
        exprdict = defaultdict(list)
        h2title = re.compile('<h2>(.*?)</h2>').findall(sp)
        tdtitle = re.compile('<td width="60">(.*?)</td>').findall(sp)
        tdco = re.compile('<td>(.*?)</td>').findall(sp)
        if len(h2title) != 1:
            for i, j, k in zip(h2title, tdtitle, tdco):
                temp = {}
                line = [k for k in i.split('&nbsp;') if k != '']
                temp['practiceStartTime'] = datetime.strptime(line[0].split('-')[0].replace('.', '-'), '%Y-%m')
                temp['practiceEndTime'] = datetime.strptime(line[0].split('-')[1].strip(' ').replace('.', '-'), '%Y-%m')
                temp['practiceName'] = line[1]
                if '实践描述' in j :
                    temp['practiceDescription'] = k
                exprdict['在校实践经验'].append(temp)
        else:
            temp = {}
            line = [k for k in "".join(h2title).split('&nbsp;') if k != '']
            temp['practiceStartTime'] = datetime.strptime(line[0].split('-')[0].replace('.', '-'), '%Y-%m')
            temp['practiceEndTime'] = datetime.strptime(line[0].split('-')[1].strip(' ').replace('.', '-'), '%Y-%m')
            temp['practiceName'] = line[1]
            tdco = "".join(re.compile('<td>(.*?)</td>').findall(sp))
            temp['practiceDescription'] = tdco
            exprdict['在校实践经验'].append(temp)
        return exprdict['在校实践经验']
