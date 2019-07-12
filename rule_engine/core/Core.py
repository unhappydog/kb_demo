from pyknow import *

class Light(Fact):
    pass

class Person:
    def __init__(self,_id, _type):
        self._id = _id
        self._type = _type

    def __eq__(self, other):
        return self._id == other._id

class RobotCrossStreet(KnowledgeEngine):
    @Rule(Light(color='green'))
    def green_light(self):
        print("walk")

    @Rule(Light(color='red'))
    def red_light(self):
        print("Don't walk")

    @Rule(Light(color='red'),Light(name='test'))
    def test(self):
        print('test pass')

    @Rule(AS.light << Light(color=L('red') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is ", light["color"])

if __name__ == '__main__':
    engine = RobotCrossStreet()
    engine.reset()
    engine.declare(Light(color='red', name='test'))
    engine.run()
    print('test only red')
    engine.reset()
    engine.declare(Light(color='red'))
    engine.run()

