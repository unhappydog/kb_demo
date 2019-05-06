import re
import docx
from core.cvprase.Util import adjunction as ad
from win32com import client as wc
import os
class util(object):

    def doc2docx(self,g):
        word = wc.Dispatch('Word.Application')
        doc = word.Documents.Open('E:/cv/' + g)  # 目标路径下的文件
        newpath = 'E:/cv/' + g.replace('doc', 'docx')
        doc.SaveAs(newpath, 16)  # 转化后路径下的文件
        doc.Close()
        word.Quit()

    """字典整合"""
    def integration(self, dict1, dict2):
        return {**dict1, **dict2}

    def listsplit(self,datalist):
        listpro = []
        for tra in datalist:
            if "".join(re.compile('\d{4}.\d{2} - 至今').findall("".join(tra))):
                listpro.append(datalist.index(tra))
            elif "".join(re.compile('\d{4}.\d{2} - \d{4}.\d{2}').findall("".join(tra))):
                listpro.append(datalist.index(tra))
        return listpro

    def get_doc(self,path):
        doc = docx.Document(path)
        document = ad.opendocx(path)
        fullText = ad.getdocumenttext(document)
        name = "".join([fu for fu in fullText if '先生' in fu or '女士' in fu]).strip('\t')
        table = doc.tables
        para = doc.paragraphs
        return table, para, name

    def tabletxt(self, table):
        c = []
        for row in table.rows:
            for cell in row.cells:
                if cell.text not in c:
                    c.append(cell.text)
        return c

    def tabletxtb(self, table):
        c = []
        try:
            for row in table.rows:
                z = []
                for cell in row.cells:
                    if cell.text not in z:
                        z.append(cell.text)
                c.append(z)
        except:
            for j in table:
                for row in j.rows:
                    z = []
                    for cell in row.cells:
                        if cell.text not in z:
                            z.append(cell.text)
                    c.append(z)

        return c