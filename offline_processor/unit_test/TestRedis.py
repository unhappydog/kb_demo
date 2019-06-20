import sys
sys.path.append(".")
from services.tool_services.RedisServiceV2 import RedisService
import unittest

redis_service = RedisService.instance()
class TestRedisService(unittest.TestCase):

    def test_channel(self):
        pub = redis_service.channel('test', 'p')
        sub = redis_service.channel('test', 's')
        pub('message')
        pub('message1')
        pub('message2')
        sub_value = sub()
        print(sub_value)
        sub_value = sub()
        print(sub_value)
        sub_value = sub()
        print(sub_value)
        sub2 = redis_service.channel('test', 's')
        # sub_value = sub2()
        # print(sub_value)
        pub('message3')
        sub_value1 = sub()
        print(sub_value1)
        sub_value2 = sub2()
        print(sub_value2)

if __name__ == '__main__':
    unittest.main()
