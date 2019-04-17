from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from data_access.models.KB_Company import kb_Company
from services.tool_services.MongoService import mgService as mgservice
import settings


@DataMap(_schema=settings.mysql_db, _table="kb_company")
class KBCompanyController4Mongo(BaseMongoController):

    @return_type(kb_Company)
    def get_data_by_name(self, name):
        return mgservice.query({"$or":[{"companyName":name}, {"entName":name}]},self._schema, self._table)