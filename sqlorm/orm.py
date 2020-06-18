from mysql.mysql_connector import OPMysql


def select(sql: str, args: list, size=None):
    """
    select function
    :param sql:
    :param args:
    :param size:
    :return:
    """
    mysql = OPMysql()
    args_tuple = tuple(args)
    s = sql % args_tuple + ";"
    if size:
        rs = mysql.select_one(s)
    else:
        rs = mysql.select_all(s)
    mysql.dispose()
    return rs


def execute(sql: str, args: list):
    """
    insert update delete function
    :param sql:
    :param args:
    :return:
    """
    mysql = OPMysql()
    args_tuple = tuple(args)
    s = sql % args_tuple
    rows = mysql.update(s)
    mysql.dispose()
    return rows
