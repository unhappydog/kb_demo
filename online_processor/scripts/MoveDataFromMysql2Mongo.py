from data_access.controller.KBAcademyController import KB_AcademyController
from data_access.controller.KBAcademyController4Mongo import KBAcademyController4Mongo
from data_access.controller.KBCompanyController import KBCompanyController
from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo
from data_access.controller.KBTerminologyController import KBTerminologyController
import datetime
# from services.MongoService import mgservice
from services.tool_services.mysql_service import mysqlService
from services.tool_services.MongoService import mgService as mgservice
import re


def syn_academy():
    kb_mysql = KB_AcademyController()
    kb_mongo = KBAcademyController4Mongo()

    id_dict = {1: "中国校友网(2019)", 2: "中国校友网(2018)"}
    url_dict = {1: "http://www.cuaa.net", 2: "http://www.cuaa.net"}
    datas = mysqlService.execute("select * from kb_academy_rank")
    rank_map = {
        data['academyId']: data['rank'] for data in datas
    }
    source_map = {
        data['academyId']: id_dict[int(data['toplistId'])] for data in datas
    }
    url_map = {
        data['academyId']: url_dict[int(data['toplistId'])] for data in datas
    }
    datas = kb_mysql.get_datas()

    for data in datas:
        print(data.__dict__)
        al_data = kb_mongo.get_data_by_name(data.schoolName)
        if al_data:
            id = al_data[0]._id
            # kb_mongo.insert_data(data)
            data.__dict__['_id'] = id
            data.__dict__['rank'] = rank_map.get(data.id)
            data.__dict__['ranksource'] = source_map.get(data.id)
            data.__dict__['rankurl'] = url_map.get(data.id)
            if data.speciality is not None:
                data.__dict__['tags'] = [tag for tag in data.speciality.split(';') if '211工程' == tag or '985工程' == tag
                                         or '双一流' == tag or re.match('^211工程（.*）$', tag) or re.match('^985工程（.*）$', tag) or
                                         tag == '世界一流大学和一流学科']
            else:
                data.__dict__['tags'] = []
            kb_mongo.update_by_id(data)

        #     kb_mongo.update_by_id(data)
        else:
            try:
                kb_mongo.insert_data(data)
            except Exception as e:
                print(e)
                # print(data['_id'])


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


def syn_terminology():
    kb_terminal_mysql = KBTerminologyController()
    kb_terminal_mongo = KBTerminologyController4Mongo()
    filed_table = mysqlService.execute("select * from kb_terminology_type")
    filed_table = {data['id']: data['type'] for data in filed_table}
    datas = kb_terminal_mysql.get_datas()
    for data in datas:
        # print(data.__dict__)
        # doc = data.__dict__
        doc = {}
        for column in ["cnName", "engName", "brief", "fieldId", "id", "name"]:
            doc[column] = data.__dict__[column]
        if doc['cnName'] is not None:
            doc['cnName'] = doc['cnName'].split(';')
        if doc['engName'] is not None:
            doc['engName'] = doc['engName'].split(';')
        if doc['name'] == "":
            print(doc)

        if doc['fieldId'] is not None:
            doc['fieldId'] = [filed_table.get(int(_id)) for _id in doc['fieldId'].split(';')]
        if mgservice.query({"id": data.id}, 'kb_demo', 'kb_terminology'):
            mgservice.delete({'id': data.id}, 'kb_demo', 'kb_terminology')
        kb_terminal_mongo.insert_data(doc)


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
        return datetime.datetime.strptime(date, '%Y-%m')
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
    syn_academy()
    # syn_company()
    # syn_terminology()
