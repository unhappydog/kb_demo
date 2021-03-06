from . import inf_restful
from flask import Flask, request, jsonify
from utils.Logger import logging
from utils.Utils import parse_data_to_dict
import json
from utils.Encoder import JSONEncoder
from services.LinkerService import linkerService
from services.CVService import cv_service
from services.TalentBankService import tbService
from services.DataService import dataService
from services.PersonJobFitService import PersonJobFitService
from services.UserService import UserService
from werkzeug.utils import secure_filename
from settings import BASE_DIR
import datetime
import os

personJobFitService = PersonJobFitService.instance()
userService = UserService.instance()

@inf_restful.route("/online/sourcing/test_hellow")
def test_hellow_v2():
    return "hellow v2"

@inf_restful.route("/online/sourcing/search_talent_bank/<string:keyword>/<string:location>/<string:experience>/<string:education>/<string:sort_by>/<string:talent_bank_id>/<int:page>/<int:limit>")
def search_talent_by_keyword_v2(keyword, location, experience, education, sort_by,talent_bank_id, page, limit):
    """
    search talent by keyword,
    """
    if talent_bank_id == 'none':
        talent_bank_id = None
    location = None if location == 'none' else location
    experience = None if experience == 'none' else experience
    education = None if education == 'none' else education
    sort_by = None if sort_by == 'none' else sort_by
    keyword = "" if keyword == 'none' else keyword

    # import pdd; pdb.set_trace()
    datas = tbService.search_by_keyword(keyword=keyword, location=location, experience=experience, educationDegree=education, talent_bank_id=talent_bank_id,sort_by=sort_by,page=page, size=limit)
    return json.dumps(datas,ensure_ascii=False,cls=JSONEncoder)


@inf_restful.route('/online/sourcing/move_to_talent_bank/<string:job_title>/<string:user_tag>/<string:source>/<string:source_method>/<string:talent_bank_id>', methods=['POST'])
def move_to_talent_bank(job_title, user_tag, source, source_method, talent_bank_id):
    """
    收藏到简历库功能
    """
    source= None if source == 'none' else source
    source_method = None if source_method == 'none' else source_method
    talent_bank_id = None if talent_bank_id == 'none' else talent_bank_id
    job_title = None if job_title == 'none' else job_title
    user_tag = None if user_tag == 'none' else user_tag
    if job_title and user_tag:
        return json.dumps({"state":"failed", "log":"job_title and user_tag cannot be set at the same time"})
    elif user_tag:
        job_title=user_tag
        position = False
    elif job_title:
        position = dataService.get_position_by(job_title)
        if not position:
            return json.dumps({"state":"failed", "log":"positon doesn't exists"})
        position = position[0]
    json_data = request.form['json']

    try:
        cv = linkerService.parse(json_data)
        skill_tags = linkerService.gen_skill_tag(cv)
        cv.skill_tag = skill_tags
    except Exception as e:
        logging.error(e)
        return json.dumps({"state":"failed","log":"parsing error"})
    if source:
        cv['source'] = source
    if source_method:
        cv['source_method'] = source_method
    cv['jobTitle'] = job_title
    # job person fit
    if position:
       score = personJobFitService.score(cv, position)
       cv['score'] = score

    try:
        tbService.save(cv, talent_bank_id)
    except Exception as e:
        logging.error(e)
        # return "saving error"
        return json.dumps({"state":"failed", "log":"saving error"})

    if tbService.get_by_id(cv._id, talent_bank_id):
        # return "sucess"
        return json.dumps({"state":"success"})

    else:
        # return "no exception but save failed"
        return json.dumps({"state":"failed", "log":"no exeception occured but save failed"})


@inf_restful.route("/online/talent_bank/upload/<string:job_title>/<string:user_tag>/<string:source>/<string:source_method>/<string:talent_bank_id>", methods=['POST'])
def upload(job_title, user_tag, source, source_method, talent_bank_id):
    source= None if source == 'none' else source
    source_method = None if source_method == 'none' else source_method
    talent_bank_id = None if talent_bank_id == 'none' else talent_bank_id
    job_title = None if job_title == 'none' else job_title
    user_tag = None if user_tag == 'none' else user_tag
    if job_title and user_tag:
        return json.dumps({"state":"failed", "log":"job_title and user_tag cannot be set at the same time"})
    elif user_tag:
        job_title=user_tag
        position = False
    elif job_title:
        position = dataService.get_position_by(job_title)
        if not position:
            return json.dumps({"state":"failed", "log":"positon doesn't exists"})
        position = position[0]


    if request.method == 'POST':
        try:
            f = request.files['file']
            f_path = os.path.join(BASE_DIR, 'resources', 'static', 'uploads', secure_filename(f.filename))
            f.save(f_path)
            data = cv_service.parse_from_local(f_path)
            data.source_method = 'upload'
            if source:
                data['source'] = source
            data['jobTitle'] = job_title
            # job person fit
            if position:
                score = personJobFitService.score(data, position)
                data['score'] = score
            data.skill_tag = linkerService.gen_skill_tag(data)
            logging.info("sucess")
            tbService.save(data, talent_bank_id)
        except Exception as e:
            logging.error("some thing is wrong")
            logging.exception(e)
            return json.dumps({"status": "fail"}, cls=JSONEncoder)
        cv = tbService.get_by_id(data._id, talent_bank_id)
        cv = cv[0] if cv else None
        return json.dumps(cv, cls=JSONEncoder, ensure_ascii=False)

