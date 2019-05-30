from . import inf_restful
from flask import Flask, request, jsonify
from utils.Logger import logging
from utils.Utils import parse_data_to_dict
import json
from utils.Encoder import JSONEncoder
from services.LinkerService import linkerService
from services.DataService import dataService
from services.KgizeService import kgService
from services.CVService import cv_service
from services.TalentBankService import tbService
from werkzeug.utils import secure_filename
from settings import BASE_DIR
import datetime
import re
import os


@inf_restful.route("/online/similar_jd/<string:name>/<int:page>/<int:limit>", methods=['GET'])
def get_similar_jd(name, page, limit):
    datas = dataService.get_jd_by_name(name, page, limit)
    # datas = [{"link":linkerService.link_jd(data)} for data in datas]
    split_with_br = lambda x: re.sub('<br/>{2,}','',re.sub('[0-9]{1,2}(、|：|,|，)', '<br/>', x))
    for data in datas:
        data['Name'] = re.sub("（.*）|\(.*\)", '', data['Name'])
        # data['Salary'] = (lambda x: "-".join(["{:.0f}k".format(float(ele) / 1000) for ele in x.split('-')]) \
        #     if re.match('[0-9]{1,10}-[0-9]{1,10}', x) else "")(data['Salary'])
        data['link'] = linkerService.link_jd(data)
        data['requirement'] = split_with_br(data['requirement']).strip().strip(':').strip('【').strip('】').strip()
        data['requirement'] = data['requirement'][5:] if data['requirement'].startswith('<br/>') else data['requirement']

        data['duty'] = split_with_br(data['duty']).strip().strip(':').strip('【').strip()
        data['duty'] = data['duty'][5:] if data['duty'].startswith('<br/>') else data['duty']

    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/project_experience/<string:name>/<int:page>/<int:limit>", methods=['GET'])
def search_project_experience_by_name(name, page, limit):
    datas = dataService.get_project_experience_by_name(name, page, limit)
    datas = [{
        'projectName': data['projectName'],
        'company': data.get('company', None),
        'projectDescription': data['projectDescription'],
        'linkData': linkerService.link_terminology_in_text(data['projectDescription'])
    } for data in datas]
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/get_company_by_job_title/<string:job_title>/<int:page>/<int:limit>", methods=['GET'])
def get_company_by_job_title(job_title, page, limit):
    datas = dataService.get_company_by_jd(job_title, page, limit)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)




@inf_restful.route("/online/get_news_by_tag/<string:tag>/<int:page>/<int:size>", methods=['GET'])
def get_news_by_tags(tag, page, size):
    data = dataService.get_news_by_tag(tag, page,size)
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/get_news/<int:page>/<int:size>", methods=['GET'])
def get_news(page, size):
    data = dataService.get_news(page, size)
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/get_news_by_domain/<string:domain>/<int:page>/<int:size>", methods=['GET'])
def get_news_by_domain(domain, page, size):
    data = dataService.get_news_by_domain(domain, page, size)
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder)


