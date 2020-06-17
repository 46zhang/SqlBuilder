from mysql.mysql_connector import OPMysql
from sqlbuilder.builder import *


if __name__ == '__main__':
    mysql = OPMysql()

    sql = Select("auth_user").where([('id', '>', 2)]).build()
    try:
        d = mysql.update(sql)
    except Exception as e:
        print("出现的异常情况是 {}".format(e))
    mysql.dispose()
