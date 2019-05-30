from . import inf_restful
from flask import Flask, request, jsonify
from utils.Logger import logging
from utils.Utils import parse_data_to_dict
import json
from utils.Encoder import JSONEncoder
from services.LinkerService import linkerService
from services.CVService import cv_service
from services.TalentBankService import tbService
from werkzeug.utils import secure_filename
from settings import BASE_DIR
import datetime
import os

@inf_restful.route("/online/sourcing/test_hellow")
def test_hellow_v2():
    return "hellow v2"

@inf_restful.route("/online/sourcing/search_talent_bank/<string:keyword>/<string:location>/<string:experience>/<string:education>/<string:talent_bank_id>/<int:page>/<int:limit>")
def search_talent_by_keyword_v2(keyword, location, experience, education,talent_bank_id, page, limit):
    """
    search talent by keyword,
    """
    if talent_bank_id == 'none':
        talent_bank_id = None
    location = None if location == 'none' else location
    experience = None if experience == 'none' else experience
    education = None if education == 'none' else education
    # import pdd; pdb.set_trace()
    datas = tbService.search_by_keyword(keyword=keyword, location=location, experience=experience, educationDegree=education, talent_bank_id=talent_bank_id,page=page, size=limit)
    return json.dumps(datas,ensure_ascii=False,cls=JSONEncoder)

@inf_restful.route('/online/sourcing/move_to_talent_bank/<string:job_title>/<string:source>/<string:source_method>/<string:talent_bank_id>', methods=['POST'])
def move_to_talent_bank(job_title, source, source_method, talent_bank_id):
    """
    收藏到简历库功能
    """
    source= None if source == 'none' else source
    source_method = None if source_method == 'none' else source_method
    talent_bank_id = None if talent_bank_id == 'none' else talent_bank_id
    json_data = request.form['json']

    # import pdb; pdb.set_trace()
    # print("start debug")
    try:
        cv = linkerService.parse(json_data)
    except Exception as e:
        logging.error(e)
        return json.dumps({"state":"failed","log":"parsing error"})
    if source:
        cv['source'] = source
    if source_method:
        cv['source_method'] = source_method
    cv['jobTitle'] = job_title
    try:
        tbService.save(cv, talent_bank_id)
    except Exception as e:
        logging.error(e)
        return "saving error"

    if tbService.get_by_id(cv._id, talent_bank_id):
        return "sucess"
    else:
        return "no exception but save failed"


@inf_restful.route("/online/talent_bank/upload/<string:talent_bank_id>", methods=['POST'])
def upload(talent_bank_id=None):
    if request.method == 'POST':
        try:
            logging.error(request.__dict__)
            f = request.files['file']
            f_path = os.path.join(BASE_DIR, 'resources', 'static', 'uploads', secure_filename(f.filename))
            f.save(f_path)
            data = cv_service.parse_from_local(f_path)
            data.source_method = 'upload'
            logging.info("sucess")
            tbService.save(data, talent_bank_id)
        except Exception as e:
            logging.error("some thing is wrong")
            logging.exception(e)
            return {"status": "fail"}
        cv = tbService.get_by_id(data._id, talent_bank_id)
        cv = cv[0] if cv else None
        return json.dumps(cv, cls=JSONEncoder, ensure_ascii=False)

@inf_restful.route("/online/talent_bank/get_talent_by/<string:location>/<string:experience>/<string:education>/<string:source>/<string:job_title>/<string:source_method>/<string:talent_bank_id>/<int:page>/<int:limit>")
def get_talent_by(location, experience, education, source, job_title, source_method, talent_bank_id, page, limit):
    if talent_bank_id == 'none':
        talent_bank_id = None
    location = None if location == 'none' else location
    experience = None if experience == 'none' else experience
    education = None if education == 'none' else education
    source = None if source == 'none' else education
    job_title = None if job_title == 'none' else job_title
    source_method = None if source_method =='none' else source_method

    datas = tbService.get_datas_by(location=location, experience=experience, educationDegree=education, source=source, source_method=source_method, job_title=job_title,talent_bank_id=talent_bank_id, page=page, size=limit)

    # if by == "source":
    #     datas = tbService.get_datas_by(location=location, experience=experience, educationDegree=education, source=value,talent_bank_id=talent_bank_id, page=page, size=limit)

    # elif by == "job_title":
    #     datas = tbService.get_datas_by(location=location, experience=experience, educationDegree=education, job_title=value,talent_bank_id=talent_bank_id, page=page, size=limit)

    return json.dumps(datas,ensure_ascii=False, cls=JSONEncoder)

@inf_restful.route("/online/talent_bank/add_to_favorite/<string:cv_id>/<string:talent_bank_id>/<string:user_id>")
def add_to_favorite(cv_id, talent_bank_id, user_id):
    if tbService.add_to_favorite(cv_id, user_id, talent_bank_id):
        return "sucess"
    else:
        return "failed"

@inf_restful.route("/online/talent_bank/get_favorite/<string:user_id>/<string:location>/<string:experience>/<string:education>/<string:source>/<string:source_method>/<string:talent_bank_id>/<int:page>/<int:limit>")
def get_favorite(user_id, location, experience, education, source,source_method, talent_bank_id, page, limit):
    location = None if location == 'none' else location
    experience = None if experience == 'none' else experience
    education = None if education == 'none' else education
    source = None if source == 'none' else education
    source_method = None if source_method == 'none' else education

    datas = tbService.get_favorite(user_id, location, experience, education, source,source_method, None, None, page, limit, talent_bank_id)

    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)
