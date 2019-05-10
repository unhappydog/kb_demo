class EducationExperience:
    def __init__(self, educationTimePeriod="", educationStartTime="", educationEndTime="",
                 educationSchool="", educationMajor="", educationDegree="",
                 educationMajorDescription="", educationScore="", majorBigType="",
                 majorSmallType=""):
        self.educationTimePeriod = educationTimePeriod
        self.educationStartTime = educationStartTime
        self.educationEndTime = educationEndTime
        self.educationSchool = educationSchool
        self.educationMajor = educationMajor
        self.educationDegree = educationDegree
        self.educationMajorDescription = educationMajorDescription
        self.educationScore = educationScore
    def __getitem__(self, item):
        return self.__dict__[item]
