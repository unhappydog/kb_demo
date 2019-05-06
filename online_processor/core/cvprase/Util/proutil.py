from operator import itemgetter
from itertools import groupby
import fitz
import re
class proutil(object):
    def titlextract(self, doc):
        """
        抽取简历中的标签
        :param doc:
        :return:
        """
        res = []
        for page in doc:
            text = page.getText("dict")
            for i in text['blocks']:
                try:
                    for j in i['lines']:

                        if j['spans'][0]['size'] == 8.40234375:
                            if j['spans'][0]['text'] not in res:
                                if re.compile('.*\d.*|\d.*|.*\d').findall(j['spans'][0]['text']):
                                    continue
                                elif j['bbox'][0] != 90.61732482910156:
                                    continue
                                else:
                                    res.append(j['spans'][0]['text'])
                except:
                    continue
        return res

    def integration(self,dict1,dict2):
        """
        :param dict1:
        :param dict2:
        :return:合并后的dict
        """
        return {**dict1,**dict2}
    def location(self ,rl1 ,rl2):
        """
            定义两个关键词之间的坐标，以及坐标之间构成的矩阵
            （x0,y0,x1,y1）
        """
        try:
            if len(rl2)==1:
                rect=rl1[0]|rl2
            else:
                rect =rl1 |rl2[0]
        except:
            rect =rl1[0]|rl2[0]
        rect[2] =596
        rect[3] = rect[3]-15
        return rect
    def textExtract(self ,doc ,page ,rect):
        """
        抽取矩形框里面的所有文本信息
        page:加载所抽取文本所在位置的页数
        rect:两关键词之间形成的矩阵的坐标
        :return:
        """
        words =doc.loadPage(page).getTextWords()
        mywords =[w for w in words if fitz.Rect(w[:4]).intersects(rect)]
        mywords.sort(key=itemgetter(3 ,0))
        group =groupby(mywords ,key=itemgetter(3))
        return group

    def medialpro(self, pagedict, pagenum, i, doc):
        datalist = []
        kno = pagenum.index(i)
        pstart = [v for k, v in pagedict.items() if k == i][0]
        try:
            pend = [v for k, v in pagedict.items() if k == pagenum[kno + 1]][0]
            if pstart == pend:
                page = doc.loadPage(pend)
                rl1 = page.searchFor(i)
                rl2 = page.searchFor(pagenum[kno + 1])
                intentrect = proutil().location(rl1, rl2)
                text = proutil().textExtract(doc, pend, intentrect)
                for g in text:
                    datalist.append([ss[4] for ss in g[1]])
                return datalist
            else:

                page = doc.loadPage(pstart)
                text = page.getText()
                while pstart != pend:
                    pstart += 1
                    text += doc.loadPage(pstart).getText()
                return text
        except:
            # title标题字段在简历的最后一页的最后一个字段
            if pstart == len(doc) - 2:
                res = ''
                while pstart != len(doc) - 1:
                    res += doc.loadPage(pstart).getText()
                    pstart += 1
                return res
            if pstart == len(doc) - 1:
                page = doc.loadPage(pstart)
                rl1 = page.searchFor(i)
                rl2 = [fitz.Rect(36, rl1[0][1], 596, 840)]
                intentrect = proutil().location(rl1, rl2)
                text = proutil().textExtract(doc, pstart, intentrect)
                for g in text:
                    datalist.append([ss[4] for ss in g[1]])
                return datalist


    def an_medialpro(self, pagedict, pagenum, i, doc):
        pstart = [v for k, v in pagedict.items() if k == i][0]
        page = doc.loadPage(pstart)
        text = page.getText()
        text += doc.loadPage(pstart).getText()
        return text

