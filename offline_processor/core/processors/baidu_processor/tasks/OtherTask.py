from core.processors.baidu_processor import baiduProcessor
from core.base.BaseTask import BaseTask
from data_access.controller.CommonController4Mongo import CommonController4Mongo
from services.tool_services.neo_service import NeoService
from services.data_services.CommonDataService import commonDataService
from utils.Constants import is_bad_column, is_replicate_column, cv_label
from utils.Logger import logging
from core.linker.Searcher import Searcher
from core.linker.TerminologyLinker import TerminologyLinker
from core.common.mixins.Neo4jMixin import Neo4jMixin
import pandas as pd
import re
import uuid

neoService = NeoService.instance()
searcher = Searcher.instance()

@baiduProcessor.add_as_processors(order=11, stage=2, schema='kb_demo', table='kb_company')
class SaveTask(BaseTask):
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.controller = CommonController4Mongo(schema, table)

    def fit(self, data):
        self.controller.insert_datas_from_df(data)
        return data

@baiduProcessor.add_as_processors(order=12, stage=2)
class ExtractTask(BaseTask, Neo4jMixin):
    def __init__(self):
        self.members = []
        self.relations = []
        self.invests = []
        self.neoService = neoService

    def fit(self, data):
        companys = data.apply(lambda x: x[['_id', 'companyName', 'establishedDate', 'companyScale', 'companyLocation', 'brief', 'dom', 'companyType', 'regCapital']], axis=1)
        companys['name'] = companys['companyName']
        companys.apply(lambda x:self.save_company(x), axis=1)
        data.apply(lambda x: self.ontology_and_relation(x), axis=1)
        [self.save_company(x) for x in self.invests]
        [self.save_to_neo4j('member',x) for x in self.members if not self.if_exists('member', x['_id'])]
        [self.save_relation(x) for x in self.relations]

        self.members = []
        self.relations = []
        return data

    def save_company(self, x):
        if not self.if_exists('company', x['_id']):
            self.save_to_neo4j('company', x)

    def ontology_and_relation(self, x):
        members = x.get("members", [])
        if type(members) != list:
            members = []
        for member in members:
            self.extract_member_info(member, x['_id'])

        invests = x.get("invests", [])
        if type(invests) != list:
            invests = []
        for invest in invests:
            self.extract_invest_info(invest, x['_id'])


    def extract_member_info(self, member, jd_id):
         member_info = member
         member_info['_id'] = member['teamMember']
         member_info['name'] = member['teamMember']
         self.members.append(member_info)
         relation = {}
         relation['to_id'] = member_info['_id']
         relation['to_type'] = 'member'
         relation['from_id'] = jd_id
         relation['from_type'] = 'company'
         relation['name'] = '高管'
         self.relations.append(relation)

    def extract_invest_info(self, invest, jd_id):
        invest_name = invest['investorName']
        invest_info = searcher.search_company(invest_name)
        if not invest_info:
            invest_info = {}
            invest_info['name'] = invest_name
            invest_info['_id'] = invest_name
        else:
            invest_info['name'] = invest_name
        self.invests.append(invest_info)
        relation = invest
        relation['from_id'] = invest_info['_id']
        relation['from_type'] = 'company'
        relation['to_id'] = jd_id
        relation['to_type'] = 'company'
        relation['name'] = '投资'
        self.relations.append(relation)

