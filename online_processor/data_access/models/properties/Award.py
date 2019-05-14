class Award:
    def __init__(self, time="", awardKind="", awardLevel="", awarddescription=""):
        self.time = time
        self.awardKind = awardKind
        self.awardLevel = awardLevel
    def __getitem__(self, item):
        return self.__dict__[item]