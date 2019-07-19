from core.processors.baidu_processor import baiduProcessor
from core.base.BaseTask import BaseTask
from core.linker.Searcher import Searcher
import pandas as pd
import re

@baiduProcessor.add_as_processors(order=1, stage=1)
class PreProcessor(BaseTask):
    def __init__(self):
        self.searcher = Searcher.instance()
        pass

    def fit(self, data):
        data = data.apply(lambda x: self.map(x), axis=1)
        data = data.drop_duplicates(subset=['companyName'], keep='first')
        data= data[data['companyName'].apply(lambda x: self.not_duplicate(x))]
        return data

    def map(self, x):
        new_x = {}
        new_x['_id'] = str(x['_id'])
        # new_x['_id'] = x['_id']

        new_x['companyName'] = x['fullname']
        new_x['entName'] = x['fullname']
        new_x['companyType'] = x['industry']
        x_business = x['business']
        business_scope = x_business.get('business_scope','')
        business_scope = re.sub("\(.+?\)$",'',business_scope)
        new_x['companyScopeTags'] = business_scope.split('、')
        new_x['dom'] = x_business.get('registered_address')
        new_x['establishedDate'] = x_business.get('registration_time')
        new_x['regCapital'] = x_business.get('registered_capital')
        ceos = x_business.get('personnel', [])
        ceos = [
             {'memberJob':member['job'],
             'memberPhoto':'',
             'memberDes':'',
             'teamMember':member['name']} for member in ceos
        ]
        new_x['ceos'] = ceos

        members = x_business.get('team',[])
        members = [
            {'memberJob':member['job'],
             'memberPhoto':'',
             'memberDes':'',
             'teamMember':member['name']} for member in members
        ]
        new_x['members'] = members
        new_x['companyStatus'] = x_business['statue']
        new_x['entType'] = x_business['type']
        new_x['companyScale'] = ""
        investments = x_business.get('investment', [])
        invests = [
            {'investDate': investment['time'],
             'investRound': '',
             'investMoney':investment['investment_captital'],
             'investorName':investment['company_name'],
             'investType':''} for investment in investments
        ]
        new_x['invests'] = invests

        return pd.Series(new_x)


    def not_duplicate(self, company_name):
        company_info = self.searcher.search_company(company_name)
        if company_info:
            return False
        else:
            return True


