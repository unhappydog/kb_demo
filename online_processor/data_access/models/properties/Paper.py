class Paper:
    def __init__(self,name="", source="", pubishTime="", description=""):
        self.name = name
        self.source = source
        self.publishTime = pubishTime
        self.description = description
    def __getitem__(self, item):
        return self.__dict__[item]