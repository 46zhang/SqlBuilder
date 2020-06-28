from mysql.mysql_connector import OPMysql


def dict_slice(aim_dict: dict, start: int, end: int) -> dict:
    """
    dict slice funciton
    :param aim_dict:
    :param start:
    :param end:
    :return:
    """
    keys = [i for i in aim_dict]
    slice_result = {}
    for k in keys[start:end]:
        slice_result[k] = aim_dict[k]
    return slice_result


def select(sql: str, args: list, size=None) -> dict:
    """
    select function
    :param sql:带参数的sql语句
    :param args:sql语句中的参数
    :param size:
    :return:dict
    """
    mysql = OPMysql()
    args_tuple = tuple(args)
    s = sql % args_tuple + ";"
    if size == 1:
        rs = mysql.select_one(s)
    else:
        rs = mysql.select_all(s)
    mysql.dispose()
    # 如果返回结果超过了size限制
    if size and size < len(rs):
        return rs[:size]
    return rs


def execute(sql: str, args: list) -> int:
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
