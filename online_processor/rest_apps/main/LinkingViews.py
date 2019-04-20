from . import inf_restful
from flask import Flask, request, jsonify
import json
from utils.Encoder import JSONEncoder
from services.LinkerService import linkerService
from services.DataService import dataService
from services.KgizeService import kgService

@inf_restful.route('/online/link',
                   methods=["POST"])
def link_cv():
    """
    linking academies, companies, majors in cv
    :return: json format cv
    """
    if request.method == 'POST':
        # json_data = dict(request.form)
        json_data = request.form["json"]
        print(json_data)
        cv = linkerService.parse(json_data)
        dataService.save(cv)
        academies = linkerService.link_academy(cv)
        companys = linkerService.link_company(cv)
        terminologys = linkerService.link_terminology(cv)
        result = {}
        result['academies'] = academies
        result['companies'] = companys
        result['terminologys'] = terminologys
        # JSONEncoder().encode)
        return json.dumps(result, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route('/online/kgize', methods=['POST'])
def kgize():
    """
    covert a cv into a knowlege graph
    :return: json format cv represent as k,v pairs
    """
    if request.method == 'POST':
        # json_data = dict(request.form)
        json_data = request.form["json"]
        cv = linkerService.parse(json_data)
        dataService.save(cv)
        academies = linkerService.link_academy(cv)
        companys = linkerService.link_company(cv)
        terminologys = linkerService.link_terminology(cv)
        result = kgService.kgsizer_4tupe(cv, terminologys, academies, companys)
        return json.dumps(result, ensure_ascii=False, cls=JSONEncoder)
    pass


@inf_restful.route("/hellow", methods=['GET'])
def hellow():
    return "hellow"
