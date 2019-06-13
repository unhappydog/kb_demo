import json
from bson import ObjectId
from datetime import datetime, date
import time


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MyEncoder4News(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            delta_time = datetime.now() - obj
            if delta_time.days > 1:
                return obj.strftime('%Y-%m-%d %H:%M')
            elif delta_time.days > 0:
                return "{0}天前".format(delta_time.days)
            elif delta_time.seconds > 60:
                minutes = delta_time.seconds / 60
                if minutes > 60:
                    hours = minutes / 60
                    return "{0}小时前".format(int(hours))
                else:
                    return "{0}分钟前".format(int(minutes))
            else:
                return "{0}秒前".format(delta_time.seconds)
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, float):
            obj = time.localtime(obj)
            obj = datetime(year=obj.tm_year,
                           month=obj.tm_mon,
                           day=obj.tm_mday,
                           hour=obj.tm_hour,
                           minute=obj.tm_min,
                           second=obj.tm_sec)
            return covert_time(obj)
        elif isinstance(obj, int):
            obj = time.localtime(float(obj))
            obj = datetime(year=obj.tm_year,
                           month=obj.tm_mon,
                           day=obj.tm_mday,
                           hour=obj.tm_hour,
                           minute=obj.tm_min,
                           second=obj.tm_sec)
            return covert_time(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def covert_time(time_value):
    delta_time = datetime.now() - time_value
    if delta_time.days > 1:
        return time_value.strftime('%Y-%m-%d')
    elif delta_time.days > 0:
        return "{0}天前".format(delta_time.days)
    elif delta_time.seconds > 60:
        minutes = delta_time.seconds / 60
        if minutes > 60:
            hours = minutes / 60
            return "{0}小时前".format(int(hours))
        else:
            return "{0}分钟前".format(int(minutes))
    else:
        return "{0}秒前".format(delta_time.seconds)
