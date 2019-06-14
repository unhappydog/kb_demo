class Position:
    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, index, value):
        self.__dict__[index] = value
