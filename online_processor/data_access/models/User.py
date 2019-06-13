class User:
    def __init__(self,_id="", followed_company=[], followed_academy=[], followed_skill=[]):
        self._id = _id
        self.followed_company = followed_company
        self.followed_skill = followed_skill
        self.followed_academy = followed_academy

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, index, value):
        self.__dict__[index] = value
