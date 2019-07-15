from . import inf_restful
from flask import Flask, request, jsonify
import json
from werkzeug.utils import secure_filename
from settings import BASE_DIR
import datetime
import re
import os

@inf_restful.route("/rule_engine/inf", methods=['POST'])
def inf():
    if request.method = 'POST':
        data = request.form.get['json']
        

