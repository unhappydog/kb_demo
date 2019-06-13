from services.tool_services.MongoService import mgService
import datetime
import json
import difflib

name_map = {  # :代表为列表中元素的属性，.代表是属性
    'companyName': 'com_name',
    'entName': 'com_registered_name',
    'establishedDate': 'com_born_date',
    'companyScale': 'company_scale.com_scale_name',
    'contactTel': 'contact.tel',
    'frName': 'frName',
    'regCapital': 'regcap',
    'contactEmail': 'contact.email',
    'contactAddree': 'contact.addr',
    'companyLocation': 'com_local',
    'companyStage': 'com_stage_name',
    'fundStatus': '',
    ':tags': 'tag_info.normal_tag.:name',
    ':fundingTags': 'tag_info.especial_tag.:name',
    'companyScopeTags': 'com_scope.cat_name',
    'brief': 'com_des',
    'fundNeeds': 'com_fund_needs_name',
    'productImg': '',
    'productPdf': '',
    'companyLogo': 'com_logo_archive',
    'entType': 'enttype',
    'dom': 'dom',
    'insertTime': '',
    'md5': '',
    'companyType': '',
    'lastInvestDate': '',
    'lastInvestMoney': '',
    'creditCode': '',
    'businessTermFrom': '',
    'businessTermTo': '',
    'registrationAuthority': '',
    'approvalDate': '',
    'registrationstatus': '',
    'businessScope': 'com_scope.cat_name',
    'aliasName': '',
    'formerName': '',
    'englishName': '',
    'englishNameAbbre': '',
    'mainBusiness': '',
    ':members': {'person': {
        'memberJob': 'des',
        'memberPhoto': 'logo',
        'memberDes': 'per_des',
        'teamMember': 'name'
    }},
    ':products': {'products': {
        'productName': 'name',
        'productDes': 'des',
        'productLink': 'url'
    }},
    ':news': {'news': {
        'companyNewsTitle': 'title',
        'companyNewsTime': 'time',
        'companyNewsLink': 'url'
    }},
    # ':mileStones': {'mile_stones': {
    #     'mileStoneDate': 'date:year.month.day',
    #     'mileStone': 'des'
    # }},
    # 'invests': {'industry.list': {
    #     'investDate': '',
    #     'investRound': '',
    #     'investMoney': '',
    #     'investorName': '',
    #     'investorType': ''
    # }},
    'outbounds': ''
}


def syn_company():
    companys = mgService.query_as_gen({}, 'kb_demo', 'company_source_Itjuzi')
    for company in companys:
        data = parse_company(company)
        if mgService.query({"companyName": data['companyName']}, 'kb_demo', 'kb_company'):
            if '_id' in data:
                del data['_id']
            if data.get('regcap', None):
                data['regcap'] = "{:.1f}".format(float(data['regcap']))
            mgService.update({'companyName': data['companyName']}, data, 'kb_demo', 'kb_company')
        else:
            mgService.insert(data, 'kb_demo', 'kb_company')


def syn_company_from_xin():
    # mgService.delete({"c"})
    companys = mgService.query_as_gen({}, 'kb_demo', 'kb_xin_company2')
    for data in companys:
        temp_name = data['companyName']
        if string_similar(data['entName'], data['companyName']) < 0.3:
            data['companyName'] = data['entName']
        if mgService.query({"companyName": temp_name}, 'kb_demo', 'kb_company'):
            del data['_id']
            mgService.update({'companyName': temp_name}, data, 'kb_demo', 'kb_company')
        elif data.get('_id') and mgService.query({"_id": data['_id']}, 'kb_demo', 'kb_company'):
            _id = data['_id']
            del data['_id']
            mgService.update({'_id': _id}, data, 'kb_demo', 'kb_company')
        else:
            mgService.insert(data, 'kb_demo', 'kb_company')


