from core.processors.cv_processor import cvProcessor
from core.base.BaseTask import BaseTask
from utils import Utils
from core.base.data.LSHBasedFixSizeHash import LSHBasedFixSizeHash

@cvProcessor.add_as_processors(order=1, stage=1, replicate_column="ISREPLICATE", min_score=0.7)
class DistinctTask(BaseTask):
    def __init__(self, replicate_column, min_score):
        self.replicate_column = replicate_column
        self.history = LSHBasedFixSizeHash()
        self.min_score = min_score

    def fit(self, data):
        data[self.replicate_column] = data.apply(lambda x: self.check_if_duplicate(x), axis=1)
        return data

    def check_if_duplicate(self, cv):
        if cv is None:
            return 1

        """
        check if a cv is duplicate use the describes of it's experiences
        """
        work_experiences = cv.get('workExperience', [])
        education_experiences = cv.get('educationExperience', [])
        project_experiences = cv.get('projectExperience', [])

        work_describes = [work_experience.get('workDescription') for work_experience in work_experiences]

        education_describes = [education_experience.get('educationSchool') + education_experience.get('educationMajor') for education_experience in education_experiences]

        project_describes = [project_experience.get('projectDescription','') + project_experience.get('projectDuty','') for project_experience in project_experiences]

        describes = work_describes + education_describes + project_describes
        if not describes:
            return 1
        m = Utils.compute_min_hash(describes)
        m_score = self.history.get_max_similar(m)
        self.history.add(m)
        if m_score > self.min_score:
            return 1
        return 0
