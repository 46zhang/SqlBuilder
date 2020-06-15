import asyncio
import time
import uuid

import aiomysql

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
        orm.create_pool(asyncio.get_event_loop(), user='root', password='123456', db='mysql', database='sqlorm'))
    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    a = "fafaf"
    print(a)
    print(u)
    asyncio.run(u.save())
    print("over")


loop = asyncio.get_event_loop()


async def go():
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                           user='root', password='123456',
                                           db='mysql', loop=loop, autocommit=False)

    with (await pool) as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT 10")
        # print(cur.description)
        (r,) = await cur.fetchone()
        assert r == 10
    pool.close()
    await pool.wait_closed()


loop.run_until_complete(go())

if __name__ == "__main__":
    # test_orm()
    asyncio.run(go())
