from  core.cvprase.cvword.contentPrase import ContentParse
import os
from core.cvprase.Util.util import util
class cvword(object):
    def mainwordprase(self,root,path):
            table,para,name=util().get_doc(root+'/'+path)
            basicdict = ContentParse().basic_info(table, para, name)
            totaldict = basicdict
            iss = [i.text.strip(' ') for i in para if i.text.strip(' ') == '自我评价']
            if iss:
                title = [pa.text.strip(' ') for pa in para[4:]]
            else:
                title = [pa.text.strip(' ') for pa in para[2:]]
            startindex = 0
            endindex = 0
            workindex = 0
            for ti in title:
                if ti.strip(' ') == '工作经历':
                    workindex = title.index(ti)
                if ti.strip(' ') == '项目经历':
                    startindex = title.index(ti)
                if ti.strip(' ') == '教育经历':
                    endindex = title.index(ti)
            worktable = []
            if startindex != 0:
                newtitle = title[:startindex + 1] + title[endindex:]
                for nw, j in zip(newtitle[workindex:startindex], table[3:]):
                    worktable.append(j)
            else:
                newtitle = title
                subnewtitle = newtitle[:workindex + 1] + newtitle[workindex + 2:endindex]
                for nw, j in zip(subnewtitle, table[3:-1]):
                    worktable.append(j)
                newtitle = newtitle[:workindex + 1] + newtitle[workindex + 2:]

            totaldict['workExperience'] = ContentParse().work(util().tabletxtb(worktable))
            for nw, j in zip(newtitle, table[3:]):

                if nw == '项目经历':
                    totaldict['projectExperience'] = ContentParse().project(util().tabletxtb(j))
                if nw == '教育经历':
                    totaldict['educationExperience'] = ContentParse().eduction(util().tabletxt(j))
                if nw == '培训经历':
                    totaldict['trainingExperience'] = ContentParse().training(util().tabletxtb(j))
                if nw == '语言能力':
                    totaldict['language'] = ContentParse().language(util().tabletxt(j))
                if nw == '专业技能':
                    totaldict['skill'] = ContentParse().skill(util().tabletxt(j))
                if '证书' in nw:
                    if util().tabletxt(j)[0] != '':
                        totaldict['certificate'] = ContentParse().certifi(util().tabletxt(j))
                if '在校实践经历' == nw:
                    totaldict['associationExperience'] = ContentParse().asscciation(util().tabletxtb((j)))
                if '在校学习情况' == nw:
                    totaldict['award'] = ContentParse().award(util().tabletxtb(j))
                if nw == '兴趣爱好':
                    totaldict['hobby'] = ContentParse().job(util().tabletxt(j))


            return totaldict







if __name__=='__main__':

    cvword().mainwordprase()








