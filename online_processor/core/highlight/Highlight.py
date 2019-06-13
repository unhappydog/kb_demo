from core.highlight.Utils import basicinfo
from utils.Utils import int_to_hanzi
import re
class hightlight(object):
    """
    简历亮点检测：
    教育亮点，证书亮点，语言能力亮点,工作公司亮点
    """
    def __init__(self):
        self.hightlight=''
        self.cvdata=basicinfo().get_cvdata()
        self.company=basicinfo().get_company()
        # self.front, self.back, self.ai, self.database = basicinfo().get_terminology()
    def eminentPoint(self):

       for line in self.cvdata:
         totalhigh = []
         print(line['name'])
         print(line['_id'])
         eh=self.eduction_highlight(line)
         lh=self.language_highlight(line)
         ch=self.certificate_highlight(line)
         ci=self.company_highlight(line,self.company)
         if not isinstance(eh,bool):
             totalhigh.extend(eh)
         if not isinstance(lh,bool):
             totalhigh.extend(lh)
         if not isinstance(ch,bool):
             totalhigh.extend(ch)
         if not isinstance(ci,bool):
             totalhigh.extend(ci)
         if totalhigh:
             print(totalhigh)
    #教育亮点(211,985院校)
    def eduction_highlight(self,singledata):
            academy = basicinfo().get_academy()
            educationdata=singledata['educationExperience']
            edulist = []
            for edu in educationdata:
                school=[ school for school in academy if edu['educationSchool']==school['schoolName']]
                if school:
                    for sc in school[0]['tags']:
                        if sc == '':
                            continue
                        else:
                            if len(school[0]['tags']) > 2:
                                temp = {}
                                temp['label'] = '教育亮点'
                                temp['highlight'] = '候选人有突出的教育背景，毕业于国内985、211、双一流的知名院校' + edu['educationSchool']
                                temp['level'] = 0
                                edulist.append(temp)
                            elif '985' in sc:
                                temp = {}
                                temp['label'] = '教育亮点'
                                temp['highlight'] = '候选人有优秀的教育背景，毕业于国内985、211的知名院校' + edu['educationSchool']
                                temp['level'] = 1
                                edulist.append(temp)
                            elif '211' in sc and len(school[0]['tags']) == 2:
                                temp = {}
                                temp['label'] = '教育亮点'
                                temp['highlight'] = '候选人有亮眼的教育背景，来自于国内211、双一流院校' + edu['educationSchool']
                                temp['level'] = 2
                                edulist.append(temp)
                            elif '211' in sc:
                                temp = {}
                                temp['label'] = '教育亮点'
                                temp['highlight'] = '候选人有良好的教育经历，来自于国内211院校' + edu['educationSchool']
                                temp['level'] = 3
                                edulist.append(temp)
            if edulist:
                if len(edulist)>1:
                    level=[]
                    elist=[]
                    tmp=[]
                    for el in edulist:
                        level.append(el['level'])
                        el.pop('level')
                        elist.append(el)
                    index=level.index(min(level))
                    tmp.append(elist[index])
                    res=tmp
                else:
                       edulist[0].pop('level')
                       res =edulist
                return res
            else:
                return  False
    #证书亮点
    def certificate_highlight(self,singledata):
          certifi=[]
          certificate=singledata['certificate']
          if certificate:
              if len(certificate)==1:
                  temp={}
                  temp['label']='证书'
                  temp['highlight']='候选人持有'+certificate[0]['name']+'证书'
                  certifi.append(temp)
              else:
                  stopword=['优秀毕业生','运动会','毕业证书','学位证','毕业证','奖学金','优秀学生干部','优秀员工','校级优秀个人','优秀学生',
                            '校友先进十佳','国家励志奖学金','社会活动奖','助学金','三好学生']
                  effective=[]
                  patent=[]
                  for cer in certificate:
                      filterword=[st for st in stopword if st in cer['name']]

                      if filterword:
                          continue
                      elif '专利' in cer['name'] or '发表' in cer['name']:
                          patent.append(cer['name'])

                      else:
                          if  "".join(re.findall('证书.*号',cer['name'])) in cer['name']:
                              matchword="".join(re.findall('证书.*号',cer['name']))
                              if matchword:
                                  effective.append(cer['name'].split(matchword)[0])

                          effective.append(cer['name'])
                  if effective:
                      temp={}
                      temp['label']='证书'
                      temp['highlight']='候选人持有'+re.sub(' ','',"、".join(effective))+'证书，能力较强'
                      certifi.append(temp)
                  if patent:
                      temp={}
                      temp['label']='发表著作'
                      temp['highlight']='候选人发表了'+"、".join(patent)+'有一定的科研能力'
                      certifi.append(temp)
              return certifi
          else:
              return False
    #语言能力亮点
    def language_highlight(self,singledata):
        lau=[]
        language=singledata['language']
        if language:
            if len(language)>1:
                langu=[lan['languageKind'] for lan in language]
                temp={}
                temp['label']='语言能力'
                temp['highlight']='候选人具有较强的语言学习能力可同时使用'+"、".join(langu)+'这'+int_to_hanzi(len(langu))+'种语言'
                lau.append(temp)
            else:
                if language[0]['listeningSpeakingLevel']=='熟练' and language[0]['readingWritingLevel']=='熟练':
                    temp={}
                    temp['label']='语言能力'
                    temp['highlight']='候选人'+language[0]['languageKind']+'优秀，可以流利的听说读写'
                    lau.append(temp)
            if lau:
                return lau
            else:
                return False
        else:
            return False
    #工作公司亮点（名企）
    def company_highlight(self,singledata,company):
        comhighlight=[]
        famouscop=[]
        companydata=singledata['workExperience']
        for com in companydata:
              for i in company:
                  try:
                      if i['label']=='名企' and com['workCompany'] in i['companyName']:
                            if com['workCompany'] not in famouscop:
                                famouscop.append(com['workCompany'])
                  except:
                      continue
        if famouscop:
            if len(famouscop)==1:
                if len(famouscop[0])==2:
                    if famouscop[0]=='金融' or famouscop[0]=='讯飞':
                        return False
                else:
                    temp={}
                    temp['label']='名企'
                    temp['highlight']='候选人有'+"、".join(famouscop)+'的工作经验，是有实力的人才'
                    comhighlight.append(temp)
            elif len(famouscop)>1:
                temp = {}
                temp['label']='名企'
                temp['highlight'] = '候选人有' + "、".join(famouscop) + '的工作经验，是有实力过硬的人才'
                comhighlight.append(temp)
        if comhighlight:
            return comhighlight
        else:
            return  False



if __name__=='__main__':
    data=basicinfo().get_cvdata()
    print(data)
    hightlight().eminentPoint()