def parse_company(data):
    temp = {}
    for target_name, origin_name in name_map.items():
        if target_name.startswith(':'):
            temp[target_name[1:]] = []
            target = temp[target_name[1:]]
            target_name = target_name[1:]
        else:
            temp[target_name] = ""
            target = temp[target_name]
            target_name = target_name
        if type(origin_name) == str:
            if origin_name == "":
                continue
            else:
                if type(target) == str:
                    origin_sub_names = origin_name.split('.')
                    result = ""
                    if origin_sub_names[0].startswith(':'):
                        if data.get(origin_sub_names[0][1:], []):
                            print(origin_sub_names)
                            print(data[origin_sub_names[0][1:]])
                            temp_item = data[origin_sub_names[0][1:]][0]
                        else:
                            continue
                    else:
                        if data.get(origin_sub_names[0]):
                            temp_item = data[origin_sub_names[0]]
                        else:
                            continue
                    for index in range(1, len(origin_sub_names)):
                        if index == len(origin_sub_names) - 1:
                            result = temp_item[origin_sub_names[index]]
                            temp_item = result
                        elif origin_sub_names[index].startswith(':'):
                            temp_item = temp_item[origin_sub_names[index][1:]][0]
                        else:
                            temp_item = temp_item[origin_sub_names[index]]

                    temp[target_name] = temp_item
                elif type(target) == list:
                    origin_sub_names = origin_name.split('.')
                    result = []
                    if origin_sub_names[0].startswith(':'):
                        temp_item = data[origin_sub_names[0][1:]]
                    else:
                        temp_item = data[origin_sub_names[0]]
                    for index in range(1, len(origin_sub_names)):
                        if index == len(origin_sub_names) - 1:
                            # result.append(temp_item[origin_sub_names[index]])
                            if origin_sub_names[index].startswith(':'):
                                if type(temp_item) == list:
                                    for sub_temp_item in temp_item:
                                        result.append(sub_temp_item[origin_sub_names[index][1:]])
                                else:
                                    result.append(temp_item[origin_sub_names[index][1:]])
                            else:
                                if type(temp_item) == list:
                                    for sub_temp_item in temp_item:
                                        result.append(sub_temp_item[origin_sub_names[index]])
                                else:
                                    result.append(temp_item[origin_sub_names[index]])
                            temp_item = result
                        elif origin_sub_names[index].startswith(':'):
                            temp_item = temp_item[origin_sub_names[index][1:]][0]
                        else:
                            temp_item = temp_item[origin_sub_names[index]]
                    temp[target_name] = temp_item
        elif type(origin_name) == dict:
            origin_main_name = list(origin_name.keys())[0]
            result = []
            for item in data[origin_main_name]:
                temp_item = {}
                for k, v in origin_name[origin_main_name].items():
                    temp_item[k] = item[v]
                result.append(temp_item)
            if type(target) == list:
                temp[target_name] = result
    temp['mileStones'] = parse_mile_stone(data)
    temp['invests'] = parse_invests(data)
    return temp


def parse_mile_stone(data):
    origin_mile_stones = data.get('mile_stones')
    if not origin_mile_stones:
        return []
    result = []
    for origin_mile_stone in origin_mile_stones:
        year = int(origin_mile_stone['year'])
        month = int(origin_mile_stone['month'])
        day = int(origin_mile_stone['day'])
        temp_dict = {}

        if month < 1 or month > 12:
            month = 1
        if year > 2020:
            year = 2019
        if day < 1 or day > 31:
            day = 1
        temp_dict['mileStoneDate'] = datetime.datetime(year, month, day)
        temp_dict['mileStone'] = origin_mile_stone['des']
        result.append(temp_dict)
    return result


def parse_invests(data):
    origin_invest = data['industry']
    # number_json = json.loads(origin_invest['number'], encoding='utf8')
    # times = number_json['time']
    # amount = number_json['financing_amount']
    invest_list = origin_invest['list']
    result = []
    for invest in invest_list:
        temp = {}
        temp['investorName'] = invest['name']
        result.append(temp)
    return result


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


if __name__ == '__main__':
    # syn_company()
    syn_company_from_xin()
