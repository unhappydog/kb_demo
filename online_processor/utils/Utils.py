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
    elif re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date):
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    elif re.match('^[0-9]{1,2}月 [0-9]{1,2}日.*$', date):
        month, day = date.split('日')[0].split('月 ')
        return datetime.datetime(year=2019, month=int(month), day=int(day))
    elif re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', date):
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        print("un recongize {0}".format(date))
        return date


def parse_data_to_dict(data):
    doc = {}
    for key, value in data.__dict__.items():
        # if key == "_id":
        #     key = "id"
        if type(value) != list:
            doc[key] = value
        else:
            doc[key] = []
            for value_item in value:
                if type(value_item) == dict:
                    doc[key].append(value_item)
                elif type(value_item) == str:
                    doc[key].append(value_item)
                else:
                    doc[key].append(value_item.__dict__)
    return doc


if __name__ == '__main__':
    print(convert_str_2_date('2012-09-01 00:00:00'))
    print(convert_str_2_date('2015-07-01'))
