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
        sub_value = sub()

        print(sub_value)
        pub('message1')
        sub_value = sub()
        print(sub_value)
        pub('message2')
        sub_value = sub()
        print(sub_value)

if __name__ == '__main__':
    unittest.main()
