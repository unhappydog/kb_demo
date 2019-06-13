from . import inf_restful
from flask import Flask, request, jsonify
from utils.Logger import logging
from utils.Utils import parse_data_to_dict
import json
from utils.Encoder import JSONEncoder
from services.LinkerService import linkerService
from services.DataService import dataService
from services.KgizeService import kgService
from services.UserService import UserService

userService = UserService.instance()


@inf_restful.route('/online/link',
                   methods=["POST"])
def link_cv():
    """
    linking academies, companies, majors in cv
    :return: json format cv
    """
    logging.debug("accepted data")
    if request.method == 'POST':
        # logging.debug(dir(request))
        json_data = request.form["json"]
        # logging.debug(json_data)
        cv = linkerService.parse(json_data)
        dataService.save(cv)
        academies = linkerService.link_academy(cv)
        companys = linkerService.link_company(cv)
        terminologys = linkerService.link_terminology(cv)
        logging.debug("terminologys is :" + json.dumps(terminologys, ensure_ascii=False, cls=JSONEncoder))
        cv_dict = parse_data_to_dict(cv)
        risks = linkerService.risk_recongnize(cv_dict)
        result = {}
        result['academies'] = academies
        logging.debug("_________academies\n")
        # logging.debug(academies)
        result['companies'] = companys
        result['terminologys'] = terminologys
        result['risks'] = risks
        cv.__dict__['linked_result'] = result
        dataService.save(cv)
        return json.dumps(result, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route('/online/kgize', methods=['POST'])
def kgize():
    """
    covert a cv into a knowlege graph
    :return: json format cv represent as k,v pairs
    """
    if request.method == 'POST':
        # json_data = dict(request.form)
        json_data = request.form["_id"]

        cv =dataService.get(json_data)
        if cv:
            cv = linkerService.parse(cv)
        else:
            return "None id find"
        # academies = linkerService.link_academy(cv)
        # companys = linkerService.link_company(cv)
        # terminologys = linkerService.link_terminology(cv)
        academies = cv.linked_result['academies']
        companys = cv.linked_result['companies']
        terminologys = cv.linked_result['terminologys']
        result = kgService.kgsizer_4tupe(cv, terminologys, academies, companys)
        return json.dumps(result, ensure_ascii=False, cls=JSONEncoder)
    pass


@inf_restful.route('/online/linkv2/<string:user_id>',
                   methods=["POST"])
def link_cv_v2(user_id):
    """
    linking academies, companies, majors in cv
    :return: json format cv
    """
    logging.debug("accepted data")
    if request.method == 'POST':
        # logging.debug(dir(request))
        json_data = request.form["json"]
        # logging.debug(json_data)
        cv = linkerService.parse(json_data)
        dataService.save(cv)
        academies = linkerService.link_academy(cv)
        companys = linkerService.link_company(cv)
        terminologys = linkerService.link_terminology(cv)
        logging.debug("terminologys is :" + json.dumps(terminologys, ensure_ascii=False, cls=JSONEncoder))
        cv_dict = parse_data_to_dict(cv)
        risks = linkerService.risk_recongnize(cv_dict)

        result = userService.is_followed(companys, academies, terminologys, user_id)
        result['risks'] = risks
        cv.__dict__['linked_result'] = result
        dataService.save(cv)
        return json.dumps(result, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route('/online/save', methods=['POST'])
def save_cv():
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
            dataService.save(cv)
        except Exception as e:
            logging.error(e)
            return "saving error"
        if dataService.get(cv._id):
            return "success"
        else:
            return "no exception but save failed"



@inf_restful.route("/hellow", methods=['GET'])
def hellow():
    return "hellow"
