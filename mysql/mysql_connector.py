import pymysql
from DBUtils.PooledDB import PooledDB
from mysql.config import mysqlInfo


class OPMysql(object):
    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = OPMysql.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if OPMysql.__pool is None:
            OPMysql.__pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=mysqlInfo['host'],
                                      user=mysqlInfo['user'], passwd=mysqlInfo['password'], db=mysqlInfo['db'],
                                      port=mysqlInfo['port'], charset=mysqlInfo['charset'])
            # print(f'---------------{OPMysql.__pool}')
        return OPMysql.__pool.connection()
        # 插入\更新\删除sql

    def update(self, sql, param=None):
        # print('op_insert', sql)
        if param == None:
            insert_num = self.cur.execute(sql)
        else:
            insert_num = self.cur.execute(sql, param)
        # print('mysql sucess ', insert_num)
        self.coon.commit()
        return insert_num

    def insert_many(self, sql, values):

        count = self.cur.executemany(sql, values)
        return count

    # 查询
    def select_one(self, sql, param=None):
        # $print('op_select', sql)
        if param == None:
            self.cur.execute(sql)  # 执行sql
        else:
            self.cur.execute(sql, param)  # 执行sql
        select_res = self.cur.fetchone()  # 返回结果为字典
        return select_res

    def select_all(self, sql):
        # $print('op_select', sql)
        self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchall()  # 返回结果为字典
        return select_res

        # 释放资源

    def dispose(self):
        self.coon.close()
        self.cur.close()
