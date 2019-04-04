import threading
# from services.mysql_service import mysql


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






