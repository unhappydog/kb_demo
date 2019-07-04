from . import inf_restful
from flask import Flask, request, jsonify
import json
from utils.Encoder import JSONEncoder
from services.KBService import KBService
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


@inf_restful.route("/online/kb/demo_entity/<string:company>/<string:job>/<string:candidate>", methods=['GET'])
def demo_entity(company, job, candidate):
    company = False if company == 'false' else True
    job = False if job == 'false' else True
    candidate = False if candidate == 'false' else True
    data = kbService.demo_entity(company, job, candidate, 10)
    return json.dumps(data, ensure_ascii=False, cls=JSONEncoder) 
