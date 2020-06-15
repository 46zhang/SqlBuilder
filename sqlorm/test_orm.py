import asyncio
import time
import uuid

import aiomysql
import pymysql

from sqlorm import orm
from sqlorm.model import Model
from sqlorm.field import StringField, FloatField, BooleanField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


def test_orm():
    asyncio.run(
        orm.create_pool( user='pusher', password='push', db='sqlorm'))
    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    a = "fafaf"
    print(a)
    print(u)
    asyncio.run(u.save())
    print("over")


async def go():
    pool = await aiomysql.create_pool(host='localhost', port=3306,
                                      user='pusher', password='push',
                                      db='sqlorm', loop=asyncio.get_event_loop(), autocommit=False)

    with (await pool) as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT 10")
        # print(cur.description)
        (r,) = await cur.fetchone()
        assert r == 10
    pool.close()
    await pool.wait_closed()
    # conn = await aiomysql.connect(host="localhost", port=3306,
    #                               user="pusher", password="push",
    #                               db="sqlorm", loop=asyncio.get_event_loop()
    #                               )


if __name__ == "__main__":
    test_orm()
    #asyncio.run(go(), debug=True)
