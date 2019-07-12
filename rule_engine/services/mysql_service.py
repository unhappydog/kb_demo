import pymysql
from DBUtils.PooledDB import PooledDB
import settings
from threading import Lock


class MysqlService:
    _instance = None
    _lock = Lock()

    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self, host=settings.mysql_host, port=settings.mysql_port,
                 user=settings.mysql_user, passwd=settings.mysql_password,
                 db=settings.mysql_db):
        self.pool = PooledDB(pymysql, 5,
                             host=host,
                             port=port,
                             user=user,
                             passwd=passwd,
                             db=db)

    def execute(self, *sqls):
        conn = self.pool.connection()
        # conn.set
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            for sql in sqls:
                cursor.execute(sql)
            datas_source = cursor.fetchall()
            datas = [data for data in datas_source]
            return datas
        finally:
            conn.commit()
            cursor.close()
            conn.close()



if __name__ == '__main__':
    print(mysqlService.execute("show databases;"))
    print(mysqlService.execute("use jiaotong;", "show tables;"))
    # print(mysql.execute("show tables;"))
    # print(MysqlService.execute.__name__)
