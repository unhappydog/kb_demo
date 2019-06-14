from core.person_job_fit.PersonJobFit import PersonJobFit
from threading import Lock


class PersonJobFitService:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.personJobFit = PersonJobFit()

    @classmethod
    def instance(cls):
        if PersonJobFitService._instance is None:
            with PersonJobFitService._lock:
                if PersonJobFitService._instance is None:
                    PersonJobFitService._instance = PersonJobFitService()
        return PersonJobFitService._instance

    def score(self,cv, position):
        return self.personJobFit.score(cv, position)
