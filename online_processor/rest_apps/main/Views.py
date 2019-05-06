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
from werkzeug.utils import secure_filename
import os


@inf_restful.route("/online/similar_jd/<string:name>/<int:page>/<int:limit>", methods=['GET'])
def get_similar_jd(name, page, limit):
    datas = dataService.get_jd_by_name(name, page, limit)
    # datas = [{"link":linkerService.link_jd(data)} for data in datas]
    for data in datas:
        data['link'] = linkerService.link_jd(data)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/talent_bank/search/<string:by>/<string:searchWord>/<int:page>/<int:limit>/<string:mode>", methods=['GET'])
def search_talent_by_keyword(by, searchWord, page, limit, mode):
    """
    按照职位名称、教育程度 、来源、或者其它查询人才库
    :param by:
    :param searchWord:
    :param page:
    :param limit:
    :return:
    """
    if mode == "none":
        mode = None
    if by == "keyword":
        datas = tbService.search_by_name(searchWord, page, limit, mode)
    elif by == "education":
        datas = tbService.search_by_education(searchWord, page,limit, mode)
    elif by == "source":
        datas = tbService.search_by_source(searchWord, page, limit, mode)
    elif by == "none":
        datas = tbService.get_datas(page, limit, mode)
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


# @inf_restful.route("/upload")
