# -*-coding:utf-8-*-
from core.cvgenerate.util import geUtil
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from core.cvgenerate.cvdetial import detailinfo
class generation(object):
  def __init__(self,path):
      self.path=path


  def firstflood(self,data):
      if isinstance(data,list):
          data=data[0]
      document = Document()
      document.styles['Normal'].font.name = u'宋体'
      document.styles['Normal'].font.size = Pt(9)
      document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
      fcname = geUtil().function_name(detailinfo())
      for exec in fcname:
          try:
              getattr(detailinfo(), exec)(document, data, geUtil().en_to_cn(exec))
          except:
              getattr(detailinfo(), exec)(document, data)

      document.save(self.path + data['_id'] + '.docx')


if __name__=='__main__':

    gen = generation('/tmp/pycharm_141/core/cvgenerate/file/')
    data=geUtil().getdata()[0]
    gen.firstflood(data)
