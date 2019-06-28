from core.processors.cv_processor import cvProcessor
from core.common.tasks.PreProcessTask import BasePreProcessTask


@cvProcessor.add_as_processors(order=0, stage=1,bad_column="ISBAD")
class PreProcessTask:
    def __init__(self, bad_column):
        self.bad_column = bad_column

    def fit(self, data):
        data[self.bad_column] = data.apply(lambda x: 0 if self.check_if_good(x) else 1, axis=1)
        return data

    def check_if_good(self, cv):
        workExperience = cv.get('workExperience', [])
        if_work_experience_good = self.check_work_experience(workExperience)
        educationExperience = cv.get('educationExperience', [])
        if_education_experience_good = self.check_education_experience(educationExperience)
        return if_education_experience_good and if_work_experience_good

    def check_work_experience(self, work_experiences):
        if work_experiences:
            for work_experience in work_experiences:
                if len(work_experience.get('workDescription', '')) <= 10:
                    return False
        return True

    def check_education_experience(self, education_experiences):
        if not education_experiences:
            return False
        else:
            return True
