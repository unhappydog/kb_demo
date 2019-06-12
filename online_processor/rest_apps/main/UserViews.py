from . import inf_restful
from flask import Flask, request, jsonify
from utils.Logger import logging
from utils.Utils import parse_data_to_dict, check_if_none
import json
from utils.Encoder import JSONEncoder
from services.LinkerService import linkerService
from services.CVService import cv_service
from services.TalentBankService import tbService
from services.DataService import dataService
from services.UserService import UserService
from werkzeug.utils import secure_filename
from settings import BASE_DIR
import datetime
import os

userService = UserService.instance()

@inf_restful.route("/online/user/test_hellow")
def test_user_hellow():
    return "user worked"

@inf_restful.route("/online/user/follow/<string:user_id>/<string:company>/<string:academy>/<string:skill>")
def follow(user_id, company, academy, skill):
    company = check_if_none(company)
    academy = check_if_none(academy)
    skill = check_if_none(skill)
    if userService.get_user(user_id):
        userService.update_add_interest(user_id, company, academy, skill)
        return json.dumps({"result":"success"})
    else:
        if userService.add_user(user_id, company, academy, skill):
            return json.dumps({"result":"success"})
        else:
            return json.dumps({"result":"failed", "log":"unknown"})


@inf_restful.route("/online/user/unfollow/<string:user_id>/<string:company>/<string:academy>/<string:skill>")
def unfollow(user_id, company, academy, skill):
    company = check_if_none(company)
    academy = check_if_none(academy)
    skill = check_if_none(skill)
    if userService.get_user(user_id):
        userService.update_remove_interest(user_id, company, academy, skill)
        return json.dumps({"result":"success"})
    else:
        return json.dumps({"result":"failed", "log":"user doesn't exists"})

@inf_restful.route("/online/user/get_interests/<string:user_id>/<int:company>/<int:academy>/<int:skill>")
def get_interests(user_id, company, academy, skill):
    company = True if company != 0 else False
    academy = False if academy == 0 else True
    skill = False if skill == 0 else True
    datas = userService.get_interest_by_id(user_id, company, academy, skill)
    return json.dumps(datas, ensure_ascii=False)
