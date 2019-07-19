from datasketch import MinHash
import re
import datetime
from pandas._libs.tslibs.timestamps import Timestamp


def convert_str_2_date(date):
    if date is None:
        return None
    if type(date) == Timestamp:
        return date.to_pydatetime()
    if type(date) == datetime.datetime:
        return date
    if re.match('^[0-9]{4}\.[0-9]{2}$', date):
        return datetime.datetime.strptime(date, "%Y.%m")
    elif re.match('^[0-9]{2}-[0-9]{2}-[0-9]{2}$', date):
        return datetime.datetime.strptime("20" + date, "%Y-%m-%d")
    elif re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date):
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    elif re.match('^[0-9]{1,2}月 [0-9]{1,2}日.*$', date):
        month, day = date.split('日')[0].split('月 ')
        return datetime.datetime(year=2019, month=int(month), day=int(day))
    elif re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', date):
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    elif re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$', date):
        return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        print("un recongize {0}".format(date))
        return date


def get_variable(name):
    loc = locals()
    key = ''
    for key in loc:
        if loc[key] == name:
            return key


def parse_segged_word(doc):
    if doc is None or doc is "":
        return []
    return [word.split(':')[0] for sentence in doc.split(';') for word in sentence.split(',')]


def compute_min_hash(word_list):
    m = MinHash()
    for word in word_list:
        m.update(word.encode())
    return m


def update_min_hash(m, word_list):
    for word in word_list:
        m.update(word.encode())
    return m


def update_add_dict(d1, d2):
    """
    更新字典，取字段较全者
    """
    temp = {}
    for k, v in d1.items():
        if k in d2.keys():
            if v is None:
                temp[k] = d2[k]
            elif d2[k] is None:
                temp[k] = v
            if type(v) == list and type(d2[k]) == list:
                v = v.extend(d2[k])
                temp[k] = v
            elif type(v) == list and type(d2[k]) != list:
                v = v.append(d2[k])
                temp[k] = v
            elif type(v) != list and type(d2[k]) == list:
                v = d2[k].append(v)
                temp[k] = v
            elif type(v) == dict and type(d2[k]) == dict:
                temp[k] = update_add_dict(v, d2[k])
            else:
                temp[k] = [v, d2[k]]
        else:
            temp[k] = v
    for k, v in d2.items():
        if k not in d1.keys():
            temp[k] = v
    return temp


if __name__ == '__main__':
    print(len(compute_min_hash(['aaa']).digest()))
