import redis as pyrdis
import threading
from online_processor.settings import settings


def Singleton(cls):
    _instance = {}
    _instance_lock = threading.Lock()

    def _singleton(*args, **kargs):
        if cls not in _instance:
            with _instance_lock:
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


class RedisService:
    def __init__(self, host=settings.redis_host, port=settings.redis_port):
        self.pool = pyrdis.ConnectionPool(host=host, port=port)

    def get_value(self, key):
        jedis = pyrdis.StrictRedis(connection_pool=self.pool)
        return jedis.get(key)

    def set_value(self, key, value, time=0):
        jedis = pyrdis.StrictRedis(connection_pool=self.pool)
        if time != 0:
            jedis.set(name=key, value=value, ex=time)
        else:
            jedis.set(name=key, value=value)


redis = RedisService()
