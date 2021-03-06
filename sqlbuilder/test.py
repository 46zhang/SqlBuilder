from sqlbuilder.builder import *

"""
假设我们现在有个购物车表
brand(id,name,logo,date)
user(id,name,password)
shopping(id,brand_id,user_id,time,money)
"""
if __name__ == '__main__':
    # "SELECT * FROM brand  WHERE id = 2 and name like '手机%'  order by id,date ;"
    print(Select("brand").where([('id', '=', 2), ('name', 'like', "手机%")], OPERATION.OP_AND).asc(
        ["id", "date"]).build())
    # "SELECT id,username,password FROM user  WHERE id 1 'and' and username jense 'and' and password 123456 'and' ;"
    print(Select("user", "id,username,password").where(['id', 'username', 'password'], [1, "jense", "123456"]).build())
    select_user_shopping = Select("shopping", ("user_id,brand_id,mony")).join(
        [("user", 'shopping.user_id', 'user.id')]).where(
        [('shopping.id', "=", 2), ('user.name', 'not like', 'abc')]).build()
    # "SELECT * FROM shopping join user on shopping.user_id = user.id WHERE shopping.id = 2 or user.name not like 'abc' ;"
    print(select_user_shopping)
    # 更新数据
    s = Update("USER", [("name", "Jense"), ("num", '12346')]).where(
        [("name", "=", "jense")]).build()
    # "UPDATE  USER SET name = 'Jense',num = '12346' WHERE name = 'jense' ;"
    print(s)
    # 删除数据
    a = Delete('user').where([("name", "=", "jense")]).build()
    # "DELETE FROM user  WHERE name = 'jense' ;"
    print(a)
    # 插入数据
    i = Insert('user', ['id', 'name', 'password'], [123, 'jense', '456']).build()
    # "INSERT INTO user (id , name , password) value (123 , 'jense' , '456');"
    print(i)
