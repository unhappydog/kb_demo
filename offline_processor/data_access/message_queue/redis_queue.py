import redis
from settings import redis_port, redis_port
import threading


class RedisService:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def instance(cls):
        if RedisService._instance is None:
            with RedisService._lock:
                if RedisService._instance is None:
                    RedisService._instance = cls()
        return RedisService._instance

    def __init__(self, host=settigs.redis_host, port=settings.redis_port):
        self.pool = redis.ConnectionPool(host=host, port=port)

    def get_value(self, key):
        redis = redis.StrictRedis(connection_pool=self.pool)
        return redis.get(key)


    def set_value(self, key, value, time=0):
        redis = redis.StrictRedis(connection_pool=self.pool)
        if time != 0:
            redis.set(name=key, value=value, ex=time)
        else:
            redis.set(name=key, value=value)

    def channel(self, topic, action='p'):
        """Public or subscribe a channel

        This function create a topic in redis, and return a
        publish function or subscribe function according to
        the input paragm
        Args:
            topic (str): The channel name
            action (str): p for create channel, s for subscribe channel

        Returns:
            func: the publish function or subscribe function

        """
        redis = redis.StrictRedis(connection_pool=self.pool)
        def publish(msg):
            redis.publish(topic, msg)
            return True

        def subscribe():
            pub.parse_response()
            return pub

        if action == 'p':
            return publish
        elif action == 's':
            pub = redis.pubsub()
            pub.subscribe(topic)
            pub.parse_response()
            return subscribe
