import datetime
import re


def get_variable(name):
    loc = locals()
    key = ''
    for key in loc:
        if loc[key] == name:
            return key


def convert_str_2_date(date):
    if type(date) == datetime.datetime:
        return date
    if re.match('^[0-9]{4}\.[0-9]{2}$', date):
        return datetime.datetime.strptime(date, "%Y.%m")
    elif re.match('^[0-9]{2}-[0-9]{2}-[0-9]{2}$', date):
        return datetime.datetime.strptime("20" + date, "%Y-%m-%d")
    elif re.match('^[0-9]{1,2}月 [0-9]{1,2}日.*$', date):
        month, day = date.split('日')[0].split('月 ')
        return datetime.datetime(year=2019, month=int(month), day=int(day))
    elif re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', date):
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        print("un recongize")
        return date


if __name__ == '__main__':
    print(convert_str_2_date('2012-09-01 00:00:00'))
