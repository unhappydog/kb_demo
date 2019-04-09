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


def return_type(cls_type):
    """
    covert the return of a special func to cls_type
    :param cls_type:
    :return:
    """

    def wrapper(func):
        def _return_type(self, *args, **kwargs):
            datas = func(self, *args, **kwargs)
            result = []
            for data in datas:
                temp_instance = cls_type()
                for key, value in data.items():
                    if key == '﻿id' or key == 'id':
                        key = '_id'
                    temp_instance.__dict__[key] = value
                result.append(temp_instance)
            return result

        return _return_type

    return wrapper
