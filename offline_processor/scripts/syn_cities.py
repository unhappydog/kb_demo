import sys
sys.path.append(".")
from services.tool_services.mysql_service import mysqlService
from services.tool_services.MongoService import mgService

def syn_cites():
    sql = "select city, province from analysis_cities ,analysis_provinces where analysis_cities.provinceid = analysis_provinces.provinceid "

    datas = mysqlService.execute('use ai_intelligence',sql)
    for data in datas:
        try:
            mgService.insert(data, 'kb_graph', 'kb_graph_cities')
        except Exception as e:
            print(e)

if __name__ == '__main__':
    syn_cites()
