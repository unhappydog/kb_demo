from . import inf_restful
from flask import Flask, request, jsonify
import json
from utils.Encoder import JSONEncoder
from utils.Utils import parse_data_to_dict
from services.TalentBankService import tbService
from services.KBService import KBService
from services.LinkerService import linkerService
from services.DataService import dataService

kbService = KBService.instance()

@inf_restful.route("/online/kb/expand_entity/<string:label>/<string:name>/<string:_id>/<int:limit>",
                   methods=["GET"])
def expand_entity(label, name, _id, limit):
    name = None if name == 'none' else name
    _id = None if _id == 'none' else _id

    nodes, links = kbService.find_entity(label, name, _id, limit)
    data = {}
    data['nodes'] = nodes
    data['links'] = links
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/kb/demo_entity/<string:company>/<string:job>/<string:candidate>/<string:skill>", methods=['GET'])
def demo_entity(company, job, candidate, skill):
    company = False if company == 'false' else True
    job = False if job == 'false' else True
    candidate = False if candidate == 'false' else True
    skill = False if skill == 'false' else True
    data = kbService.demo_entity(company, job, candidate, skill, 10)
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder) 

@inf_restful.route("/online/kb/demo_entity/<string:company>/<string:job>/<string:candidate>", methods=['GET'])
def demo_entity_old(company, job, candidate):
    company = False if company == 'false' else True
    job = False if job == 'false' else True
    candidate = False if candidate == 'false' else True
    data = kbService.demo_entity(company, job, candidate, True, 10)
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder) 

@inf_restful.route("/online/kb/get_data/<string:data_type>/<string:_id>")
def get_data_by_type_and_id(data_type, _id):
    if data_type == 'cv':
        _cv = tbService.get_by_id(_id)
        if _cv:
            cv = _cv[0]
        else:
            return json.dumps({"result":"failed"})

        cv = linkerService.parse(cv)
        dataService.save(cv)
        academies = linkerService.link_academy(cv)
        companys = linkerService.link_company(cv)
        terminologys = linkerService.link_terminology(cv)
        cv_dict = parse_data_to_dict(cv)
        risks = linkerService.risk_recongnize(cv_dict)
        result = {}
        result['academies'] = academies
        result['companies'] = companys
        result['terminologys'] = terminologys
        result['risks'] = risks
        cv.__dict__['linked_result'] = result
        dataService.save(cv)
        return json.dumps(result, ensure_ascii=False, cls=JSONEncoder)
    elif data_type == 'company':
        _company = dataService.get_company_by_id(_id)
        if _company:
            _company = _company[0]
        else:
            return json.dumps({"result":"failed"})
        return json.dumps(_company, ensure_ascii=False, cls=JSONEncoder)


@inf_restful.route("/online/kb/paths_between_nodes/<string:first_id>/<string:second_id>/<int:limit>")
def get_paths_between_nodes(first_id, second_id, limit):
    first_id = None if first_id == 'none' else first_id
    second_id = None if  second_id == 'none' else second_id
    first_id = "HWufE78VWOSOrYKUoDC(WA" if first_id is None else first_id
    second_id = "电子信息工程" if second_id is None else second_id
    nodes, links = kbService.paths_between_entitys(first_id, second_id, limit)
    data = {}
    data['nodes'] = nodes
    data['links'] = links
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder)
