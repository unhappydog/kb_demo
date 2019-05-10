class Skill:
    def __init__(self, name="", skillMastery="", skillUseTime=""):
        self.name = name
        self.skillMastery = skillMastery
        self.skillUseTime = skillUseTime

    def __getitem__(self, item):
        return self.__dict__[item]

