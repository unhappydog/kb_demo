from utils.MongoMapTags import query, delete, update, DataMap
from data_access.base.BaseMongoController import BaseMongoController
from services.tool_services.MongoService import mgService as mgservice
import settings


@DataMap(_schema=settings.mysql_db, _table="jd_company")
class JDCompanyController4Mongo(BaseMongoController):

    def get_data_by_name(self, name):
        return mgservice.query({"$or": [{"companyName": name}, {"entName": name}]}, self._schema, self._table)

    def get_data_by_job_title(self, job_title, page, limit):
        return mgservice.query_sort(query_cond={'jobTitle': job_title}, table=self._table,
                                    db=self._schema, sort_by='startDate', page=page, size=limit)
