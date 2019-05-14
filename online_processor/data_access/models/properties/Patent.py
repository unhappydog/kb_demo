class Patent:
    def __init__(self, name="", publishTime=""):
        self.name = name
        self.publishTime = publishTime
    def __getitem__(self, item):
        return self.__dict__[item]