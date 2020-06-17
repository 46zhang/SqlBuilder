import time
import uuid

from sqlorm.model import Model
from sqlorm.field import StringField, FloatField, BooleanField, IntegerField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = IntegerField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


# async def test_example(loop):
#     await orm.create_pool(loop=loop, host='localhost', port=3306,
#                           user='pusher', password='push',
#                           db='sqlorm', autocommit=False)
#     u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
#     await u.save()


if __name__ == "__main__":
    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    u.save()
