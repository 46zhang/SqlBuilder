import logging

import aiomysql
from mysql.mysql_connector import OPMysql


#
# async def create_pool(loop, **kw):
#     logging.info('create database connection pool...')
#     global __pool
#     __pool = await aiomysql.create_pool(
#         host='127.0.0.1',
#         port=3306,
#         user='pusher',
#         password='push',
#         db='sqlorm',
#         loop=loop
#     )
#
#
# async def select(sql: str, args, size=None):
#     global __pool
#     async with __pool.get() as conn:
#         async with conn.cursor(aiomysql.DictCursor) as cur:
#             await cur.execute(sql.replace('?', '%s'), args or ())
#             if size:
#                 rs = await cur.fetchmany(size)
#             else:
#                 rs = await cur.fetchall()
#         logging.info('rows returned: %s' % len(rs))
#         return rs
#
#
# async def execute(sql, args, autocommit=True):
#     async with __pool.get() as conn:
#         if not autocommit:
#             await conn.begin()
#         try:
#             async with conn.cursor(aiomysql.DictCursor) as cur:
#                 await cur.execute(sql.replace('?', '%s'), args)
#                 affected = cur.rowcount
#             if not autocommit:
#                 await conn.commit()
#         except BaseException as e:
#             if not autocommit:
#                 await conn.rollback()
#             raise
#         return affected
#

def select(sql: str, args, size=None):
    mysql = OPMysql()
    if size:
        mysql.select_one(sql.replace('?', '%s'), args)
    else:
        mysql.select_all(sql.replace('?', '%s'))
    mysql.dispose()


def execute(sql, args):
    mysql = OPMysql()
    args_tuple = tuple(args)
    print(args_tuple)
    s = sql.replace('?', "'%s'") % args_tuple
    print(s)
    mysql.update(s)
    mysql.dispose()
