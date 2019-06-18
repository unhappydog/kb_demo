from data_access.controller.PositionController import PositionController
from data_access.models.Position import Position
from services.LinkerService import linkerService
import math
import re


class PersonJobFit:

    def __init__(self):
        self.controller = PositionController()

    def score(self,cv, position):

        # import pdb; pdb.set_trace()

        score = 0
        #score education 10
        cv_education = cv.highestEducationDegree
        position_education = position['education']
        education_score = self.score_education(cv_education, position_education)
        score += education_score *5

        #score education experiences 10
        cv_education_experience = cv.educationExperience
        education_experience_score = self.score_education_experience(cv_education_experience)
        score += education_experience_score *5

        #score experience 10
        cv_work_experience = cv.workYear
        position_work_experience = position['workYear']
        work_experience_score = self.score_work_experience(cv_work_experience, position_work_experience)
        score += work_experience_score *5

        #score skill 60
        cv_skill_tags = linkerService.gen_skill_tag(cv)
        position_skill_tags = self._extract_skills_from_position(position)
        work_skill_score = self.score_skill(cv_skill_tags, position_skill_tags)
        score += 60 * work_skill_score

        #score project 10
        cv_project_experience = cv.projectExperience
        position_project_experience = position['workDescription']
        project_experience_score = self.score_project_experience(cv_project_experience, position_project_experience)
        if project_experience_score >= 10:
            project_experience_score = 10
        score  += project_experience_score

        #score company 5
        score +=5

        #scre risk 10
        cv_risk = linkerService.risk_recongnize(cv)
        risk_score = self.score_risk(cv_risk)
        score += risk_score * 2

        #score_location 5
        cv_location = cv.expectedWorkplace
        position_location = position['workCity']
        location_score = self.score_location(cv_location, position_location)
        score += location_score *5

        #score age 5
        cv_age = cv.age
        age_score = self.score_age(cv_age)
        score += age_score *5

        #score salary 5
        cv_salary = cv.expectedSalary
        position_salary = position['salary']
        salary_score = self.score_salary(cv_salary, position_salary)
        score += salary_score *5

        #score industry
        score = int(score)
        if score <= 0:
            score =0
        elif score >=95:
            score = 95

        return score
        pass

    def score_education(self,cv_education, position_education):
        education_embed= {
            "不限":-1,
            "专科":0,
            "本科":1,
            "硕士":2,
            "博士":3
        }
        if education_embed.get(cv_education, -0.5) >= education_embed.get(position_education, 0):
            return 1
        else:
            return 0
        pass


    def score_education_experience(self, cv_education_experience):
        if not cv_education_experience:
            return 0
        for education_experience in cv_education_experience:
            if education_experience.educationNature == "统招":
                return 1
        return 0
    def score_work_experience(self,cv_work_experience, position_work_experience):
        if re.match('[0-9]{1,3}-[0-9]{1,3}年', position_work_experience):
            min_year, max_year = position_work_experience.strip("年").split('-')
            min_year, max_year = int(min_year), int(max_year)
            cv_work_experience = int(cv_work_experience)
            if cv_work_experience <= max_year and cv_work_experience >= min_year:
                return (cv_work_experience - min_year)/(max_year - min_year) + 1
        return 0

    def score_skill(self,cv_skill, position_skill):
        if not cv_skill or not position_skill:
            return 0
        a , b, c = set(cv_skill) & set(position_skill), set(position_skill), set(cv_skill + position_skill)
        return len(a) /len(b)

    def score_project_experience(self,cv_project_experience, position_project_experience):
        return len(cv_project_experience)

    def score_company(self,cv_company):
        return 0

    def score_risk(self,cv_risk):
        return -len(cv_risk)

    def score_location(self,cv_location, position_location):
        if not position_location:
            return 0
        if position_location in cv_location:
            return 1
        else:
            return 0
        pass

    def score_age(self,cv_age):
        if cv_age >= 35:
            return -1
        else:
            return 0
        pass

    def score_salary(self,cv_salary, position_salary):
        min_cv_salary, max_cv_salary = self._convert_salary(cv_salary)
        min_position_salary, max_position_salary = self._convert_salary(position_salary)
        if min_cv_salary < max_position_salary:
            if max_cv_salary < max_position_salary:
                return 2
            else:
                return 1
        else:
            return -1

    def score_industry(self,cv_industry, position_industry):
        return 0
        pass

    def _convert_salary(self, salary):
        if re.match("[0-9]{1,10}-[0-9]{1,10}元\/月", salary):
            min_salary, max_salary = salary[:-3].split('-')
        elif re.match("[0-9]{1,10}-[0-9]{1,10}", salary):
            min_salary, max_salary = salary.split('-')
        else:
            return 0,0
        min_salary, max_salary = int(min_salary), int(max_salary)
        return min_salary, max_salary

    def _extract_skills_from_position(self, position):
        result = []
        des = position['workDescription']
        req = position['jobRequirement']
        des = des if des else ""
        req = req if req else ""
        result = linkerService.gen_skill_tag_from_text(des) + linkerService.gen_skill_tag_from_text(req)
        return result
