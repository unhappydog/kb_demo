from utils.Tags import Singleton
from services.tool_services.mysql_service import mysqlService
from data_access.controller.KBPostController4Mongo import KBPostController4Mongo


@Singleton
class CommonDataService:
    def __init__(self):
        self.controller = KBPostController4Mongo()
        self.keyword_dict = self.controller.get_prefix_dict()
        self.word_to_title = {}
        for job_title, keywords in self.keyword_dict.items():
            for keyword in keywords:
                if keyword in self.word_to_title.keys():
                    self.word_to_title[keyword].append(job_title)
                else:
                    self.word_to_title[keyword] = [job_title]
        self.word_to_title['知识图谱'] = ['知识图谱工程师']

    def get_company_ai_top_50(self):
        companys = mysqlService.execute("select * from kb_ai_company_top_50")
        return [company['name'] for company in companys]

    def keyword_to_job(self, keyword):
        return self.word_to_title.get(keyword, [])


commonDataService = CommonDataService()
