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


# @inf_restful.route(
#     "/online/talent_bank/search/<string:by>/<string:searchWord>/<int:page>/<int:limit>/<string:mode>/<string:talent_bank_id>",
#     methods=['GET'])
# # @inf_restful.route("/online/talent_bank/search/<string:by>/<string:searchWord>/<int:page>/<int:limit>/<string:mode>",
# #                    methods=['GET'])
# def get_talent_by(by, searchWord, page, limit, mode, talent_bank_id=None):
#     """
#     按照职位名称、教育程度 、来源、或者其它查询人才库
#     :param by:
#     :param searchWord:
#     :param page:
#     :param limit:
#     :return:
#     """
#     if mode == "none":
#         mode = None
#     if by == "keyword":
#         datas = tbService.search_by_name(searchWord, page, limit, mode, talent_bank_id=talent_bank_id)
#     elif by == "education":
#         datas = tbService.search_by_education(searchWord, page, limit, mode, talent_bank_id=talent_bank_id)
#     elif by == "source":
#         datas = tbService.search_by_source(searchWord, page, limit, mode, talent_bank_id=talent_bank_id)
#     elif by == "none" or by == 'undefined':
#         datas = tbService.get_datas(page, limit, mode, talent_bank_id=talent_bank_id)
#     return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/talent_bank/search_with_name/<string:name>/<string:by>/<string:searchWord>/<int:page"
                   ">/<int:limit>/<string:mode>/<string:talent_bank_id>",
                   methods=['GET'])
# @inf_restful.route("/online/talent_bank/search_with_name/<string:name>/<string:by>/<string:searchWord>/<int:page"
#                    ">/<int:limit>/<string:mode>",
#                    methods=['GET'])
def get_talent_with_name_by(name, by, searchWord, page, limit, mode, talent_bank_id=None):
    """
    通过简历中任务名称来搜索简历，筛选条件有职位名称、教育程度 、来源、或者其它查询人才库
    :param by:
    :param searchWord:
    :param page:
    :param limit:
    :return:
    """
    if mode == "none":
        mode = None
    if by == "keyword":
        datas = tbService.search_by_name(searchWord, page, limit, mode, name, talent_bank_id=talent_bank_id)
    elif by == "education":
        datas = tbService.search_by_education(searchWord, page, limit, mode, name, talent_bank_id=talent_bank_id)
    elif by == "source":
        datas = tbService.search_by_source(searchWord, page, limit, mode, name, talent_bank_id=talent_bank_id)
    elif by == "none" or by == 'undefined':
        datas = tbService.get_datas(page, limit, mode, name, talent_bank_id=talent_bank_id)
    return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


# @inf_restful.route("/online/sourcing/search_talent_bank/<string:keyword>/<int:page>/<int:limit>/<talent_bank_id>",
#                    methods=['GET'])
# # @inf_restful.route("/online/sourcing/search_talent_bank/<string:keyword>/<int:page>/<int:limit>", methods=['GET'])
# def search_talent_by_keyword(keyword, page, limit, talent_bank_id=None):
#     datas = tbService.search_by_keyword(keyword, page=page, size=limit, talent_bank_id=None)
#     return json.dumps(datas, ensure_ascii=False, cls=JSONEncoder)


# @inf_restful.route("/online/upload/<string:source>/<string:talent_bank_id>", methods=['POST'])
# # @inf_restful.route("/online/upload/<string:source>", methods=['POST'])
# def upload(source, talent_bank_id=None):
#     if request.method == 'POST':
#         try:
#             # print(request.files)
#             # logging.error(request.files)
#             # request.__dict__
#             logging.error(request.__dict__)
#             f = request.files['file']
#             # print()
#             f_path = os.path.join(BASE_DIR, 'resources', 'static', 'uploads', secure_filename(f.filename))
#             f.save(f_path)
#             data = cv_service.parse_from_local(f_path)
#             data.source = source
#             data.source_method = 'upload'
#             # print(data.__dict__)
#             logging.info("sucess")
#             tbService.save(data, talent_bank_id)
#         except Exception as e:
#             # print(e)
#             logging.error("some thing is wrong")
#             logging.exception(e)
#             return {"status": "fail"}
#         cv = tbService.get_by_id(data._id, talent_bank_id)
#         cv = cv[0] if cv else None
#         return json.dumps(cv, cls=JSONEncoder, ensure_ascii=False)


# @inf_restful.route("/online/count_talent_banks/<string:talent_bank_id>", methods=['GET'])
# # @inf_restful.route("/online/count_talent_banks", methods=['GET'])
# def count_talent_banks(talent_bank_id):
#     week_1 = datetime.timedelta(weeks=1)
#     month_1 = datetime.timedelta(days=30)
#     now_time = datetime.datetime.now()

#     result = {
#         'all': tbService.count_all_data(talent_bank_id),
#         'in_week': tbService.count_data_after(now_time - week_1, talent_bank_id),
#         'in_month': tbService.count_data_after(now_time - month_1, talent_bank_id)
#     }
#     return json.dumps(result)


# @inf_restful.route("/online/count_talent_tags/<string:talent_bank_id>", methods=['GET'])
# # @inf_restful.route("/online/count_talent_tags", methods=['GET'])
# def count_talent_tags(talent_bank_id):
#     return json.dumps(tbService.count_tags(talent_bank_id))


@inf_restful.route('/online/save_to_bank/<string:talent_bank_id>', methods=['POST'])
# @inf_restful.route('/online/save_to_bank', methods=['POST'])
def save_cv_to_bank(talent_bank_id):
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
            tbService.save(cv, talent_bank_id)
        except Exception as e:
            logging.error(e)
            return "saving error"
        if tbService.get_by_id(cv._id, talent_bank_id):
            return "success"
        else:
            return "no exception but save failed"
