from settings import mongo_db
from services.tool_services.MongoService import mgService as mgservice


def DataMap(_schema=mongo_db, _table=''):
    """
    map a class to table
    :param _schema: db
    :param _table: table
    :return:
    """

    def wrapper(cls):
        def _dataMap(*args, **kargs):
            instance = cls(*args, **kargs)
            instance.__dict__['_schema'] = _schema
            instance.__dict__['_table'] = _table
            return instance

        return _dataMap

    return wrapper


def insert():
    def wrapper(func):
        def _sql(self, data, *args, **kargs):
            if type(data) == dict:
                doc = data
            else:
                doc = parse_data(data)
            mgservice.insert(doc, self._schema, self._table)
            return True

        return _sql

    return wrapper


def delete(by=None):
    def wrapper(func):
        def _sql(self, _id, *args, **kwargs):
            if by == None:
                spec = {"_id": _id}
            else:
                spec = by
            mgservice.delete(spec, self._schema, self._table)
            return True

        return _sql

    return wrapper


def update():
    def wrapper(func):
        def _sql(self, data, *args, **kwargs):
            spec = {"_id": data._id}
            doc = parse_data(data)
            del doc["_id"]
            mgservice.update(spec, doc, self._schema, self._table)
            return True
        return _sql
    return wrapper


def query(by={"_id": "_id"}):
    def wrapper(func):
        def _sql(self, *args, **kwargs):
            # spec = {"_id": _id}
            loc = locals()
            spec = {}
            if by is None:
                data = mgservice.query({}, self._schema, self._table)
            else:
                for k, v in by.items():
                    spec[k] = loc['kwargs'][v]
                data = mgservice.query(spec, self._schema, self._table)
            return data

        return _sql

    return wrapper


def parse_data(data):
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