from core.processors.baidu_processor import baiduProcessor
from core.base.BaseTask import BaseTask
import pandas as pd
import re

@baiduProcessor.add_as_processors(order=1, stage=1)
class PreProcessor(BaseTask):
    def __init__(self):
        pass

    def fit(self, data):
        data = data.apply(lambda x: self.map(x), axis=1)
        return data

    def map(self, x):
        new_x = {}
        new_x['_id'] = x['_id']
        new_x['companyName'] = x['fullname']
        new_x['entName'] = x['fullname']
        new_x['companyType'] = x['industry']
        x_business = x['business']
        business_scope = x_business.get('business_scope','')
        business_scope = re.sub("\(.+?\)$",'',business_scope)
        new_x['companyScopeTags'] = business_scope.split('、')
        new_x['dom'] = x_business['registered_address']
        new_x['establishedDate'] = x_business['registration_time']
        new_x['regCapital'] = x_business['registered_capital']
        members = x_business.get('personnel', [])
        new_members = [
            {'memberJob':member['job'],
             'memberPhoto':'',
             'memberDes':'',
             'teamMember':member['name']} for member in members
        ]
        new_x['members'] = new_members
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