@inf_restful.route("/online/talent_bank/search_by_keyword/<string:keyword>/<string:update_time>/<string:experience>/<string:education>/<string:source>/<string:job_title>/<string:source_method>/<string:sort_by>/<string:talent_bank_id>/<int:page>/<int:limit>")
def search_talent_by_Keyword_position_company(keyword, update_time, experience,education,source,job_title, source_method, sort_by, talent_bank_id, page, limit):
    if talent_bank_id == 'none':
        talent_bank_id = None
    update_time = None if update_time == 'none' else update_time
    experience = None if experience == 'none' else experience
    education = None if education == 'none' else education
    source = None if source == 'none' else source
    job_title = None if job_title == 'none' else job_title
    source_method = None if source_method =='none' else source_method
    sort_by = None if sort_by == 'none' else sort_by
    keyword = '' if keyword == 'none' else keyword

    datas = tbService.get_datas_by(keyword=keyword,update_time=update_time, experience=experience, educationDegree=education, source=source, source_method=source_method, job_title=job_title, sort_by=sort_by,talent_bank_id=talent_bank_id, page=page, size=limit)
    return json.dumps(datas,ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/talent_bank/get_talent_by/<string:update_time>/<string:experience>/<string:education>/<string:source>/<string:job_title>/<string:source_method>/<string:sort_by>/<string:talent_bank_id>/<string:location>/<int:page>/<int:limit>")
def get_talent_by(update_time, experience, education, source, job_title, source_method, sort_by, talent_bank_id, location, page, limit):
    if talent_bank_id == 'none':
        talent_bank_id = None
    update_time = None if update_time == 'none' else update_time
    experience = None if experience == 'none' else experience
    education = None if education == 'none' else education
    source = None if source == 'none' else source
    job_title = None if job_title == 'none' else job_title
    source_method = None if source_method =='none' else source_method
    sort_by = None if sort_by == 'none' else sort_by
    location = None if location == 'none' else location

    datas = tbService.get_datas_by(update_time=update_time, experience=experience, educationDegree=education, source=source, source_method=source_method, job_title=job_title, sort_by=sort_by, talent_bank_id=talent_bank_id,location=location, page=page, size=limit)
    return json.dumps(datas,ensure_ascii=False, cls=JSONEncoder)

@inf_restful.route("/online/talent_bank/add_to_favorite/<string:cv_id>/<string:talent_bank_id>/<string:user_id>")
def add_to_favorite(cv_id, talent_bank_id, user_id):
    cv = tbService.get_by_id(cv_id,talent_bank_id=talent_bank_id)
    if cv:
        cv = cv[0]
        cv_object = linkerService.parse(cv)
        cv['skill_tag'] = linkerService.gen_skill_tag(cv_object)

        if tbService.add_to_favorite(cv, user_id, talent_bank_id):
            return "success"
        else:
            return "failed"
    else:
        cv = dataService.get(cv_id)
        if cv:
            cv = linkerService.parse(cv)
            cv.skill_tag = linkerService.gen_skill_tag(cv)
            tbService.save(cv, talent_bank_id)
            if tbService.add_to_favorite(cv_id, user_id, talent_bank_id):
                return "success"
        return "failed"

@inf_restful.route("/online/talent_bank/remove_from_favorite/<string:cv_id>/<string:talent_bank_id>/<string:user_id>")
def remove_from_favorite(cv_id, talent_bank_id, user_id):
    if tbService.remove_from_favorite(cv_id, user_id, talent_bank_id):
        return "success"
    else:
        return "failed"

@inf_restful.route("/online/talent_bank/remove_from_favorite_v2/<string:talent_bank_id>/<string:user_id>", methods=["POST"])
def remove_from_favorite_v2(talent_bank_id, user_id):
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        cv_list = request.form['json']
        try:
            cv_list = json.loads(cv_list, encoding='utf8')
            for cv_id in cv_list['cv_list']:
                if not tbService.remove_from_favorite(cv_id, user_id, talent_bank_id):
                    return "failed"
            else:
                return "success"
        except:
            return "failed"


@inf_restful.route("/online/talent_bank/get_favorite/<string:user_id>/<string:update_time>/<string:experience>/<string:education>/<string:source>/<string:source_method>/<string:sort_by>/<string:talent_bank_id>/<int:page>/<int:limit>")
def get_favorite(user_id, update_time, experience, education, source,source_method, sort_by, talent_bank_id, page, limit):
    update_time = None if update_time == 'none' else update_time
    experience = None if experience == 'none' else experience
    education = None if education == 'none' else education
    source = None if source == 'none' else education
    source_method = None if source_method == 'none' else education
    sort_by = None if sort_by == 'none' else sort_by
    datas = tbService.get_favorite(user_id, None, update_time, experience, education, source,source_method, None, None, page, limit, talent_bank_id, sort_by)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)

