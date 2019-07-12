
class Ontology:
    def __init__(self, _id, _type):
        self._id = _id
        self._type = _type

    def __eq__(self, other):
        return self._id == other._id and self._type == other._type

    def __hash__(self):
        return hash(self._id) + hash(self._type)
