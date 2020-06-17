from mysql.mysql_connector import OPMysql


def select(sql: str, args, size=None):
    """
    select function
    :param sql:
    :param args:
    :param size:
    :return:
    """
    mysql = OPMysql()
    args_tuple = tuple(args)
    s = sql.replace('?', "'%s'") % args_tuple
    if size:
        mysql.select_one(s)
    else:
        mysql.select_all(s)
    mysql.dispose()


def execute(sql, args):
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
