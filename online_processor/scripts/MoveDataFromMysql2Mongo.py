from data_access.controller.KBAcademyController import KB_AcademyController
from data_access.controller.KB_AcademyController4Mongo import KB_AcademyController4Mongo
from data_access.controller.KBCompanyController import KBCompanyController
import datetime
from services.MongoService import mgservice
import re


def syn_academy():
    kb_mysql = KB_AcademyController()
    kb_mongo = KB_AcademyController4Mongo()

    datas = kb_mysql.get_datas()
    for data in datas:
        print(data.__dict__)
        kb_mongo.insert_data(data)


def syn_company():
    kb_company_mysql = KBCompanyController()
    datas = kb_company_mysql.get_datas()
    for data in datas:
        doc = data.__dict__
        doc["tags"] = extract_tags(doc, "tags")
        doc["fundingTags"] = extract_tags(doc, 'fundingTags')

        doc['companyScopeTags'] = extract_tags(doc, 'companyScopeTags', split_dot=';')
        doc['members'] = exetract_info(doc, ['memberJob', 'memberPhoto', 'memberDes', 'teamMember'])
        doc['products'] = exetract_info(doc, ['productName', 'productDes', 'productLink'])
        doc['news'] = exetract_info(doc, ['companyNewsTitle', 'companyNewsTime', 'companyNewsLink'])
        doc['mileStones'] = exetract_info(doc, ['mileStoneDate', 'mileStone'])
        doc['invests'] = exetract_info(doc,
                                       ['investDate', 'investRound', 'investMoney', 'investorName', 'investorType'])
        doc['outbounds'] = exetract_info(doc, ['outboundName', 'outboundDate', 'outboundRound',
                                               'outboundMoney', 'outboundInvestor', 'outboundInvestorType'])

        format_date_data(doc)
        print(doc)
        mgservice.insert(doc, 'kb_demo', 'kb_company')


def exetract_info(doc, col_names):
    temp_list = []
    result = []
    for col_name in col_names:
        temp_list.append(doc[col_name].split("|"))
        del doc[col_name]
    infos = zip(*temp_list)
    for k_v in infos:
        temp = {}
        for i in range(0, len(col_names)):
            if k_v[i] == "":
                continue
            temp[col_names[i]] = k_v[i]
        if temp == {}:
            continue
        result.append(temp)
    return result


def extract_tags(doc, col_name, split_dot="|"):
    tags = doc[col_name].split(split_dot)
    return [tag for tag in tags if tag != "" and tag is not None]


def date_format(date):
    if re.match('^[0-9]{4}-[0-9]{1,2}$', date):
        # return "new Date(\"{0}\")".format(date)
        return datetime.datetime.strptime(date,'%Y-%m')
    elif re.match('^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$', date):
        # return "new Date(\"{0}\")".format(date)
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    elif re.match('^[0-9]{4},[0-9]{1,2}$', date):
        # return "new Date(\"{0}\")".format(date.replace(",", "-"))
        return datetime.datetime.strptime(date, '%Y,%m')
    elif re.match('^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}$', date):
        # return "new Date(\"{0}\")".format(date)
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def format_date_data(doc, end_str='Date'):
    for k, v in doc.items():
        if type(v) == list:
            for sub_item in v:
                if type(sub_item) == str:
                    continue
                for sub_k, sub_v in sub_item.items():
                    if sub_k.endswith(end_str):
                        sub_item[sub_k] = date_format(sub_v)
        if k.endswith(end_str):
            doc[k] = date_format(v)


def extract_mem_info(doc):
    names = doc["teamMember"].split("|")
    del doc["teamMember"]
    deses = doc["memberDes"].split("|")
    del doc["memberDes"]
    photos = doc["memberPhoto"].split("|")
    del doc["memberPhoto"]
    jobs = doc["memberJob"].split("|")
    del doc["memberJob"]
    infos = zip(names, deses, photos, jobs)
    result = []
    for name, des, photo, job in infos:
        result.append({
            'memberName': name,
            'memberDes': des,
            'memberPhoto': photo,
            'memberJob': job
        })
    return result


if __name__ == '__main__':
    # syn_academy()
    syn_company()
