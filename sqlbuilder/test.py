from sqlbuilder.builder import *

"""
假设我们现在有个购物车表
brand(id,name,logo,date)
user(id,name,password)
shopping(id,brand_id,user_id,time,money)
"""
if __name__ == '__main__':
    # 查询确定的id
    brand_id = Condition("id", 2)
    # 按照name来查询
    brand_name = Condition("name", "iphone")
    # 查询不等于"panda"的
    brand_logo = Condition("logo", "panda", OPERATION.OP_NOT_LIKE)
    # 日期要大于等于5月20号的
    brand_date = Condition("date", "20200520", OPERATION.OP_GE)
    "SELECT * FROM brand  WHERE id = 2 and name like '手机%'  order by id,date ;"
    print(Select("brand").where([('id', '=', 2), ('name', 'like', "手机%")], OPERATION.OP_AND).asc(
        ["id", "date"]).build())
    select_user_shopping = Select("shopping").join(
        [Condition('shopping.user_id', 'user.id', OPERATION.OP_JOIN, "user")]).where(
        [('shopping.id', "=", 2), ('user.name', 'not like', 'abc')], OPERATION.OP_OR).build()
    "SELECT * FROM shopping join user on shopping.user_id = user.id WHERE shopping.id = 2 or user.name not like 'abc' ;"
    print(select_user_shopping)
    # 更新数据
    s = Update("USER", [("name", "Jense"), ("num", '12346')]).where(
        [("name", "=", "jense")]).build()
    "UPDATE  USER SET name = 'Jense',num = '12346' WHERE name = 'jense' ;"
    print(s)
    # 删除数据
    a = Delete('user').where([("name", "=", "jense")]).build()
    "DELETE FROM user  WHERE name = 'jense' ;"
    print(a)
    # 插入数据
    i = Insert('user', ['id', 'name', 'password'], [123, 'jense', '456']).build()
    "INSERT INTO user (id , name , password) value (123 , 'jense' , '456');"
    print(i)
