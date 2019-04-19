from utils.Logger import logging
from data_access.controller.CVController4Mongo import CVController4Mongo
from utils.Constants import REGEX_CN
import re
import json
from bson import ObjectId
import time, datetime
from core.parser.CVParser import CVParser
from core.linker.Linker import Linker
from services.NLPService import nlpService
from services.LinkerService import linkerService
from collections import Counter


class CVPaint:
    def __init__(self):
        self.cv_controller = CVController4Mongo()
        self.parser = CVParser()

    def data_label(self, cv):
        '''

        :param cv:
        :return:
        '''
        work_experience = cv.workExperience
        education_experiences = cv.educationExperience
        update_time = cv.updateTime

        job_interval = 0  # 工作间隔时间
        job_interval_max = 0  # 最大工作间隔时间

        education_time = []
        work_time = []

        for educationExperience in education_experiences:
            education_start_time = educationExperience.educationStartTime
            if educationExperience.educationEndTime != None:
                education_end_time = educationExperience.educationEndTime
            else:
                education_end_time = update_time
            # education_time.append((education_start_time, education_end_time))
            education_time.append({"start_time": education_start_time, "end_time": education_end_time})

        for workExperience in work_experience:
            # time_period = workExperience.workTimePeriod
            work_start_time = workExperience.workStartTime
            if workExperience.workEndTime != None:
                work_end_time = workExperience.workEndTime
            else:
                work_end_time = update_time
            # work_time.append((work_start_time, work_end_time))
            work_time.append({"start_time": work_start_time, "end_time": work_end_time})

        # 工龄
        work_total_time = sum([(i["end_time"] - i["start_time"]).days for i in work_time]) / 365

        # 跳槽次数
        job_hopping_time = len(work_experience) - 1

        # 跳槽频率
        experience_time = max(max(zip(*education_time)[1]), max(zip(*work_time)[1])) - min(
            min(zip(*education_time)[0], min(zip(*work_time)[0])))
        for educationTime in education_time:
            print(educationTime)

        # job_hopping_freq = total_time

        # 工作时间间隔

    def timeline(self, cv):
        '''

        :param cv:
        :return: list
        {"start": startTime, "end": endTime, "experience": "training", "text": text}
        '''
        education_experiences = cv.educationExperience
        work_experience = cv.workExperience
        project_experience = cv.projectExperience
        training_experience = cv.trainingExperience
        # publish_paper = cv.publishPaper
        # publish_pook = cv.publishBook
        # publish_patent = cv.publishPatent
        # award = cv.award
        # certificate = cv.certificate

        result = []

        for educationExperience in education_experiences:
            start_time = educationExperience.educationStartTime
            end_time = educationExperience.educationEndTime
            school_name = educationExperience.educationSchool
            major = educationExperience.educationMajor
            degree = educationExperience.educationDegree
            text = degree + "\n" + school_name + "\n" + major
            experience = {"start": start_time, "end": end_time, "experience": "education", "text": text}
            result.append(experience)

        for workExperience in work_experience:
            start_time = workExperience.workStartTime
            end_time = workExperience.workEndTime
            company = workExperience.workCompany
            position = workExperience.workPosition
            text = company + "\n" + position
            experience = {"start": start_time, "end": end_time, "experience": "work", "text": text}
            result.append(experience)

        for projectExperience in project_experience:
            start_time = projectExperience.projectStartTime
            end_time = projectExperience.projectEndTime
            project = projectExperience.projectName
            text = project
            experience = {"start": start_time, "end": end_time, "experience": "project", "text": text}
            result.append(experience)

        for trainingExperience in training_experience:
            start_time = trainingExperience.trainingStartTime
            end_time = trainingExperience.trainingEndTime
            training = trainingExperience.trainingCourse
            text = training
            experience = {"start": start_time, "end": end_time, "experience": "training", "text": text}
            result.append(experience)

        return result

    def salary_change(self, cv):
        '''

        :param cv:
        :return: dict
        '''
        work_experience = cv.workExperience
        companys = []
        salary_top = []
        salary_bottom = []

        for workExperience in work_experience:
            company = workExperience.workCompany
            salary = workExperience.workSalary
            if salary == None:
                top, bottom = "-", "-"
            elif salary == "":
                top, bottom = "-", "-"
            elif salary == "":
                top, bottom = "-", "-"
            salary_top.append(top)
            salary_bottom.append(bottom)
            companys.append(company)
        result = {"companys": companys, "salarytop": salary_top, "salarybottom": salary_bottom}
        return result

    def position_background(self, cv):
        '''

        :param cv:
        :return:
        data: [
            {value: 335, name: '直达'},
            {value: 679, name: '营销广告'},
            {value: 1548, name: '搜索引擎'}]
        '''
        work_experience = cv.workExperience
        industry_dict = {}
        position_dict = {}
        for workExperience in work_experience:
            industry = workExperience.workCompanyIndustry
            position = workExperience.workPosition
            time = workExperience.workTimePeriod
            # startTime = workExperience.workStartTime
            # endTime = workExperience.workEndTime
            year = re.search("([0-9]*)年([0-9]*)个月", time).group(1)
            mouth = re.search("([0-9]*)年([0-9]*)个月", time).group(2)
            work_time = int(year) + int(mouth) / 12
            if industry not in industry_dict.keys():
                industry_dict[industry] = work_time
            else:
                industry_dict[industry] += work_time
            if position not in position_dict.keys():
                position_dict[position] = work_time
            else:
                position_dict[position] += work_time
        result = {"industry": [], "positon": []}
        result["industry"] = [{"value": value, "name": name} for name, value in industry_dict.items()]
        result["positon"] = [{"value": value, "name": name} for name, value in position_dict.items()]

        return result

    def skill_radar(self, cv):
        '''

        :param cv:
        :return:
        '''

    def cv_word_cloud(self, cv):
        '''

        :param cv:
        :return:
        '''

    def terms_bar(self, cv):
        '''

        :param cv:
        :return:
        '''

    def cv_paint(self, cv):
        result = {}
        result["data_label"] = self.data_label(cv)
        result["timeline"] = self.timeline(cv)
        result["salary_change"] = self.salary_change()
        result["position_background"] = self.position_background()
        result["skill_radar"] = self.skill_radar()
        result["cv_word_cloud"] = self.cv_word_cloud()
        result["terms_bar"] = self.terms_bar()
        json.dumps(result)
        return result

    def term_cloud(self, cv):
        link_dict = {'educationExperience': ['educationMajorDescription'],
                     'workExperience': ['workDescription', 'workDuty', 'workSummary'],
                     'projectExperience': ['projectName', 'projectDuty', 'projectSummary'],
                     'trainingExperience': ['trainingCourse', 'trainingDescription'],
                     'associationExperience': ['practiceName', 'practiceDescription']}
        all_text = [
            # cv.__dict__[column] for column in link_list
            cv.selfEvaluation
        ]
        if type(cv.skill) == list:
            all_text.extend(cv.skill)
        elif type(cv.skill) == str:
            all_text.append(cv.skill)

        for k, v in link_dict.items():
            all_text.extend([exprience.__dict__[column] for column in v for exprience in cv.__dict__[k]])
        all_text = ".".join(all_text)
        stop_words = ['', '\uf06c']
        cn_sentences = nlpService.sentencesize(all_text)
        cn_words = [word for doc in cn_sentences for word in nlpService.seg_words(doc)]
        cn_skill_words = linkerService.recongnize_terminology(cn_words, 'cn')

        text_en = all_text.lower()
        text_en = "".join(text_en.split())
        text_en_pure = re.sub("({0}|,|;|，|。|；|\.|\\n')+".format(REGEX_CN), '__', text_en)
        en_words = text_en_pure.split("__")
        en_words = [word for word in en_words if word not in stop_words]
        en_skill_words = linkerService.recongnize_terminology(en_words, 'en')
        words = en_words + cn_words
        skill_words = cn_skill_words + en_skill_words
        return Counter(words), Counter(skill_words)


if __name__ == "__main__":
    controller = CVController4Mongo()
    cv = controller.get_data_by_id(_id=ObjectId("5cb718c192a9e90c4f81fe03"))[0]
    cv_paint = CVPaint()
    cv = cv_paint.parser.parse(cv)
    # cv_paint.data_label(cv)
    # testtime = cv.workExperience[0].workStartTime
    # print(testtime.timetuple().tm_year)
    print(cv_paint.term_cloud(cv))

    # print(cvpaint.data_label())
