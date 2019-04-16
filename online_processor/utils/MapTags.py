from services import mysqlService as mysql
from settings import mysql_db


def DataMap(_schema=mysql_db , _table=''):
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





def sql(sql, *parameters):
    """
    execute sql with parameters.
    :param sql: a sql str in format of python format string.st: "select * from {0}"
    :param parmeters: parameter's name of every parameter in parameters, for example:
    @sql("select * from _table where id = {0}", "_id")
    def get_by_id(_id)
    :return: a list of data, which is the result of executing provided sql
    """

    def wrapper(func):
        def _sql(self, *args, **kargs):
            # print(locals())
            loc = locals()
            paras = [loc['kargs'][para] for para in parameters]
            acture_sql = sql.format(*paras).replace("_table", self._table)
            if '_schema' in self.__dict__:
                datas = mysql.execute("use {0}".format(self._schema), acture_sql)
            else:
                datas = mysql.execute(acture_sql)
            return datas

        return _sql

    return wrapper


def update():
    """
    update by _id
    :return:
    """

    def wrapper(func):
        def _sql(self, data, *args, **kargs):
            _id = data._id
            # mysql.execute("update {0} set ")
            update_format = "{0}={1}"
            update_list = []
            for k, v in data.__dict__.items():
                if k != '_id':
                    update_list.append(update_format.format(k, v))
            actual_sql = "update {0} set {1} where id={2}".format(self._table, ",".join(update_list), _id)
            mysql.execute(actual_sql)
            return True

        return _sql

    return wrapper


def insert():
    def wrapper(func):
        def _sql(self, data, *args, **kargs):
            keys = []
            values = []
            for key,value in data.__dict__.items:
                if key == "_id":
                    keys.append("id")
                else:
                    keys.append(key)
                values.append(value)

            actual_sql = "insert into {0}({1}) values({2})".format(self._table, ",".join(keys), ",".join(values))
            mysql.execute(actual_sql)
            return True

        return _sql

    return wrapper
