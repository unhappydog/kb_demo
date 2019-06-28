from utils.MapTags import DataMap, sql, update, insert
from services.tool_services.mysql_service import mysqlService
from data_access.base.BaseController import BaseController
from utils.Logger import logging

class CommonController(BaseController):
    def __init__(self, schema, table):
        self._table = table
        self._schema = schema

    def insert_datas_from_df(self, df, key_column="_id"):
        _table = self._table
        key = key_column

        if df is None of df.empy:
            return

        for index, row in df.iterrows():
            columns = list(row.index)
            columns.remove(key_column)
            data = mysqlService.execute("use {0};select * from {1} where {2} = {3}".format(self._schema, self._table, key_column, row[key_column]))
            if data:
                use_replace = False
            else:
                use_replace = True

            if use_replace == True:
                sql_head = "replace {0} set".format(self._table)
            else:
                sql_head = "update {0} set".format(self._table)

            sql_body = " {0}=\"{1}\""
            if use_replace is True:
                sql_end = ",{0}={1}".format(key, row[key])
            else:
                sql_end = "where {0}={1}".format(key, row[key])
            sql = sql_head
            for column in columns:
                if row[column] is None:
                    continue
                elif type(row[column]) is float:
                    if math.isnan(row[column]):
                        continue
                    else:
                        sql += sql_body.format(column, row[column]) + ","
                elif type(row[column]) is str:
                    sql += sql_body.format(column, row[column].replace("\"", "\\\"")) + ","
                else:
                    sql += sql_body.format(column, row[column]) + ","
            sql = sql[:-1] + " " + sql_end

            try:
                mysqlService.execute("use {0};{1}".format(self._schema, sql))
            except Exception as e:
                logging.error("bad sql {0}".format(sql), e)
                logging.exception()

