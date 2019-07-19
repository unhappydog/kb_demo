from core.processors.company_processor import companyProcessor
from core.base.BaseTask import BaseTask
        # import pdb; pdb.set_trace()
from data_access.controller.CommonController4Mongo import CommonController4Mongo
from services.tool_services.neo_service import NeoService
from services.data_services.CommonDataService import commonDataService
from utils.Constants import is_bad_column, is_replicate_column, cv_label
from utils.Logger import logging
from core.linker.Searcher import Searcher
from core.linker.TerminologyLinker import TerminologyLinker
import pandas as pd
import re
import uuid

neoService = NeoService.instance()
searcher = Searcher.instance()

@companyProcessor.add_as_processors(order=12, stage=2)
class ExtractTask(BaseTask):
    def __init__(self):
        self.members = []
        self.relations = []
        self.invests = []

    def fit(self, data):
        # data = data[data.apply(lambda x: x[is_bad_column] ==0 and x[is_replicate_column] ==0 , axis=1)]
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


    def save_relation(self, relation):
        relation_str = [ "{0}:\"{1}\"".format(k,v) for k,v in relation.items()]
        relation_str = "{" +",".join(relation_str) + "}"

        try:
            data = neoService.exec("match (n1:{0})-[r:{4}]-(n2:{1}) where n1._id =\"{2}\" and n2._id =\"{3}\" return r".format(
            relation['from_type'],
            relation['to_type'],
            relation['from_id'],
            relation['to_id'],
            relation['name'])).data()
            if data:
                return

        except Exception as e:
            logging.exception("check duplicate error")

        sql = "match (n1:{0}), (n2:{1}) where n1._id =\"{2}\" and n2._id =\"{3}\" create (n1)-[r:{4} {5}]->(n2)".format(
            relation['from_type'],
            relation['to_type'],
            relation['from_id'],
            relation['to_id'],
            relation['name'],
            relation_str)
        try:
            neoService.exec(sql)
        except Exception as e:
            logging.error("create relation error")
            logging.exception("save relation error")

    def save_to_neo4j(self, label, x):
        if type(x) == pd.Series:
            x = x.to_dict()
        neoService.create(label, **x)

    def if_exists(self, label, _id):
        try:
            data = neoService.exec("match (n:{0}) where n._id=\"{1}\" return n".format(label, _id)).data()
        except Exception as e:
            logging.exception("error occured when checking if exists")
            return True

        if data:
            return True
        else:
            return False

