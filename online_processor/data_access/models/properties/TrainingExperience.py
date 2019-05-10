class TrainingExperience:
    def __init__(self, trainingTimePeriod="", trainingStartTime="", trainingEndTime="",
                 trainingOrg="", trainingPlace="", trainingCourse="", trainingCertificate="",
                 trainingDescription=""):
        self.trainingTimePeriod = trainingTimePeriod
        self.trainingStartTime = trainingStartTime
        self.trainingEndTime = trainingEndTime
        self.trainingOrg = trainingOrg
        self.trainingPlace = trainingPlace
        self.trainingCourse = trainingCourse
        self.trainingCertificate = trainingCertificate
        self.trainingDescription = trainingDescription

    def __getitem__(self, item):
        return self.__dict__[item]