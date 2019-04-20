from data_access.controller.CVController4Mongo import CVController4Mongo
from utils.Constants import REGEX_CN
import re
import json
from bson import ObjectId
from core.parser.CVParser import CVParser
from services.NLPService import nlpService
from services.LinkerService import linkerService
from collections import Counter
from utils.Encoder import JSONEncoder

class CVPaint:
    def __init__(self):
        self.cv_controller = CVController4Mongo()
        self.parser = CVParser()

    def year_to_char(self,year):
        if year < 1:
            return "{}个月".format(str(round(year * 12)))
        else:
            return "{}年{}个月".format(str(int(year)),str(round((year - int(year))*12)))

    def conver_null_time(self,start_time,end_time,update_time):
        if start_time == None :
            start_time = update_time
        if end_time == None:
            end_time = update_time
        return start_time ,end_time

    def extract_terminology(self,text):
        stop_words = ['', '\uf06c']
        cn_sentences = nlpService.sentencesize(text)
        cn_words = [word for doc in cn_sentences for word in nlpService.seg_words(doc)]
        cn_skill_words = linkerService.recongnize_terminology(cn_words, 'cn')

        text_en = text.lower()
        text_en = "".join(text_en.split())
        text_en_pure = re.sub("({0}|,|;|，|。|；|\\n'|、)+".format(REGEX_CN), '__', text_en)
        en_words = text_en_pure.split("__")
        en_words = [word for word in en_words if word not in stop_words]
        en_skill_words = linkerService.recongnize_terminology(en_words, 'en')
        skill_words = cn_skill_words + en_skill_words
        return  skill_words

    def data_label(self,cv):
        '''
        :param cv:
        :return:
        '''
        work_experience = cv.workExperience
        education_experiences = cv.educationExperience
        project_experience = cv.projectExperience
        update_time = cv.updateTime

        education_time = []
        work_time = []
        work_time_tuple = []
        education_time_tuple = []

        for educationExperience in education_experiences:
            education_start_time = educationExperience.educationStartTime
            education_end_time = educationExperience.educationEndTime
            education_start_time, education_end__time =self.conver_null_time(education_start_time,education_end_time,update_time)

            education_time_tuple.append((education_start_time, education_end_time))
            education_time.append({"start_time": education_start_time, "end_time": education_end_time})


        for workExperience in work_experience:
            work_start_time = workExperience.workStartTime
            work_end_time = workExperience.workEndTime
            work_start_time, work_end_time = self.conver_null_time(work_start_time,work_end_time,update_time)

            work_time_tuple.append((work_start_time, work_end_time))
            work_time.append({"start_time":work_start_time,"end_time":work_end_time})

        # 工龄
        work_total_time = sum([(i["end_time"]-i["start_time"]).days for i in work_time])/365
        work_total_time_char = self.year_to_char(work_total_time)

        # 跳槽次数
        job_hopping_time = len(work_experience)-1
        job_hopping_time_char = "{0}次".format(str(job_hopping_time))


        # 平均工作经历时间
        job_hopping_freq = work_total_time/len(work_experience)
        job_hopping_freq_char = self.year_to_char(job_hopping_freq)

        #平均工作空档期 最大工作空档期
        if len(work_experience) <= 1:
            job_interval_ave = "-"
            job_interval_max = "-"
        else:
            start_list = [i[0] for i in work_time_tuple][:-1]
            end_list = [i[1] for i in work_time_tuple][1:]
            job_interval_list = [(start_list[i]-end_list[i]).days for i in range(job_hopping_time)]
            job_interval_ave = sum(job_interval_list)/len(job_interval_list)
            job_interval_max = max(job_interval_list)
            job_interval_ave = "{}个月".format(str(round(job_interval_ave/30)))
            job_interval_max = "{}个月".format(str(round(job_interval_max/30)))

        #项目数量
        project_num = "{0}个".format(str(len(project_experience)))


        result = {  "工龄":work_total_time_char,
                    "跳槽次数":job_hopping_time_char,
                    "平均工作经历时间":job_hopping_freq_char,
                    "平均工作空档期":job_interval_ave,
                    "最大工作空档期":job_interval_max,
                    "项目数量":project_num
                    }
        # print(result)
        return result

    def timeline(self, cv):
        '''

        :param cv:
        :return: list
        {"start": startTime, "end": endTime, "activity": "training", "text": text}
        '''
        education_experiences = cv.educationExperience
        work_experience = cv.workExperience
        project_experience = cv.projectExperience
        training_experience = cv.trainingExperience
        update_time = cv.updateTime


        result = []

        for educationExperience in education_experiences:
            start_time = educationExperience.educationStartTime
            end_time = educationExperience.educationEndTime
            start_time,end_time = self.conver_null_time(start_time,end_time,update_time)

            school_name = educationExperience.educationSchool
            major = educationExperience.educationMajor
            degree = educationExperience.educationDegree
            text = degree + "\n" + school_name + "\n" + major
            experience = {"start": start_time, "end": end_time, "activity": "education", "text": text}
            result.append(experience)

        for workExperience in work_experience:
            start_time = workExperience.workStartTime
            end_time = workExperience.workEndTime
            start_time, end_time = self.conver_null_time(start_time, end_time, update_time)

            company = workExperience.workCompany
            position = workExperience.workPosition
            text = company + "\n" + position
            experience = {"start": start_time, "end": end_time, "activity": "work", "text": text}
            result.append(experience)

        for projectExperience in project_experience:
            start_time = projectExperience.projectStartTime
            end_time = projectExperience.projectEndTime
            start_time, end_time = self.conver_null_time(start_time,end_time,update_time)

            project = projectExperience.projectName
            text = project
            experience = {"start": start_time, "end": end_time, "activity": "project", "text": text}
            result.append(experience)

        for trainingExperience in training_experience:
            start_time = trainingExperience.trainingStartTime
            end_time = trainingExperience.trainingEndTime
            start_time, end_time = self.conver_null_time(start_time,end_time,update_time)
            if start_time == update_time and end_time == update_time:
                continue
            training = trainingExperience.trainingCourse
            text = training
            experience = {"start": start_time, "end": end_time, "activity": "training", "text": text}
            result.append(experience)

        # print(result)

        for r in result:
            r["start"].strftime("%Y-%m")
            r["end"].strftime("%Y-%m")

        return result

    def salary_change(self, cv):
        '''

        :param cv:
        :return: dict
        {'companys': ['浙江阿拉丁电子商务股份有限公司', '上海益实多电子商务有限公司'],
         'salarytop': ['10001', '8001'],
         'salarybottom': ['15000', '10000']}
        '''
        work_experience = cv.workExperience
        companys = []
        salary_top = []
        salary_bottom = []

        for workExperience in work_experience:
            company = workExperience.workCompany
            salary = workExperience.workSalary
            if salary == None or salary == "保密":
                top , bottom = "-","-"
            else:
                if re.match("([0-9]*)-([0-9]*)元/月",salary):
                    top =  re.match("([0-9]*)-([0-9]*)元/月",salary).group(1)
                    bottom = re.match("([0-9]*)-([0-9]*)元/月",salary).group(2)
                elif re.match("([0-9]*)元/月 以下",salary):
                    top = re.match("([0-9]*)元/月 以下", salary).group(1)
                    bottom = 0
                elif re.match("([0-9]*)元/月 以上",salary):
                    bottom = re.match("([0-9]*)元/月 以上", salary).group(1)
                    top = bottom + 1000
                else:
                    top, bottom = "-", "-"

            salary_top.append(top)
            salary_bottom.append(bottom)
            companys.append(company)
        result = {"companys":companys , "salarytop":salary_top , "salarybottom":salary_bottom}

        # print(result)
        return result

    def position_background(self, cv):
        '''
        :param cv:
        :return:
        {'industry': [{'value': 595, 'name': '互联网'}], 'positon': [{'value': 412, 'name': '数据处理'}, {'value': 183, 'name': 'java工程师'}]}
        '''
        work_experience = cv.workExperience
        industry_dict = {}
        position_dict = {}
        for workExperience in work_experience:
            industry = workExperience.workCompanyIndustry
            position = workExperience.workPosition
            work_start_time = workExperience.workStartTime
            if workExperience.workEndTime != None:
                work_end_time = workExperience.workEndTime
            else:
                work_end_time = cv.updateTime
            work_days = (work_end_time - work_start_time).days

            if industry not in industry_dict.keys():
                industry_dict[industry] = work_days
            else:
                industry_dict[industry] += work_days

            if position not in position_dict.keys():
                position_dict[position] = work_days
            else:
                position_dict[position]+=work_days

        result = {"industry": [], "positon": []}
        result["industry"] = [{"value": value, "name": name} for name, value in industry_dict.items()]
        result["positon"] = [{"value": value, "name": name} for name, value in position_dict.items()]

        # print(result)
        return result

    def skill_radar(self,cv):

        '''

        :param cv:
        :return:
        '''
        scale_list = {"精通":["精通"],
                      "熟练": ["熟练","熟悉","熟练使用","擅长","深入","熟练掌握"],
                      "掌握": ["能够应用","能够使用","可以","掌握","良好","具备 能力","有 能力"],
                      "了解": ["了解","一般","知道","认识","有 使用经验"]}
        null_result = [
            {'text': '办公软件', 'value': 0},
            {'text': '编程语言', 'value': 0},
            {'text': '数据库', 'value': 0},
            {'text': '算法', 'value': 0},
            {'text': '开发工具', 'value': 0}
        ]

        result = []
        if type(cv.skill) == list:
            for skill in cv.skill:
                skill_words = self.extract_terminology(skill["name"])
                for word in skill_words:
                    if skill["skillMastery"] in scale_list["精通"]:
                        scale_value = 4
                    elif skill["skillMastery"] in scale_list["熟练"]:
                        scale_value = 3
                    elif skill["skillMastery"] in scale_list["掌握"]:
                        scale_value = 2
                    elif skill["skillMastery"] in scale_list["了解"]:
                        scale_value = 1
                    result.append({'text': word, 'value': scale_value})

        elif type(cv.skill) == str:
            result = null_result

        elif cv.skill== None:
            result = null_result

        return result

    def cv_paint(self,cv):
        '''
        :param cv: get from mongodb by id
        :return:
        '''
        cv = self.parser.parse(cv)
        result = {}
        result["data_label"] = self.data_label(cv)
        result["timeline"] = self.timeline(cv)
        result["salary_change"] = self.salary_change(cv)
        result["position_background"] = self.position_background(cv)
        result["skill_radar"] = self.skill_radar(cv)
        result["cv_word_cloud"] = self.term_cloud(cv)[0]
        result["terms_bar"] = self.term_cloud(cv)[1]
        json.dumps(result,cls=JSONEncoder)
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
            all_text.extend([skill["name"] for skill in cv.skill])
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
        text_en_pure = re.sub("({0}|,|;|，|。|；|\\n'|、)+".format(REGEX_CN), '__', text_en)
        en_words = text_en_pure.split("__")
        en_words = [word for word in en_words if word not in stop_words]
        en_skill_words = linkerService.recongnize_terminology(en_words, 'en')
        words = en_words + cn_words
        skill_words = cn_skill_words + en_skill_words
        # return dict(Counter(words)), dict(Counter(skill_words).most_common(10))
        count_words = Counter(words)
        count_skill_words = Counter(skill_words).most_common(10)
        count_words = [{'texts': k, 'weights': v} for k, v in count_words.items()]
        count_skill_words = [{'texts': k, 'weights': v} for k, v in count_skill_words]
        return count_words, count_skill_words



if __name__ == "__main__":
    cv_paint = CVPaint()
    cv = cv_paint.cv_controller.get_data_by_id(_id="N7p7DBeE6lKOrYKUoDC(WA")[0]
    result = cv_paint.cv_paint(cv)
    print(result)


