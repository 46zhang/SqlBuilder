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
#"SELECT * FROM brand  WHERE id = 2 and name like '手机%'  order by id,date ;"
print(Select("brand").where([('id', '=', 2), ('name', 'like', "手机%")], OPERATION.OP_AND).asc(
        ["id", "date"]).build())
# 更新数据
s = Update("USER", [("name", "Jense"), ("num", '12346')]).where(
        [("name", "=", "jense")]).build()
#"UPDATE  USER SET name = 'Jense',num = '12346' WHERE name = 'jense' ;"
```

**delete删除**
```python
a = Delete('user').where([("name","=","jense")]).build()
print(a)
#等价与 'DELETE FROM user  WHERE name = 'jense' ;'
```
## SQL ORM
todo


## 设计之禅
1. 灵活多变为第一要素
2. 调用链式的灵活构建
3. 统一的规范、接口会更加美观
