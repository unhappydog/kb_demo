from collections import defaultdict
from datetime import datetime
import fitz
import re
from core.cvprase.Util.proutil import proutil
class indivial(object):
    def basic_info(self, doc, pagenum):
        """
         简历最开始的部分：抽取用户的个人基本信息
        """
        page = doc.loadPage(0)
        rl1 = fitz.Rect(0, 0, 0, 0)
        rl2 = page.searchFor(list(pagenum.keys())[0])
        pripersonrect = proutil().location(rl1, rl2)
        text = proutil().textExtract(doc, 0, pripersonrect)
        subdict={}
        baseitem = []
        newlist=['gender','age','birthday','workYear','highestEducationBackground','marital']
        for g in text:
            baseitem.append([ss[4] for ss in g[1]])
        for key in baseitem:
             temp=[]
             for i in key:
                if i not in temp:
                    temp.append(i)
             strtemp=''.join(temp)
             if '更新时间' in strtemp:
                 subdict['updateTime']=datetime.strptime(temp[1].strip(' ').replace('.','-'),'%Y-%m-%d')
             if 'ID:' in strtemp:
                 subdict['id']=strtemp.split(':')[1].strip(' ')
             if '先生' in strtemp or '女士' in strtemp:
                 subdict['name']=strtemp
             if '岁' in strtemp:
                     for k,v in zip(temp,newlist):
                        if '工作经验' in strtemp:
                            subdict[v] = k
                        else:
                            new=newlist[:]
                            new.remove('workYear')
                            for k, v in zip(temp, new):
                                    subdict[v] = k

             if '户口' in strtemp:
                 if '|' in strtemp:
                     strno=''
                     for  i in "".join(strtemp.split('|')[0]).split("：")[1]:
                         if i not in strno:
                             strno+=i
                     subdict['currentAddress']=strno
                 elif '现居住地' in strtemp:
                     subdict['currentAddress']=strtemp.split('：')[1]
                 if '户口' in temp[-1]:
                     subdict['domicilePlace']=temp[-1].split('：')[1].strip(' ')
                 else:
                     subdict['domicilePlace']=temp[-2].split('：')[1].strip(' ')
                     subdict['politicsStatus']=temp[-1].strip(' ')
             elif '现居住地' in strtemp:
                 subdict['currentAddress']=strtemp.split('：')[1]

        subdict['age']=int(re.compile('\d+').findall(subdict['age'])[0])
        if [k for v,k in subdict.items() if v=='workYear']:
            subdict['workYear']= int(re.compile('\d+').findall(subdict['workYear'])[0])
        subdict['birthday']=datetime.strptime("".join(re.compile('\d{4}.\d+').findall(subdict['birthday'])).replace('年','-'),'%Y-%m')
        return  subdict


    def content(self,doc,pagevalue,pagedict):
         """
         求职意向的解析
         :param doc:
         :param pagenum:
         :return:
         """
         totaldict = {}
         for i in pagedict.keys():
             if i=='求职意向':
                 intentitem=proutil().medialpro(pagedict,pagevalue,i,doc)
                 dict={'期望工作地区':'expectedWorkplace','期望月薪':'expectedSalary','目前状况':'expectedStatus','期望工作性质':'expectedWorkNature','期望从事职业':'expectedOccupation','期望从事行业':'expectedIndustry'}
                 for i in intentitem[1:]:
                     for k,v in dict.items():
                         if i[0].split('：')[0].strip(' ')==k:
                             if len(i[0].split('：'))==2:
                                 totaldict[v]=i[0].split('：')[1].strip(' ')
             elif i=='自我评价':
                 evaluationitem=proutil().medialpro(pagedict,pagevalue,i,doc)
                 strev=''
                 for ev in evaluationitem[1:]:
                     strev+="".join(ev)
                 totaldict['selfEvaluation']=strev
                 continue
             elif i=='工作经历':
                 worktext = proutil().medialpro(pagedict, pagevalue, i, doc)
                 if isinstance(worktext,list):
                     worktext= proutil().an_medialpro(pagedict, pagevalue, i, doc).strip(' ').split('\n')
                 else:
                     worktext=(proutil().medialpro(pagedict,pagevalue,i,doc)).strip(' ').split('\n')
                 start=worktext.index([j for j in worktext if j==i][0])
                 end = worktext.index([j for j in worktext if j == pagevalue[pagevalue.index(i) + 1]][0])
                 textlist = worktext[start + 2:end]
                 totaldict['workExperience']=self.work_experience(textlist)
             elif i == '项目经历':
                 progress = proutil().medialpro(pagedict, pagevalue, i, doc)
                 if isinstance(progress, list):
                     progress = (proutil().an_medialpro(pagedict, pagevalue, i, doc)).strip(' ').split('\n')
                 else:
                     progress = (proutil().medialpro(pagedict, pagevalue, i, doc)).strip(' ').split('\n')
                 start = progress.index([j for j in progress if j == i][0])
                 end = progress.index([j for j in progress if j == pagevalue[pagevalue.index(i) + 1]][0])
                 textlist = progress[start + 2:end]
                 totaldict['projectExperience'] = self.progress_experience(textlist)
             elif i=='教育经历':
                 edu = proutil().medialpro(pagedict, pagevalue, i, doc)
                 totaldict['educationExperience']=self.edu_prase(edu,pagevalue,i)
             elif i=='证书':
                 cer=proutil().medialpro(pagedict, pagevalue, i, doc)
                 if cer :
                    totaldict['certificate'] = self.certifi(cer, pagevalue, i)
             elif i=='培训经历':
                 training= proutil().medialpro(pagedict,pagevalue,i,doc)
                 if isinstance(training,list):
                      training=training[1:]
                 totaldict['trainingExperience']=self.training_exprience(training,pagevalue,i)
             if i=='专业技能':
                 proficy=proutil().medialpro(pagedict, pagevalue, i, doc)
                 totaldict['skill']=self.skill(proficy,pagevalue,i)
             elif i=='语言能力':
                 language = proutil().medialpro(pagedict, pagevalue, i, doc)
                 totaldict['language'] =self.language(language,pagevalue,i)
             elif i=='兴趣爱好' or i=='个人爱好':
                 insert=proutil().medialpro(pagedict,pagevalue,i,doc)
                 insertstr=''
                 for ins in insert[1:]:
                     if len(ins) == 1:
                         insertstr += "".join(ins)
                     else:
                         s = "".join(ins)
                         insertstr += ";" + s
                 totaldict['hobby']=insertstr
         return totaldict


    #工作经历
    def work_experience(self,infolist):
           workstage=[]#工作阶段
           workdict = defaultdict(list)
           worksplit=[]
           for i in infolist:
               if re.match('\d+.\d+ -.*', i, flags=0):
                   if infolist.index(i) not in workstage:
                       workstage.append(infolist.index(i))
                   else:  # 重复的值index()之后的结果是一样的 ，因此下标可能出现重复的值
                       index = [x for x in range(len(infolist)) if infolist[x] == i]
                       for idx in index:
                           if idx not in workstage:
                               workstage.append(idx)
                  #对得到的每个工作阶段进行分片
           if len(workstage)==1:
               worksplit.append([i for i in infolist])
           else:
               for st in range(0,len(workstage)-1):
                       worksplit.append(infolist[workstage[st]:workstage[st+1]])
               worksplit.append(infolist[workstage[-1]:])
           for line in worksplit:
               temp = {}
               if '-'  in line[0]:
                   temp['workStartTime'] = datetime.strptime(line[0].split('-')[0].strip(' ').replace('.', '-'), '%Y-%m')
                   if '至今' in line[0]:
                       temp['workEndTime'] = ''
                   else:
                       temp['workEndTime'] = datetime.strptime("".join(re.compile('\d{4}.\d{2}').findall(line[0].split('-')[1])).replace('.', '-'), '%Y-%m')
               else:
                   temp['workStartTime'] = datetime.strptime(line[1].split('-')[0].strip(' ').replace('.', '-'),'%Y-%m')
                   if '至今' in line[1]:
                       temp['workEndTime'] = ''
                   else:
                       temp['workEndTime'] = datetime.strptime("".join(re.compile('\d{4}.\d{2}').findall(line[1].split('-')[1])).replace('.', '-'), '%Y-%m')
               try:
                    workbasic = [line.index(i) for i in line if '工作描述' in i][0]
               except:
                   continue
               for x in line[1:workbasic - 1]:
                   if '(' in x:

                       wolist=[i for i in x.split('(') if i!='']
                       if len(wolist)>1:
                            comname=[i for i in x.split(' ') if i!='']
                            temp['workCompany'] = comname[0]
                       else:
                            temp['workTimePeriod'] = re.sub('[\) ]','',"".join(wolist))

                   if len(x.split('|'))>1:
                       uplist=[ i for  i in x.split('|') if i !='' ]
                       if len(uplist)>1:
                           temp['workPosition']=x.split('|')[0].strip(' ')
                           temp['workSalary']=x.split('|')[1].strip(' ')
               loindex = []
               for li in line[workbasic:]:
                   if 'ID' in li:
                       loindex.append(line.index(li))
               if loindex:
                   stindex = min(loindex)
                   temp['workDescription'] = "".join(line[workbasic:stindex]).replace('工作描述：', '')
               else:
                   temp['workDescription'] = "".join(line[workbasic:-1]).replace('工作描述：', '')
               if '元' in  line[workbasic-1]:
                   workdict['workExperience'].append(temp)
                   continue
               else:
                    locwork = line[workbasic-1].split('|')

               if len(locwork) == 1:
                   temp['workCompanyIndustry'] = "".join(locwork).strip(' ')
               elif len(locwork) == 2:
                   temp['workCompanyIndustry'] = locwork[0].strip(' ')
                   temp['workCompanyNature'] = locwork[1].strip(' ').split('：')[1]
               else:
                   try:
                       temp['workCompanyIndustry'] = locwork[0].strip(' ')
                       temp['workCompanyNature'] = locwork[1].strip(' ').split('：')[1]
                       temp['workCompanyScale'] = locwork[2].strip(' ').split('：')[1]
                   except:
                       temp['workCompanyIndustry']='/'.join(locwork)
               workdict['workExperience'].append(temp)
           return workdict['workExperience']

    def progress_experience(self,prolist):
        projectdict = defaultdict(list)
        prosplit = self.listsplit(prolist)
        for pro in range(0, len(prosplit)):
            if pro <= len(prosplit) - 2:
                newinfo = prolist[prosplit[pro]:prosplit[pro + 1]]
            else:
                newinfo = prolist[prosplit[pro - 1]:]
            if newinfo:
                temp = {}
                for line in newinfo:
                    strline = "".join(line)
                    protitle = "".join(re.compile('\d{4}.\d{2} - (.*)').findall(strline))
                    if protitle:
                        protime = "".join(re.compile('\d{4}.\d{2} - \d{4}.\d{2}').findall(strline))
                        if protime:
                            temp['projectStartTime'] = datetime.strptime(protime.split('-')[0].strip(' ').replace('.', '-'),"%Y-%m")
                            temp['projectEndTime'] = datetime.strptime(protime.split('-')[1].strip(' ').replace('.', '-'),'%Y-%m')
                            temp['projectName'] = "".join(re.compile('.*\d(.*)').findall(strline)).strip(' ')
                        else:
                            protime = "".join(re.compile('\d{4}.\d{2} - 至今').findall(strline))
                            temp['projectStartTime'] = datetime.strptime(protime.split('-')[0].strip(' ').replace('.', '-'),"%Y-%m")
                            temp['projectEndTime'] = ''
                            temp['projectName'] = "".join(re.compile('至今(.*)').findall(strline)).strip(' ')
                    else:
                        dict = {'项目描述': 'projectDescription','责任描述': 'projectDuty', '软件环境': 'projectSoftwareEnv',
                                '硬件环境': 'projecctHardwareEnv', '开发工具': 'projectTool'}
                        for k, v in dict.items():
                            if k in line :
                                temp[v] = line.replace(k+'：','')
                projectdict['project'].append(temp)
        return projectdict['project']

    #教育经历
    def edu_prase(self,edu,pagevalue,i):
        edudict = defaultdict(list)
        if isinstance(edu, list):
           edulist=edu[1:]
        else:
            frontext = edu.split(i)[-1]
            behind = frontext.split(pagevalue[pagevalue.index(i) + 1])[0]
            textlist = re.compile('\d{4}.\d{2} - .*').findall(behind)
            edulist = []
            for tx in textlist:
                txsplit = [i for i in tx.split(' ') if i != '']
                edulist.append(txsplit)
        for line in edulist:
            temp = {}
            temp['educationStartTime'] = datetime.strptime(line[0].replace('.', '-'), '%Y-%m')
            if '至今' in line[2]:
                temp['educationEndTime'] = ''
            else:
                temp['educationEndTime'] = datetime.strptime(line[2].replace('.', '-'), '%Y-%m')
            temp['educationDegree'] = line[-1]
            temp['educationSchool'] = line[3]
            temp['educationMajor'] = line[-2]
            edudict['education'].append(temp)
        return edudict['education']
    #培训经历
    def training_exprience(self,trainlist,pagevalue,i):
        trastage = []
        sradict = defaultdict(list)
        trasplit = []
        if isinstance(trainlist,list):
            for i in trainlist:
                if re.match('\d+.\d+', "".join(i), flags=0):
                    if trainlist.index(i) not in trastage:
                        trastage.append(trainlist.index(i))
                    else:  # 重复的值index()之后的结果是一样的 ，因此下标可能出现重复的值
                        index = [x for x in range(len(trainlist)) if trainlist[x] == i]
                        for idx in index:
                            if idx not in trastage:
                                trastage.append(idx)
            if len(trastage) > 1:
                for st in range(0, len(trastage) - 1):
                    trasplit.append(trainlist[trastage[st]:trastage[st + 1]])
                trasplit.append(trainlist[trastage[-1]:])
            else:
                temp={}
                norepeat=[]
                for j in trainlist[0]:
                    if j not in norepeat:
                            norepeat.append(j)
                temp['trainingStartTime']=datetime.strptime(norepeat[0].replace('.','-'),'%Y-%m')
                if '至今' in norepeat[2]:
                    temp['trainingEndTime']=''
                else:
                     temp['trainingEndTime']=datetime.strptime(norepeat[2].replace('.','-'),'%Y-%m')
                temp['trainingCourse']=norepeat[-1]
                for x in trainlist[1:]:
                    strx="".join(x)
                    if '培训机构' in strx:
                        temp['trainingOrg']="".join(x).split('：')[1]
                    if '培训地点' in strx:
                        temp['traininigPlace']="".join(x).split('：')[1]
                    if '所获证书' in strx:
                        temp['trainingCertificate']="".join(x).split('：')[1]
                    if '培训描述' in strx:
                        temp['trainingDescription']="".join(x).split('：')[1]
                sradict['trainingExperience'].append(temp)
        else:#返回的结果为字符串
               forntext=trainlist.split(i)[-1]
               if pagevalue[pagevalue.index(i)+1]=='证书':
                   behind="".join(re.compile('(.*)证书').findall(re.sub('[\n]',';',forntext))).split(';')
               else:
                   behind=forntext.split(pagevalue[pagevalue.index(i)+1])[0].split('\n')
               trainlist=self.listsplit(behind)
               for tra in range(0, len(trainlist)):
                   temp = {}
                   if tra <= len(trainlist) - 2:
                       newinfo = behind[trainlist[tra]:trainlist[tra + 1]]
                   else:
                       newinfo = behind[trainlist[tra - 1]:]
                   for be in newinfo:
                       if '-' in be:
                           timematch="".join(re.compile('\d{4}.\d{2} - \d{4}\d{2}').findall(be))
                           if timematch:
                               temp['trainingStartTime']=datetime.strptime(timematch.split('-')[0].strip(' ').replace('.','-'),'%Y-%m')
                               temp['trainingEndTime']=datetime.strptime(timematch.split('-')[1].strip(' ').replace('.','-'),'%Y-%m')
                           else:
                               temp['trainingCourse']=be.split(' ')[-1].strip(' ')
                       if '培训机构' in be:
                               temp['trainingOrg']=be.split('：')[1].strip(' ')
                       if '培训地点' in be:
                               temp['traininigPlace']=be.split('：')[1].strip(' ')
                       if '所获证书' in be:
                               temp['trainingCertificate']=be.split('：')[1].strip(' ')
                       if '培训描述' in be:
                               temp['trainingDescription']="".join(newinfo[newinfo.index(be):-1]).replace('培训描述：','')
                   sradict['trainingExperience'].append(temp)
        return sradict['trainingExperience']
    def certifi(self,cerlist, pagevalue, i):
        certidict=defaultdict(list)
        if isinstance(cerlist,list):
            if cerlist[0][0]=="证书":
                table=cerlist[1:]
            else:
                useindex=[cerlist.index(i) for i in cerlist if i[0]=='证书']
                table=cerlist[useindex[0]+1:]
            for i in table:
                    temp={}
                    temp['time']=datetime.strptime(i[0].replace('.','-'),'%Y-%m')
                    temp['name']=i[-1]
                    certidict['certificate'].append(temp)
        else:
            frontext=cerlist.split('证书')[-1]
            behind=frontext.split(pagevalue[pagevalue.index(i)+1])[0]
            for be in behind.split('\n'):
                splbe=[i for i in be.split(' ') if i!='']
                if len(splbe)>1:
                    temp={}
                    temp['time']=datetime.strptime(splbe[0].replace('.','-'),'%Y-%m')
                    temp['name']=splbe[1]
                    certidict['certificate'].append(temp)
        return certidict['certificate']

    def skill(self,proficy,pagevalue,i):
        srt = defaultdict(list)
        strpc=''
        for pc in proficy[1:]:
            strpc+="\n".join(pc)
        if isinstance(proficy, list):
            for pr in proficy[1:]:
                temp={}
                strspl="".join(pr).split('：')
                if len(strspl)==2:
                    temp['name']=strspl[0]
                    temp['skillMastery']=strspl[1]
                    srt['skill'].append(temp)
                else:
                    srt['skill']=strpc
                    break
        else:
            fronttext = [i for i in proficy.split('专业技能') if i != ''][-1]
            behind="".join(fronttext.split(proficy[proficy.index(fronttext)+1])).split('\n')
            for be in behind:
                bespl=be.split('：')
                if len(bespl)>1:
                    temp={}
                    temp['name']=bespl[0]
                    temp['skillMastery']=bespl[1]
                    srt['skill'].append(temp)
        return srt['skill']
    def language(self,language,pagevalue,i):
        laudict = defaultdict(list)
        lanlist=[]
        if isinstance(language,list):
            lanlist=language[1:]
        else:
            fronttext=language.split(i)[-1]
            txlist=fronttext.split(pagevalue[pagevalue.index(i)+1])[0].split(' ')
            lanlist.append(txlist)

        for la in lanlist:
            temp = {}
            temp['languageKind'] = la[0].strip('：\n')
            temp['readingWritingLevel'] = "".join(
                re.compile('读写能力(.*)').findall("".join([x for x in la if '读写' in x])))
            temp['listeningSpeakingLevel'] = "".join(
                re.compile('听说能力(.*)').findall("".join([x for x in la if '听说' in x])))
            laudict['language'].append(temp)
        return laudict['language']

    def listsplit(self, datalist):
        listpro = []
        for tra in datalist:
            if "".join(re.compile('\d{4}.\d{2} - 至今').findall("".join(tra))):
                listpro.append(datalist.index(tra))
            elif "".join(re.compile('\d{4}.\d{2} - \d{4}.\d{2}').findall("".join(tra))):
                listpro.append(datalist.index(tra))
        return listpro