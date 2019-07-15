from core.EngineFactory import engine_factory
from core.engines.Ontology import Ontology

class Core:
    def _parse(self, datas):
        for data in datas:
            



if __name__ == '__main__':
    engine = RobotCrossStreet()
    engine.reset()
    engine.declare(Light(color='red', name='test'))
    engine.run()
    print('test only red')
    engine.reset()
    engine.declare(Light(color='red'))
    engine.run()

