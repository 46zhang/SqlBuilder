# SQL解析器与SQL ORM实现
## 项目背景
目前orm框架是主流的数据库操作方式，但是其存在着灵活性不高的问题，我在项目中使用了django的orm框架， 发现存在俩个问题   
1. 联表查询不方便，如果表格之间没有外键关联，往往需要建立第三个表来映射俩个表格之间的关系  
2. 多条件查询以及嵌套查询不方便，在进行多个条件过滤时，可以使用query_set的与、或等操作进行拼接，但是效率低下

## 本项目
本项目旨在通过提供灵活多变、可拓展性高sql语句解析器，通过调用链的方式实现对sql语句的拼接生成，减少重复的代码量

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
todo


## 设计之禅
1. 灵活多变为第一要素
2. 调用链式的灵活构建
3. 统一的规范、接口会更加美观
