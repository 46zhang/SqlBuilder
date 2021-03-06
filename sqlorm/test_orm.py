from utils.log import Logger
import time
import uuid

from sqlorm.model import Model
from sqlorm.field import StringField, FloatField, IntegerField


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


if __name__ == "__main__":
    querySet = User.filter(email='test4123423@example.com', order_by_decs=['id', 'name'],size=5)
    for i in querySet:
        print(i)
    #u = User(name='Test', email='test4123423@example.com', passwd='1234567890', image='about:blank')
    #u.save()
