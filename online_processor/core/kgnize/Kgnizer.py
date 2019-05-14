from core.kgnize.KgPropertyList.KgPropertyList import KgPropertyList


class Kgnizer:
    def __init__(self):
        self.name = "kgnizer"
        self.link_dict = {'educationExperience': ['educationMajorDescription'],
                          'workExperience': ['workDescription', 'workDuty', 'workSummary'],
                          'projectExperience': ['projectName', 'projectDuty', 'projectSummary'],
                          'trainingExperience': ['trainingCourse', 'trainingDescription'],
                          'associationExperience': ['practiceName', 'practiceDescription']}
        # self.all_skills = []

    def kgnize(self, cv, link_text, link_academy={}, link_company={}):
        """
        简历数据图谱化
        :param cv:
        :param link_text:
        :param link_academy:
        :param link_company:
        :return:
        """
        cv_kg = {
            'name': cv.name,
            '基础信息': {
                '年龄': cv.age,
                '学历': cv.highestEducationDegree,
                '工作年限': cv.workYear,
                '邮箱': cv.email,
                '婚姻状况': cv.marital
            },
            '求职意向': {
                '求职职位': cv.expectedOccupation,
                '期望薪资': cv.expectedSalary,
                '从事行业': cv.expectedIndustry
            },
            '教育经历':
                self.process_education_experience(cv.educationExperience, link_academy)
            ,
            '工作经历':
                self.process_work_experience(cv.workExperience, link_text['workExperience'], link_company)
            ,
            '项目经历':
                self.process_project_experience(cv.projectExperience, link_text['projectExperience'])
            ,
            '技能':
                self.process_skill(cv.skill)
            ,
            '其它能力': {
                '培训': cv.trainingExperience,
                '语言能力': cv.language,
                '获奖': cv.award,
                '文章': cv.publishPaper,
                '专利': cv.publishPatent,
                '著作': cv.publishBook,
                '证书': cv.certificate,
                '爱好特长': cv.hobby
            }
        }
        all_skills = self.get_all_skills_from(link_text)
        all_skills = self.distinct_termnologys(all_skills)

        tempset = set()
        for termnology in all_skills:
            if termnology.get('cnName'):
                name = termnology['cnName'][0]
            else:
                name = termnology['engName'][0]
            mastery = "涉及过"
            if name.lower() in tempset:
                continue
            cv_kg["技能"].append({
                "术语": name,
                "程度": mastery,
                '悬浮': termnology
            })
            tempset.add(name.lower())
        self.remove_null(cv_kg)
        return cv_kg

    def process_education_experience(self, educationExperiences, linked_academy):
        result = {}
        for educationExperience in educationExperiences:
            name = educationExperience.educationSchool
            major = educationExperience.educationMajor
            degree = educationExperience.educationDegree
            start_time = educationExperience.educationStartTime
            end_time = educationExperience.educationEndTime
            result[degree] = {
                '学校名称': name,
                '专业': major,
                '开始时间': start_time,
                '结束时间': end_time,
            }
            if name in linked_academy.keys():
                result[degree]['悬浮'] = linked_academy[name]
        return result

    def process_work_experience(self, workExperiences, linked_experiences, link_company):
        result = []
        experiences_and_linked_info = zip(workExperiences, linked_experiences)
        for workExperience, linked_experience in experiences_and_linked_info:
            name = workExperience.workCompany
            position = workExperience.workPosition
            start_time = workExperience.workStartTime
            end_time = workExperience.workEndTime
            salary = workExperience.workSalary
            industry = workExperience.workCompanyIndustry
            linked_columns = self.link_dict['workExperience']
            termnologys = self.extract_termnologys_from_linked_experiences(linked_columns, linked_experience)
            temp_info = {"职位": position,
                         "公司名称": name,
                         "开始时间": start_time,
                         "结束时间": end_time,
                         "薪资": salary,
                         "行业": industry,
                         "术语": termnologys}
            if name in link_company.keys():
                temp_info["悬浮"] = link_company[name]
            result.append(
                temp_info
            )

        return result

    def process_project_experience(self, projectExperiences, linked_experiences):
        result = []
        experience_and_linked_info = zip(projectExperiences, linked_experiences)
        for projectExperience, linked_experience in experience_and_linked_info:
            start_time = projectExperience.projectStartTime
            end_time = projectExperience.projectEndTime
            name = projectExperience.projectName
            linked_columns = self.link_dict['projectExperience']
            termnologys = self.extract_termnologys_from_linked_experiences(linked_columns, linked_experience)
            result.append({
                "项目名称": name,
                "开始时间": start_time,
                "结束时间": end_time,
                "术语": termnologys
            })
        return result

    def process_skill(self, skill):
        result = []
        if type(skill) == str:
            skills = skill.split(';')
            for _skill in skills:
                names, mastery = _skill.split(':')
                names = names.split(',')
                _skills_one_mastery = [{
                    "程度": mastery,
                    '术语': name
                } for name in names]
                result.extend(_skills_one_mastery)
        else:
            for _skill in skill:
                result.append({
                    "术语": _skill.name,
                    "程度": _skill.skillMastery
                })
        return result

    def extract_termnologys_from_linked_experiences(self, linked_columns, linked_experience):
        termnologys = [
            [termnology['terminology_detail'] for termnology in linked_experience[linked_column]] for linked_column in
            linked_columns
        ]
        termnologys = [termnology for termnology_in_one_column in termnologys for termnology in
                       termnology_in_one_column]

        # self.all_skills.extend(termnologys)
        termnologys = self.distinct_termnologys(termnologys)
        result = []
        for termnology in termnologys:
            if termnology.get('cnName'):
                name = termnology['cnName'][0]
            else:
                name = termnology['engName'][0]
            result.append({
                "术语": name,
                "悬浮": termnology
            })

        return result
        # return self.distinct_termnologys(termnologys)

    def distinct_termnologys(self, termnologys):
        name_set = set()

        def if_exists(name):
            name = name['_id']
            if name in name_set:
                return False
            else:
                name_set.add(name)
                return True

        return list(filter(if_exists, termnologys))

    def get_all_skills_from(self, link_text):
        result = []
        for experience_name in self.link_dict.keys():
            experiences_linked = link_text[experience_name]
            for experience in experiences_linked:
                for column in self.link_dict[experience_name]:
                    result.extend(experience[column])

        result = [experience['terminology_detail'] for experience in result]
        # result.append(link_text[experience][column])
        return result

    def json_to_4tupe(self, kg_cv):
        kg_property_list = KgPropertyList()
        root_id = kg_property_list.push_property(kg_cv['name'])
        for base_property in kg_cv.keys():
            if base_property == 'name':
                continue
            property_id = kg_property_list.push_property(base_property)
            kg_property_list.push_path(property_id, root_id, '', None)
            if base_property == "基础信息":
                for child_propery, child_value in kg_cv[base_property].items():
                    child_propery_id = kg_property_list.push_property(child_value)
                    kg_property_list.push_path(child_propery_id, property_id, child_propery, None)
            elif base_property == "求职意向":
                for child_propery, child_value in kg_cv[base_property].items():
                    child_propery_id = kg_property_list.push_property(child_value)
                    kg_property_list.push_path(child_propery_id, property_id, child_propery, None)
            elif base_property == "教育经历":
                for child_propery, child_value in kg_cv[base_property].items():
                    child_propery_id = kg_property_list.push_property(child_value['学校名称'])
                    kg_property_list.push_path(child_propery_id, property_id, child_propery,
                                               child_value.get('悬浮', None))
                    for child_propery_1, child_value_1 in child_value.items():
                        if child_propery_1 == "悬浮":
                            continue
                        child_propery_id_1 = kg_property_list.push_property(child_value_1)
                        kg_property_list.push_path(child_propery_id_1, child_propery_id, child_propery_1, None)
            elif base_property == "工作经历":
                for experience in kg_cv[base_property]:
                    child_propery_id = kg_property_list.push_property(experience['公司名称'])
                    kg_property_list.push_path(child_propery_id, property_id, '', experience.get('悬浮', None))
                    for child_propery_1, child_value_1 in experience.items():
                        if child_value_1 == "" or child_value_1 is None:
                            continue
                        if type(child_value_1) == str and child_value_1.strip() == "":
                            continue
                        if child_propery_1 == "悬浮":
                            continue
                        if child_propery_1 != "术语":
                            child_propery_id_1 = kg_property_list.push_property(child_value_1)
                            kg_property_list.push_path(child_propery_id_1, child_propery_id, child_propery_1, None)
                        else:
                            if len(child_value_1)>=1:
                                child_propery_id_1 = kg_property_list.push_property("术语")
                                kg_property_list.push_path(child_propery_id_1, child_propery_id, child_propery_1, None)
                            for termnolgoy in child_value_1:
                                child_propery_id_2 = kg_property_list.push_property(termnolgoy['术语'])
                                kg_property_list.push_path(child_propery_id_2, child_propery_id_1, '',
                                                           termnolgoy.get('悬浮', None))
            elif base_property == "项目经历":
                for experience in kg_cv[base_property]:
                    child_propery_id = kg_property_list.push_property(experience['项目名称'])
                    kg_property_list.push_path(child_propery_id, property_id, '', None)
                    for child_propery_1, child_value_1 in experience.items():
                        if child_propery_1 == "悬浮" or child_value_1 == "" or child_value_1 is None:
                            continue
                        if type(child_value_1) == str and child_value_1.strip() == "":
                            continue
                        if child_propery_1 != "术语":
                            child_propery_id_1 = kg_property_list.push_property(child_value_1)
                            kg_property_list.push_path(child_propery_id_1, child_propery_id, child_propery_1, None)
                        else:
                            if len(child_value_1) >=1:
                                child_propery_id_1 = kg_property_list.push_property("使用的技能")
                                kg_property_list.push_path(child_propery_id_1, child_propery_id, child_propery_1, None)
                            for termnolgoy in child_value_1:
                                child_propery_id_2 = kg_property_list.push_property(termnolgoy['术语'])
                                kg_property_list.push_path(child_propery_id_2, child_propery_id_1, '',
                                                           termnolgoy.get('悬浮', None))
            elif base_property == "技能":
                for skill in kg_cv[base_property]:
                    skill_id = kg_property_list.push_property(skill['术语'])
                    kg_property_list.push_path(skill_id, property_id, skill['程度'], skill.get('悬浮', None))
                    # for child_propery_1, child_value_1 in skill.items():
                    #     if child_propery_1 == "悬浮" or child_value_1=="" or child_value_1 is None:
                    #         continue
                    #     if child_propery_1 == "术语":
                    #         continue
                    #     child_propery_id_1 = kg_property_list.push_property(child_value_1)
                    #     kg_property_list.push_path(child_propery_id_1, skill_id, child_propery_1, None)

        return {
            "ids": kg_property_list.id_table,
            "edges": kg_property_list.property_list
        }

    def remove_null(self, temp):
        # for k, v in temp.items():
        for k in list(temp.keys()):
            v = temp[k]
            if v == "" or v is None:
                del temp[k]
            elif type(v) == list:
                for item in v:
                    if item == "" or item is None:
                        temp[k].remove(item)
                    elif type(item) == dict:
                        self.remove_null(item)
            elif type(v) == dict:
                self.remove_null(v)
