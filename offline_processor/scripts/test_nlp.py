import sys
sys.path.append(".")
from services.NLPService import nlpService
from services.tool_services.mysql_service import mysqlService

if __name__ == '__main__':
    print(mysqlService.execute("show tables"))
    a = "碧桂园机器人失灵？副总沈岗辞职800亿项目堪忧。"

    result = nlpService.ner_recong(a)
    print(result)
