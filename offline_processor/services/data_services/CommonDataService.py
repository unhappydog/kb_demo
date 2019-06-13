from utils.Tags import Singleton
from services.tool_services.mysql_service import mysqlService


@Singleton
class CommonDataService:
    def get_company_ai_top_50(self):
        companys = mysqlService.execute("select * from kb_ai_company_top_50")
        return [company['name'] for company in companys]

commonDataService = CommonDataService()
