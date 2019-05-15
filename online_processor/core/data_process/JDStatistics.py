from data_access.controller.JDController4Mongo import JDController4Mongo
import re
from services.LinkerService import linkerService
from datetime import datetime
from itertools import groupby
from collections import Counter
from data_access.controller.KBTerminologyController4Mongo import KBTerminologyController4Mongo as TC
import logging

class JDStatistics:
    def __init__(self):
        self.controller = JDController4Mongo()
        self.terminology = dict(linkerService.terminology.name_to_id, **linkerService.terminology.enname_to_id)

    def match_job_title(self,job_title,jd_datas):
        start_time = datetime.now()
        jds = []
        for jd in jd_datas:
            if job_title in jd:
                jds.append()
        end_time = datetime.now()
        print((end_time-start_time).seconds)
        return jds

    def get_jd_statistics_datas(self,jds):
        salary_list =[]
        salary_city = {}   # data format :{city:[salary_list]}
        salary_experience ={}    # data format :{experience:[salary_list]}
        salary_education ={}    # data format :{education:[salary_list]}
        # salary_enterprise_scale ={}

        requirement_city = []
        requirement_experience = []
        requirement_education = []
        #  requirement_enterprise_scale = []

        jd_date = []

        skill = {}   # data format :{terminology_id:freq}

        for jd in jds:
            if jd["Salary"] == "面议":
                salary = None
            elif re.match("([0-9]*)-([0-9]*)",jd["Salary"]):
                salary = sum(list(map(int,jd["Salary"].split("-"))))/2
            elif re.match("([0-9]*)以上",jd["Salary"]):
                salary = int(re.match("([0-9]*)以上",jd["Salary"]).group(1))
            else:
                salary = None

            if jd["Education"][-2:] == "以上":
                jd["Education"] = jd["Education"][:-2]

            if jd["City"][-1:] == "市":
                jd["City"] = jd["City"][:-1]

            if salary != None:
                salary_list.append(salary)
                # 城市薪资分布数据
                if jd["City"] not in salary_city.keys():
                    salary_city[jd["City"]] = [salary]
                else:
                    salary_city[jd["City"]].append(salary)

                # 经验薪资分布数据
                if jd["Experience"] not in salary_experience.keys():
                    salary_experience[jd["Experience"]] = [salary]
                else:
                    salary_experience[jd["Experience"]].append(salary)

                # 学历薪资分布数据
                if jd["Education"] not in salary_education.keys():
                    salary_education[jd["Education"]] = [salary]
                else:
                    salary_education[jd["Education"]].append(salary)

            #需求分布数据
            requirement_city.append(jd["City"])
            requirement_experience.append(jd["Experience"])
            requirement_education.append(jd["Education"])

            #日期数据
            jd_date.append(jd["Startdate"])

            for word in jd["skills"]:
                try:
                    skill_id = self.terminology[word]
                except KeyError:
                    logging.info("Terminology \\{}\\ not in database".format(word))
                    continue
                if skill_id not in skill.keys():
                    skill[skill_id] = 1
                else:
                    skill[skill_id] += 1


            # if jd["EnterpriseScale"] not in enterprise_scale.keys():
            #     education[jd["EnterpriseScale"]] = [salary]
            # else:
            #     education[jd["EnterpriseScale"]].append(salary)

        for skill_key in skill:
            skill[skill_key] = round(skill[skill_key] / len(jds) * 100 ,2)

        jd_statistics_datas = {"salary":{"salary_list":salary_list,
                                         "salary_city":salary_city,
                                         "salary_experience":salary_experience,
                                         "salary_education":salary_education},
                                "trend":jd_date,
                                "requirement":{"requirement_city":requirement_city,
                                               "requirement_experience":requirement_experience,
                                               "requirement_education":requirement_education},
                                "skill":skill}

        return jd_statistics_datas

    def trend(self,jd_date):
        #jd_date = [jd["Startdate"] for jd in jds]
        result = {}
        for jdDate in jd_date:
            year_month = jdDate.strftime("%Y-%m")
            if year_month not in result.keys():
                result[year_month] = 1
            else:
                result[year_month] += 1
        result1 = [{"value":v,"name":k} for k,v in result.items()]
        return result1

    def salary(self,jd_salary:dict):

        salary_freq = [{"value":len(list(g)), "name":"{}k-{}k".format(int(k*10),int(k+1)*10)}
                       for k, g in groupby(sorted(jd_salary["salary_list"]), key=lambda x: (x-1)//10000)]
        try:
            city_salary = [{"value": int(sum(v) / len(v)), "name": k} for k, v in jd_salary["salary_city"].items()]
            experience_salary = [{"value": int(sum(v) / len(v)), "name": k} for k, v in
                                 jd_salary["salary_experience"].items()]
            education_salary = [{"value": int(sum(v) / len(v)), "name": k} for k, v in jd_salary["salary_education"].items()]
        except Exception:
            print(Exception)


        city_salary = sorted(city_salary, key=lambda k: k['value'],reverse=True)[:10]
        experience_salary = sorted(experience_salary, key=lambda k: k['value'], reverse=True)
        education_salary = sorted(education_salary, key=lambda k: k['value'], reverse=True)

        result = {"freq_distribution":salary_freq,
                  "city":city_salary,
                  "experience":experience_salary,
                  "education":education_salary}

        return result

    def requirement(self,jd_requirement:dict):
        city_requirement = [{"value":v,"name":k} for k,v in Counter(jd_requirement["requirement_city"]).items()]
        experience_requirement = [{"value":v,"name":k} for k,v in Counter(jd_requirement["requirement_experience"]).items()]
        education_requirement = [{"value":v,"name":k} for k,v in Counter(jd_requirement["requirement_education"]).items()]

        city_requirement = sorted(city_requirement, key=lambda k: k['value'], reverse=True)
        less_requirement_citys = sum([city["value"] for city in city_requirement[15:]])
        city_requirement = city_requirement[:15]+ [{"value":less_requirement_citys,"name":"其他"}]


        result = {"city": city_requirement,
                  "experience": experience_requirement,
                  "education": education_requirement}

        return result

    def skill(self,jd_skill:dict):
        jd_skill = sorted(zip(jd_skill.values(),jd_skill.keys()),reverse=True)[:10]
        result = [{"value":jdSkill[0],"name":TC().get_data_by_id(_id=jdSkill[1])[0].name} for jdSkill in jd_skill]
        return result

    def statistics_by_jobtitle(self,job_title:str,statistics_time = 6):
        '''

        :param job_title:
        :return:
        {
	    'salary': {
		    'freq_distribution': [{'value': 156,'name': '0k-10k'}],
		    'city': [{'value': 27988,'name': '北京'}],
		    'experience': [{'value': 51363,'name': '10年以上'}],
	    	'education': [{'value': 29576,'name': '博士'}]
    	},
	    'trend': [{'value': 815,'name': '2018-10'}],
	    'requirement': {
	    	'city': [{'value': 1251,'name': '北京'}],
	    	'experience': [{'value': 758,'name': '1-3年'}],
	    	'education': [{'value': 860,'name': '硕士'}]
    	},
	    'skill': [{'value': 4593,'name': 1956}]
        }
        '''

        jd_datas = self.controller.get_datas_by_date_and_jobtitle(job_title=job_title,custom_month=statistics_time)
        statistics_datas = self.get_jd_statistics_datas(jd_datas)

        salary = self.salary(statistics_datas["salary"])
        trend = self.trend(statistics_datas["trend"])
        requirement = self.requirement(statistics_datas["requirement"])
        skill = self.skill(statistics_datas["skill"])

        result = {"salary":salary,
                  "trend":trend ,
                  "requirement":requirement ,
                  "skill":skill}

        return result


if __name__ == "__main__":
    jd_statistics = JDStatistics()
    jobtitle = "机器学习工程师"
    result = jd_statistics.statistics_by_jobtitle(jobtitle)
    print(result)


