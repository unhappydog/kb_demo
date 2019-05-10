# -*- coding: utf-8 -*-
from core.cvprase.cvword.contentPrase import ContentParse
from core.cvprase.Util.util import util
import re
class cvword(object):
    def mainwordprase(self,root):
            table,para,name,fulltext=util().get_doc(root)
            basicdict = ContentParse().basic_info(table, para, name)
            totaldict = basicdict
            wodata,newlist,newtable=ContentParse().workdict(para,table)
            totaldict['workExperience'] = wodata
            word={'项目经历':'projectExperience','教育经历':'educationExperience','培训经历':'trainingExperience'}
            listcopy=newlist[:]
            for nw, j in zip(newlist,newtable):
                for k,v in word.items():
                     if k==nw:
                          try:
                            totaldict[v] = getattr(ContentParse(),v)(util().tabletxtb(j))
                          except:
                              totaldict[v] = getattr(ContentParse(),  v)(util().tabletxt(j))
                          listcopy.remove(nw)
            codict=ContentParse().combindict(fulltext,newlist)
            totaldict=util().integration(totaldict,codict)
            return totaldict






if __name__=='__main__':

    cvword().mainwordprase()








