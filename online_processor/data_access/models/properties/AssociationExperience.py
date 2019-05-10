class AssociationExperience:
    def __init__(self, practiceTimePeriod="", practiceStartTime="", practiceEndTime="",
                 practiceName="", practiceDescription=""):
        self.practiceTimePeriod = practiceTimePeriod
        self.practiceStartTime = practiceStartTime
        self.practiceEndTime = practiceEndTime
        self.practiceName = practiceName
        self.practiceDescription = practiceDescription

    def __getitem__(self, item):
        return self.__dict__[item]
