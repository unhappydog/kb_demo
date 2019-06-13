from utils.MongoMapTags import query, delete, update, DataMap
from utils.Tags import return_type
from data_access.base.BaseMongoController import BaseMongoController
from data_access.models.KB_Company import kb_Company
from services.tool_services.MongoService import mgService as mgservice
import re
import settings


def filter_data(func):
    def _wrapper(*args, **kwargs):
        datas = func(*args, **kwargs)

        return [format_capital(data) for data in datas]
    return _wrapper


def format_capital(data):
    capital = data.regCapital
    if type(capital) == str:
        reg_capital = "{:.1f}万元".format(float(capital)) if re.match('^[0-9]+\.?[0-9]*$', capital) else capital
        data.regCapital = reg_capital

    detail = data.brief
    if type(detail) == str:
        if detail.endswith('展开'):
            data.brief = detail[:-2]
    return data


@DataMap(_schema=settings.mysql_db, _table="kb_company")
class KBCompanyController4Mongo(BaseMongoController):

    @filter_data
    @return_type(kb_Company)
    def get_data_by_name(self, name):
        return mgservice.query({"$or":[{"companyName":name}, {"entName":name}]},self._schema, self._table)


if __name__ == '__main__':
    a = KBCompanyController4Mongo()
    print(a.get_data_by_name("华云智能")[0].regCapital)
