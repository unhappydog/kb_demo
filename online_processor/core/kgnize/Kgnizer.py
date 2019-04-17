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
        cv_kg = {'基础信息': {
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
                self.process_work_experience(cv.workExperience, link_text['workExperience'],link_company)
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

        for termnology in all_skills:
            if termnology['cnName']:
                name = termnology['cnName'][0]
            else:
                name = termnology['engName'][0]
            mastery = "涉及过"
            cv_kg["技能"].append({
                "术语": name,
                "程度": mastery,
                '悬浮': termnology
            })

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
            linked_columns = self.link_dict['projectExperience']
            termnologys = self.extract_termnologys_from_linked_experiences(linked_columns, linked_experience)
            result.append({
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
            if termnology['cnName']:
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
