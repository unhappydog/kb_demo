from pyknow import *
from enum import Enum
from core.engines.Ontology import Ontology
from services.mysql_service import MysqlService


class Triples(Fact):
    pass

def create_method(relation):
    def reverse(self, triple):
        self.declare(Triples(from_ontology=triple['to_ontology'], to_ontology=triple['from_ontology'], relation=relation))
    return reverse


class ReverseEngine(KnowledgeEngine):
    def __init__(self):
        self.load_rules()
        super().__init__()

    def load_rules(self):
        _rules = {
            '发布公司': '发布',
        }
        count = 1
        for k,v in _rules.items():
            name = "rule" + str(count)
            count +=1
            self.__dict__[name] = Rule(AS.triple<<Triples(from_ontology=P(lambda x: isinstance(x, Ontology)), to_ontology=P(lambda x: isinstance(x, Ontology)), relation=k))(create_method(v))


if __name__ == '__main__':
    engine = ReverseEngine()
    engine.reset()
    engine.declare(Triples(from_ontology=Ontology('a','b'), to_ontology=Ontology('c','d'),relation='发布公司'))
    engine.run()
    print(engine.facts)

