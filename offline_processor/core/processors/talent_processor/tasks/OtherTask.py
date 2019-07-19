from core.processors.news_processor import newsProcessor
from core.base.BaseTask import BaseTask
from core.processors.talent_processor import talentProcessor
from data_access.controller.CommonController4Mongo import CommonController4Mongo
from services.tool_services.neo_service import NeoService
from utils.Constants import is_bad_column, is_replicate_column, cv_label
from utils.Logger import logging
from core.linker.Searcher import Searcher
from core.linker.TerminologyLinker import TerminologyLinker
from core.common.mixins.Neo4jMixin import Neo4jMixin
import pandas as pd
import re
from services.AimlService import aimlService
from utils.Utils import update_add_dict

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
class ExtractTask(BaseTask, Neo4jMixin):
    def __init__(self):
        self.company = []
        self.skills = []
        self.relations = []
        self.cities = []
        self.jobs = []
        self.majors = []
        self.neoService = neoService

    def fit(self, data):
        data = data[data.apply(lambda x: x[is_bad_column] ==0 and x[is_replicate_column] ==0 , axis=1)]
        jds = data.apply(lambda x: x[['_id', 'Name', 'Company','Salary','City','Education','Number','Welfare','Source','JobType','Startdate','Enddate','JobDescription','JobLocation']], axis=1)
        jds['name'] = jds['Name']
        jds.apply(lambda x: self.save_jd(x), axis=1)
        data.apply(lambda x: self.ontology_and_relation(x), axis=1)
        [self.save_to_neo4j('company', x) for x in self.company if not self.if_exists('company', x['_id'])]
        [self.save_to_neo4j('city',x) for x in self.cities if not self.if_exists('city', x['_id'])]
        [self.save_to_neo4j('job',x) for x in self.jobs if not self.if_exists('job', x['_id'])]
        [self.save_to_neo4j('major', x) for x in self.majors if not self.if_exists('major', x['_id'])]
        # import ipdb; ipdb.set_trace()


        [self.save_relation(x) for x in self.relations]
        self.cities = []
        self.company = []
        self.relations = []
        self.jobs = []
        self.majors = []
        return data

    def save_jd(self, x):
        if not self.if_exists('jd', x['_id']):
            self.save_to_neo4j('jd', x)

    def ontology_and_relation(self, x):
        # import ipdb; ipdb.set_trace()

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

        jobs = x.get("JobTitle", [])

        jobs = list(set(jobs))
        if jobs:
            for job in jobs:
                self.extract_job_info(job, x['_id'])

        describe = x.get("JobDescription")
        if describe:
            self.extract_describe_info(describe, x['_id'])

    def extract_describe_info(self, describe, jd_id):
        des = describe
        des_list = re.split("。|;|；|\n|[0-9]{1,2}(， |\.|。|;|；|:|：| |、|,)", des.strip())
        pattern_name_list = ["工作职责", "优先条件", "教育背景", "经验要求", "加分项"]
        temp = {}
        for doc in des_list:
            if not doc or len(doc) <= 4:
                continue
            info = aimlService.parse_info(doc)
            temp = update_add_dict(temp, info)
        result = temp.get("教育")
        if result:
            major = temp.get("专业")
            if major:
                major_info = searcher.search_major(major)
                if major_info:
                    self.majors.append(major_info)
                else:
                    major_info = {}
                    major_info['_id'] = major
                    major_info['name'] = major
                    self.majors.append(major_info)
                relation = {}
                relation['to_id'] = major_info['_id']
                relation['to_type'] = 'major'
                relation['from_id'] = jd_id
                relation['from_type'] = 'jd'
                relation['name'] = "专业要求"
                self.relations.append(relation)

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
        relation['name'] = "技能要求"
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
