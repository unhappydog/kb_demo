from core.processors.news_processor import newsProcessor
from core.base.BaseTask import BaseTask
from core.processors.talent_processor import talentProcessor
from data_access.controller.CommonController4Mongo import CommonController4Mongo
from services.tool_services.neo_service import NeoService
from utils.Constants import is_bad_column, is_replicate_column, cv_label
from utils.Logger import logging
from core.linker.Searcher import Searcher
from core.linker.TerminologyLinker import TerminologyLinker
import pandas as pd
import re

searcher = Searcher.instance()
neoService = NeoService.instance()


@talentProcessor.add_as_processors(order=11, stage=2, schema='kb_graph', table='kb_graph_talent_processed')
class SaveTask(BaseTask):
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.controller = CommonController4Mongo(schema, table)


    def fit(self, data):
        self.controller.insert_datas_from_df(data)
        return data


@talentProcessor.add_as_processors(order=12, stage=2)
class ExtractTask(BaseTask):
    def __init__(self):
        self.company = []
        self.skills = []
        self.relations = []
        self.cities = []
        self.jobs = []

    def fit(self, data):
        data = data[data.apply(lambda x: x[is_bad_column] ==0 and x[is_replicate_column] ==0 , axis=1)]
        jds = data.apply(lambda x: x[['_id', 'Name', 'Company','Salary','City','Education','Number','Welfare','Source','JobType','Startdate','Enddate','JobDescription','JobLocation']], axis=1)
        jds.apply(lambda x: self.save_jd(x), axis=1)
        data.apply(lambda x: self.ontology_and_relation(x), axis=1)
        [self.save_to_neo4j('company', x) for x in self.company if not self.if_exists('company', x['_id'])]
        [self.save_to_neo4j('city',x) for x in self.cities if not self.if_exists('city', x)]
        [self.save_to_neo4j('job',x) for x in self.jobs if not self.if_exists('job', x)]
        [self.save_relation(x) for x in self.relations]
        self.cities = []
        self.company = []
        self.relations = []
        self.jobs = []
        return data


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

    def save_jd(self, x):
        if not self.if_exists('jd', x['_id']):
            self.save_to_neo4j('jd', x)

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

    def ontology_and_relation(self, x):
        skills = x.get('skills', [])
        for skill in skills:
            skill_info = searcher.search_skill(skill)
            if not skill_info:
                continue
            self.extract_skill_info(skill_info, x['_id'])
        company = x.get("Company")
        if company:
            self.extract_company_info(company, x['_id'])

        city = x.get("City")
        if city:
            self.extract_city_info(city, x['_id'])

        job = x.get("JobTitle")
        if job:
            self.extract_job_info(city, x['_id'])

    def extract_job_info(self, job_title, jd_id):
        """抽取职位信息

        args:
            job_title: 职位名称
            jd_id:  
        """
        job = {}
        job['_id'] = job_title
        job['name'] = job_title
        self.jobs.append(job)
        relation = {}
        relation['to_id'] = job['_id']
        relation['to_type'] = 'job'
        relation['from_id'] = jd_id
        relation['from_type'] = 'jd'
        relation['name'] = "招聘职位"
        self.relations.append(relation)

    def extract_skill_info(self, skill, jd_id):
        """抽取技能相关关系

        args:
            skill: 技能，字典类型
            jd_id: """

        self.skills.append(skill)
        relation = {}
        relation['to_id'] = skill['_id']
        relation['to_type'] = 'skill'
        relation['from_id'] = jd_id
        relation['from_type'] = 'jd'
        relation['name'] = "涉及"
        self.relations.append(relation)


    def extract_company_info(self, company, jd_id):
        company_info = searcher.search_company(company)
        if company_info:
            company_info['name'] = company
            self.company.append(company_info)
        else:
            company_info = {}
            company_info['name'] = company
            company_info['_id'] = company
            self.company.append(company_info)
        relation = {}
        relation['to_id'] = company_info['_id']
        relation['to_type'] = 'company'
        relation['from_id'] = jd_id
        relation['from_type'] = 'jd'
        relation['name'] = "发布公司"
        self.relations.append(relation)


    def extract_city_info(self, city, jd_id):
        city_info = searcher.search_city(city)
        if city_info:
            city_info['name'] = city
            self.cities.append(city_info)
        else:
            city_info = {}
            city_info['_id'] = city
            city_info['name'] = city
        relation = {}
        relation['to_id'] = city_info['_id']
        relation['to_type'] = 'city'
        relation['from_id'] = jd_id
        relation['from_type'] = 'jd'
        relation['name'] = "工作城市"
        self.relations.append(relation)
