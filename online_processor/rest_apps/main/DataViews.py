from . import inf_restful
from flask import Flask, request, jsonify
import json
from utils.Encoder import JSONEncoder
from services.LinkerService import linkerService
from services.DataService import dataService

# @inf_restful.route("/hellow", methods=['GET'])
# def hellow():
#     return "hellow"
@inf_restful.route('/online/dataviews', methods=['POST'])
def get_data_vews():
    if request.method == 'POST':
        return ''

