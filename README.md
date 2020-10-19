# SQL解析器与SQL ORM实现
## 项目背景
目前orm框架是主流的数据库操作方式，虽然其存在着效率不够高的问题，但是在项目开发中，极大地提升了开发效率，大多数orm框架都较为复杂，学习成本较高，本项目旨在实现orm框架最核心部分，降低orm学习成本，增加orm框架的灵活性。
## 本项目
本项目旨在实现一个轻量级的orm框架，手把手教大家完成一个orm框架
此外，本项目还提供灵活多变、可拓展性高sql语句解析器，通过调用链的方式实现对sql语句的拼接生成，减少重复的代码量

同时本项目正在实现一个orm框架

## SQL解析器
### 使用
**select查询**
```python
#1.直接用where放置列表来做筛选
print(Select("brand").where([('id', '=', 2), ('name', 'like', "手机%")], OPERATION.OP_AND).asc(
        ["id", "date"]).build())
等价于
#"SELECT * FROM brand  WHERE id = 2 and name like '手机%'  order by id,date ;"

#2. 直接用俩个列表传入数据来做筛选
print(Select("user", "id,username,password").where(['id', 'username', 'password'], [1, "jense", "123456"]).build())
等价于
# "SELECT id,username,password FROM user  WHERE id 1 'and' and username jense 'and' and password 123456 'and' ;"
#3. 联表查询
select_user_shopping = Select("shopping", ("user_id,brand_id,mony")).join(
        [("user", 'shopping.user_id', 'user.id')]).where(
        [('shopping.id', "=", 2), ('user.name', 'not like', 'abc')]).build()
等价于
#"SELECT id,username,password FROM user  WHERE id 1 'and' and username jense 'and' and password 123456 'and' ;"
```
**插入数据**
```python
# 插入数据
i = Insert('user', ['id', 'name', 'password'], [123, 'jense', '456']).build()
# "INSERT INTO user (id , name , password) value (123 , 'jense' , '456');"
```

**delete删除**
```python
a = Delete('user').where([(["name","id","password"],["jense",2,"123455"])]).build()
print(a)
#等价与 "DELETE FROM user  WHERE name = 'jense' and id=2 and password='123455' ;"
```
## SQL ORM
demo

```python
class User(Model):
    '''table name'''
    __table__ = 'users'
    '''primary_key'''
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = IntegerField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

querySet = User.filter(email='test4123423@example.com', order_by_decs=['id', 'name'],size=5)
    for i in querySet:
        '''打印输出结果'''
        print(i)


```

## 设计之禅
1. 灵活多变为第一要素
2. 调用链式的灵活构建
3. 统一的规范、接口会更加美观
