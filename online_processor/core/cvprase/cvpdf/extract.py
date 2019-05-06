from core.cvprase.cvpdf.private_info import indivial
from core.cvprase.Util.proutil import  proutil
import fitz
import os
class cvprase(object):
    def __init__(self):
        self.resumedict={}
        
    def prase(self,root,path):
            doc=fitz.open(root+"/"+path)
            title=proutil().titlextract(doc)
            pagedict=self.get_page(doc,title)
            basicdict=indivial().basic_info(doc,pagedict)
            intentdict=indivial().content(doc,title,pagedict)
            self.resumedict=proutil().integration(basicdict,intentdict)
            return self.resumedict


    def get_page(self,doc,title):
        end=len(doc)
        dict = {}
        for k in range(0,end,1):
            page=doc.loadPage(k)
            display=page.getDisplayList()
            get_page=display.getTextPage()
            for word in title:
                rlist=get_page.search(word)
                if rlist:
                    dict[word]=k
                else:
                    continue

        return dict
# if __name__=='__main__':
#     cvprase().prase('E:/cv','')



