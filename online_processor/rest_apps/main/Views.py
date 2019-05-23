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


@inf_restful.route("/online/talent_bank/search/<string:by>/<string:searchWord>/<int:page>/<int:limit>/<string:mode>",
                   methods=['GET'])
def get_talent_by(by, searchWord, page, limit, mode):
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
        datas = tbService.search_by_education(searchWord, page, limit, mode)
    elif by == "source":
        datas = tbService.search_by_source(searchWord, page, limit, mode)
    elif by == "none" or by == 'undefined':
        datas = tbService.get_datas(page, limit, mode)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/talent_bank/search_with_name/<string:name>/<string:by>/<string:searchWord>/<int:page"
                   ">/<int:limit>/<string:mode>",
                   methods=['GET'])
def get_talent_with_name_by(name, by, searchWord, page, limit, mode):
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
        datas = tbService.search_by_name(searchWord, page, limit, mode, name)
    elif by == "education":
        datas = tbService.search_by_education(searchWord, page, limit, mode, name)
    elif by == "source":
        datas = tbService.search_by_source(searchWord, page, limit, mode, name)
    elif by == "none" or by == 'undefined':
        datas = tbService.get_datas(page, limit, mode, name)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/sourcing/search_talent_bank/<string:keyword>/<int:page>/<int:limit>")
def search_talent_by_keyword(keyword, page, limit):
    datas = tbService.search_by_keyword(keyword, page=page, size=limit)
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


@inf_restful.route("/online/upload/<string:source>", methods=['POST'])
def upload(source):
    if request.method == 'POST':
        try:
            # print(request.files)
            # logging.error(request.files)
            # request.__dict__
            logging.error(request.__dict__)
            f = request.files['file']
            # print()
            f_path = os.path.join(BASE_DIR, 'resources', 'static', 'uploads', secure_filename(f.filename))
            f.save(f_path)
            data = cv_service.parse_from_local(f_path)
            data.source = source
            data.source_method = 'upload'
            # print(data.__dict__)
            logging.info("sucess")
            tbService.save(data)
        except Exception as e:
            # print(e)
            logging.error("some thing is wrong")
            logging.exception(e)
            return {"status":"fail"}
        cv = tbService.get_by_id(data._id)
        cv = cv[0] if cv else None
    return json.dumps(cv, cls=JSONEncoder, ensure_ascii=False)


@inf_restful.route("/online/count_talent_banks", methods=['GET'])
def count_talent_banks():
    week_1 = datetime.timedelta(weeks=1)
    month_1 = datetime.timedelta(days=30)
    now_time = datetime.datetime.now()

    result = {
        'all': tbService.count_all_data(),
        'in_week': tbService.count_data_after(now_time - week_1),
        'in_month': tbService.count_data_after(now_time - month_1)
    }
    return json.dumps(result)


@inf_restful.route("/online/count_talent_tags", methods=['GET'])
def count_talent_tags():
    return json.dumps(tbService.count_tags())


@inf_restful.route('/online/save_to_bank', methods=['POST'])
def save_cv_to_bank():
    if request.method == 'POST':
        # json_data = dict(request.form)
        json_data = request.form["json"]
        print(json_data)
        try:
            cv = linkerService.parse(json_data)
        except Exception as e:
            logging.error(e)
            return "parsing error"
        try:
            tbService.save(cv)
        except Exception as e:
            logging.error(e)
            return "saving error"
        if tbService.get_by_id(cv._id):
            return "success"
        else:
            return "no exception but save failed"


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


