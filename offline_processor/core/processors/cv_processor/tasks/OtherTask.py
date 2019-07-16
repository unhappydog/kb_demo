from core.processors.cv_processor import cvProcessor
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


neoService = NeoService.instance()
searcher = Searcher.instance()
@cvProcessor.add_as_processors(order=11, stage=2, schema='kb_demo', table='kb_talent_bank')
class SaveTask(BaseTask):
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.controller = CommonController4Mongo(schema, table)

    def fit(self, data):
        self.controller.insert_datas_from_df(data)
        return data

@cvProcessor.add_as_processors(order=12, stage=2, schema='kb_demo', table='kb_project_experience')
class ExtractProjectExperience(BaseTask):
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        self.controller = CommonController4Mongo(schema, table)
        self.experience = []

    def fit(self, data):
        data.apply(lambda x: self.extract_experience(x), axis=1)
        experiences = pd.DataFrame(self.experience)
        self.controller.insert_datas_from_df(experiences)
        self.experience = []
        return data

    def extract_experience(self, data):
        projectExperiences = data['projectExperience']
        keyword = data['keyword']
        workExperiences = data['workExperience']
        company_map = {}
        if workExperiences:
            for workExperience in workExperiences:
                company_map[workExperience['workCompany']] = {}
                if workExperience['workEndTime'] is None or workExperience['workEndTime'] == "":
                    end = datetime.datetime.now()
                else:
                    end = workExperience.get('workEndTime')
                start = workExperience.get('workStartTime')
                company_map[workExperience['workCompany']]['end'] = end
                company_map[workExperience['workCompany']]['start'] = start
        else:
            pass
        if projectExperiences:
            count = 0
            for projectExperience in projectExperiences:
                count +=1
                temp = {}
                temp['_id'] = str(data['_id']) + str(count)
                temp['projectStartTime'] = projectExperience['projectStartTime']
                temp['projectEndTime'] = projectExperience['projectEndTime']
                temp['projectName'] = projectExperience['projectName']
                temp['projectTimePeriod'] = projectExperience['projectTimePeriod']
                temp['projectDuty'] = projectExperience.get('projectDuty','')
                temp['projectDescription'] = projectExperience['projectDescription']
                start = projectExperience['projectStartTime']
                temp['keyword'] = keyword
                if temp['projectEndTime'] is None or temp['projectEndTime'] == "":
                    end = datetime.datetime.now()
                else:
                    end = temp['projectEndTime']
                for company, v in company_map.items():
                    if v['start'] <= start and v['end']>=end:
                        temp['company'] = company
                self.experience.append(temp)

