class Certificate:
    def __init__(self, name="", description="", time=""):
        self.name = name
        self.description = description
        self.time = time
    def __getitem__(self, item):
        return self.__dict__[item]