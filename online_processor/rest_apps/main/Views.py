from . import inf_restful
from flask import Flask, request, jsonify
from utils.Logger import logging
from utils.Utils import parse_data_to_dict
import json
from utils.Encoder import JSONEncoder
from services.LinkerService import linkerService
from services.DataService import dataService
from services.KgizeService import kgService
from services.TalentBankService import tbService


@inf_restful.route("/online/similar_jd/<string:name>/<int:page>/<int:limit>", methods=['GET'])
def get_similar_jd(name, page, limit):
    datas = dataService.get_jd_by_name(name, page, limit)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/talent_bank/search/<string:keyword>/<int:page>/<int:limit>", methods=['GET'])
def search_talent_by_keyword(keyword, page, limit):
    datas = tbService.search_by_name(keyword, page, limit)
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