@cvProcessor.add_as_processors(order=13, stage=2)
class ExtractTask(BaseTask, Neo4jMixin):
    def __init__(self):
        self.company = []
        self.schools = []
        self.relations = []
        self.project = []
        self.majors = []
        self.skills = []
        self.cities = []
        self.jobs = []
        self.terminology_linker = TerminologyLinker()
        self.neoService = neoService

    def fit(self, data):
        data = data[data.apply(lambda x: x[is_bad_column] ==0 and x[is_replicate_column] ==0 , axis=1)]
        persons = data.apply(lambda x: x[['name','gender','age','birthday','workYear','highestEducationDegree','marital','currentAddress','domicilePlace','politicsStatus','expectedWorkplace','_id']], axis=1)
        persons.apply(lambda x: self.save_person(x), axis=1)
        data.apply(lambda x: self.ontology_and_relation(x), axis=1)

        temp = [self.save_to_neo4j('school', x) for x in self.schools if not self.if_exists('school', x['_id'])]
        temp = [self.save_to_neo4j('company', x) for x in self.company if not self.if_exists('company', x['_id'])]
        [self.save_to_neo4j('project',x) for x in self.project if not self.if_exists('project', x['_id'])]
        [self.save_to_neo4j('skill',x) for x in self.skills if not self.if_exists('skill', x['_id'])]
        [self.save_to_neo4j('city', x) for x in self.cities if not self.if_exists('city', x['_id'])]
        [self.save_to_neo4j('job', x) for x in self.jobs if not self.if_exists('job', x['_id'])]
        [self.save_to_neo4j('major',x) for x in self.majors if not self.if_exists('major', x['_id'])]
        [self.save_relation(x) for x in self.relations]
        self.schools = []
        self.company = []
        self.project = []
        self.relations = []
        self.skills = []
        self.cities = []
        self.majors = []
        return data

    def save_person(self, x):
        if not self.if_exists('candidate', x['_id']):
            self.save_to_neo4j('candidate', x)

    def ontology_and_relation(self, x):
        education_experiences = x.get('educationExperience',[])
        update_time = x.get('updateTime', None)
        for education_experience in education_experiences:
            self.extract_education_info(education_experience, x['_id'], update_time)
            major = education_experience.get('educationMajor')
            if major:
                self.extract_major_info(major, x['_id'])

        work_experiences = x.get('workExperience',[])
        for work_experience in work_experiences:
            self.extract_company_info(work_experience, x['_id'], update_time)
            if not (work_experience.get('workEndTime', None) or work_experience.get('workEndTime', None) == update_time):
                if_now_position = True 
            else:
                if_now_position = False 
            position = work_experience.get('workPosition',None)
            if position:
                self.extract_job_info(position, x['_id'], if_now_position)

        project_experiences = x.get('projectExperience',[])
        for project_experience in project_experiences:
            self.extract_project_info(project_experience, x['_id'])

        skills = x.get('skill', [])
        if type(skills) == str:
            skill_tags = self.terminology_linker.simple_word_linker(skills)
            for skill in skills:
                self.extract_skill_info(skill, x['_id'])
        for skill in skills:
            skill_tags = self.terminology_linker.simple_word_linker(skill['name'])
            skill_tags = [skill_tag['terminology_detail'] for skill_tag in skill_tags]
            mastery = skill.get('skillMastery','涉及')
            for skill_tag in skill_tags:
                self.extract_skill_info(skill_tag, x['_id'], mastery)

        # skills = self.terminology_linker.skill_tags(x)
        # for skill in skills:
        #     self.extract_skill_info(skill, x['_id'])

        city = x.get("currentAddress")
        cities = city.split(" ")
        for city in cities:
            city_info = searcher.search_city(city)
            if city_info:
                city_info['name'] = city
                self.extract_city_info(city_info, x['_id'])


    def extract_major_info(self,major, cv_id):
        major_info = searcher.search_major(major)
        if not major_info:
            major_info = {}
            major_info['_id'] = major
            major_info['name'] = major
        self.majors.append(major_info)
        relation = {}
        relation['to_id'] = major_info['_id']
        relation['to_type'] = 'major'
        relation['from_id'] = cv_id
        relation['from_type'] = 'candidate'
        relation['name'] = "就读专业"
        self.relations.append(relation)

    def extract_job_info(self, position, cv_id, if_now_posisiton=False):
        if not re.match("^.*(师|主管|科学家|经理|专员)$", position):
            position_info = commonDataService.keyword_to_job(position)
            if position_info:
                position = position_info[0]
            else:
                return
        job = {}
        job['_id'] = position
        job['name'] = position
        self.jobs.append(job)
        relation = {}
        relation['to_id'] = job['_id']
        relation['to_type'] = 'job'
        relation['from_id'] = cv_id
        relation['from_type'] = 'candidate'
        if if_now_posisiton:
            relation['name'] = '现任职位'
        else:
            relation['name'] = "曾任职位"
        self.relations.append(relation)

    def extract_city_info(self,city_info, cv_id):
        self.cities.append(city_info)
        relation = {}
        relation['to_id'] = city_info['_id']
        relation['to_type'] = 'city'
        relation['from_id'] = cv_id
        relation['from_type'] = 'candidate'
        relation['name'] = "现居地"
        self.relations.append(relation)

    def extract_skill_info(self, skill, cv_id, mastery = '涉及'):
        """抽取技能相关关系

        args:
            skill: 技能字典
            cv_id: 简历id"""
        self.skills.append(skill)
        relation = {}
        relation['to_id'] = skill['_id']
        relation['to_type'] = 'skill'
        relation['from_id'] = cv_id
        relation['from_type'] = 'candidate'
        relation['name'] = mastery
        self.relations.append(relation)


    def extract_education_info(self, education_experience, cv_id, update_time):
        """抽取教育相关关系

        根据学校名抽取专业相关内容

        Args:
          education: 学校名称
          cv_id: 简历id
          update_time: 简历更新时间
        """
        school = education_experience.get('educationSchool')
        if not school:
            print(cv_id)
            return

        school_info = searcher.search_academy(school)
        if school_info:
            school_info['name'] = school
            self.schools.append(school_info)
            relation = education_experience
            relation['to_id'] = school_info['_id']
            relation['to_type'] = 'school'
            relation['from_id'] = cv_id
            relation['from_type'] = 'candidate'
        else:
            school_info = {}
            school_info['name'] = school
            school_info['_id'] = school
            self.schools.append(school_info)
            relation = education_experience
            relation['to_id'] = school_info['_id']
            relation['to_type'] = 'school'
            relation['from_id'] = cv_id
            relation['from_type'] = 'candidate'
        if not (education_experience.get('educationEndTime', None) or education_experience.get('educationEndTime', None) == update_time):
            relation['name'] = '就读于'
        else:
            relation['name'] = '毕业于'
        self.relations.append(relation)

    def extract_company_info(self, work_experience, cv_id, update_time):
        """抽取公司相关关系

        Args:
            company: 公司名称
            cv_id: 简历id"""

        company = work_experience['workCompany']
        company_info = searcher.search_company(company)
        if company_info:
            company_info['name'] = company
            self.company.append(company_info)
            relation = work_experience
            relation['to_id'] = company_info['_id']
            relation['to_type'] = 'company'
            relation['from_id'] = cv_id
            relation['from_type'] = 'candidate'
        else:
            company_info = {}
            company_info['name'] = company
            company_info['_id'] = company
            self.company.append(company_info)
            relation = work_experience
            relation['to_id'] = company_info['_id']
            relation['to_type'] = 'company'
            relation['from_id'] = cv_id
            relation['from_type'] = 'candidate'
        if not (work_experience.get('workEndTime', None) or work_experience.get('workEndTime', None) == update_time):
            relation['name'] = '现就职于'
        else:
            relation['name'] = '曾就职于'
        self.relations.append(relation)

    def extract_project_info(self, project_experience, cv_id):
        project = project_experience['projectName']
        project_info = searcher.search_project(project)
        if project_info:
            project_info['name'] = project
            self.project.append(project_info)
            relation = project_experience
            relation['to_id'] = project_info['_id']
            relation['to_type'] = 'project'
            relation['from_id'] = cv_id
            relation['from_type'] = 'candidate'
            if 'company' not in project_info.keys():
                return
            company = project_info['company']
            company_info = searcher.search_company(company)
            if not company_info:
                return
            work_relation = {}
            work_relation['to_id'] = company_info['_id']
            work_relation['to_type'] = 'company'
            work_relation['from_id'] = project_info['_id']
            work_relation['from_type'] = 'project'
            work_relation['name'] = '项目公司'
            self.relations.append(work_relation)
        else:
            project_info = {}
            project_info['name'] = project
            project_info['_id'] = project
            self.project.append(project_info)
            relation = project_experience
            relation['to_id'] = project_info['_id']
            relation['to_type'] = 'project'
            relation['from_id'] = cv_id
            relation['from_type'] = 'candidate'
        relation['name'] = '参与'
        self.relations.append(relation)