@inf_restful.route("/online/talent_bank/count_talent_bank/<string:talent_bank_id>", methods=['GET'])
def count_talent_bank(talent_bank_id):
    datas = {
        'job_title': tbService.count_column("jobTitle", talent_bank_id),
        'source': tbService.count_column("source", talent_bank_id)
    }
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/talent_bank/gen_talent_map/<string:company>", methods=["GET"])
def gen_talent_map(company):
    datas = tbService.gen_map(company)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)

@inf_restful.route("/online/talent_bank/gen_talent_map_chart_data/<string:company>/<string:in_office>", methods=['GET'])
def gen_talent_map_chart_data(company, in_office):
    in_office = None if in_office == 'none' else in_office
    if in_office == 'true':
        in_office = True
    elif in_office == 'false':
        in_office = False
    datas = tbService.gen_chart_data(company, in_office, None, None)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)

@inf_restful.route("/online/talent_bank/get_map_cv/<string:company>/<string:in_office>")
def get_map_cv(company, in_office):
    in_office = None if in_office == 'none' else in_office
    if in_office == 'true':
        in_office = True
    elif in_office == 'false':
        in_office = False
    datas = tbService.get_map_cv(company, in_office)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)

@inf_restful.route("/online/talent_bank/goto/<string:all_follow>/<string:company>/<string:academy>/<string:skill_tag>/<string:update_time>/<string:experience>/<string:education>/<string:source>/<string:source_method>/<string:sort_by>/<string:user_id>/<string:talent_bank_id>/<int:page>/<int:limit>")
def goto(all_follow,company, academy, skill_tag,update_time, experience, education, source,source_method, sort_by, user_id, talent_bank_id, page, limit):
    all_follow = None if all_follow == 'none' else all_follow
    user_id = None if user_id == 'none' else user_id
    sort_by = None if sort_by == 'none' else sort_by
    if all_follow:
        user_interest = userService.get_interest_by_id(user_id, True, True, True)
        if all_follow == 'company':
            interest = user_interest['followed_company']
            datas = tbService.get_all_cv(interest, None, None, None, None, page, limit)
        elif all_follow == 'academy':
            interest = user_interest['followed_academy']
            datas = tbService.get_all_cv(None, interest,  None, None, None, page, limit)
        elif all_follow == 'skill':
            interest = user_interest['followed_skill']
            datas = tbService.get_all_cv(None, None, interest,  None, None, page, limit)
        return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)

    company = None if company == 'none' else company
    academy = None if academy == 'none' else academy
    skill_tag = None if skill_tag == 'none' else skill_tag
    update_time = None if update_time == 'none' else update_time
    experience = None if experience == 'none' else experience
    education = None if education == 'none' else education
    source = None if source == 'none' else education
    source_method = None if source_method == 'none' else education
    datas = tbService.get_datas_by(update_time=update_time, experience=experience, educationDegree=education,source=source, source_method=source_method, sort_by=sort_by, company=company, academy=academy, skill_tag=skill_tag, talent_bank_id=talent_bank_id)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/talent_bank/get_cv/<string:cv_id>/<string:talent_bank_id>")
def get_cv(cv_id, talent_bank_id):
    result = tbService.get_by_id(cv_id, talent_bank_id)
    if result:
        return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)
    else:
        data = {'result':'failed', 'log':'Unknown'}
        return json.dumps(data)

@inf_restful.route("/online/kanban/move_to_kanban/<string:kanban_name>/<string:cv_id>/<string:talent_bank_id>")
def move_to_kanban(kanban_name, cv_id, talent_bank_id):
    cv = tbService.get_by_id(cv_id,talent_bank_id=talent_bank_id)
    if not cv:
        cv = dataService.get(cv_id)
        tbService.save(cv, talent_bank_id=talent_bank_id, save_tag=True)

    reuslt = tbService.move_cv_to_kanban(cv_id, kanban_name, talent_bank_id)
    if reuslt:
        data = {"result":"sucess"}
    else:
        data = {"result":"failed", "log":"unknown"}
    return json.dumps(data)

@inf_restful.route("/online/kanban/get_cv_by_kanban/<string:kanban_name>/<string:job_title>/<int:page>/<int:size>/<string:talent_bank_id>")
def get_cv_by_kanban(kanban_name, job_title, page, size, talent_bank_id):
    talent_bank_id = None if talent_bank_id == 'none' else talent_bank_id
    result = tbService.get_cv_by_kanban(kanban_name, job_title, page, size, talent_bank_id)
    return json.dumps(result, ensure_ascii=False, cls=JSONEncoder)
