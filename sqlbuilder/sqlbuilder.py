import typing


class OPERATION:
    OP_EQ = "="
    OP_NE = "!="
    OP_GE = ">="
    OP_GT = ">"
    OP_LE = "<="
    OP_LT = "<"
    OP_IN = "in"
    OP_NOT_IN = "not in"
    OP_LIKE = "like"
    OP_NOT_LIKE = "not like"
    OP_PREFIX = "prefix"
    OP_NOT_PREFIX = "not prefix"
    OP_SUFFIX = "suffix"
    OP_NOT_SUFFIX = "not suffix"
    OP_AND = "and"
    OP_OR = "or"
    OP_JOIN = "join"
    OP_INNER_JOIN = "inner join"
    OP_LEFT_JOIN = "left join"
    OP_RIGHT_JOIN = "right join"


class Condition:
    """
    Condition类，是条件的基本类，主要有三种类别
    Condition(key,value):表示 key=value
    Condition(key,value,ops):表示 key ops value ops可以为 OPERATION的前10种操作
    Condition(key,value,ops,join_table):表示 ops(['join','left join','right join']) join_table on key=value
    """

    def __init__(self, key: str, value: str, ops: str = None, join_table=None):
        self.key = key
        self.value = value
        self.ops = '='
        self.join_table = None
        if ops:
            self.ops = ops
        if join_table:
            self.join_table = join_table

    def to_string(self) -> str:
        if not self.join_table:
            return "{} {} '{}'".format(self.key, self.ops, self.value)
        # 如果存在join_table 说明是join条件的，那么ops是['join','left_join',...]
        else:
            return "{} {} on {} = {}".format(self.ops, self.join_table, self.key, self.value)


class SqlBuilder(object):
    def __init__(self, table):
        self.table = table
        self.sql = ""
        self.join_parameter = []
        self.condition_and_parameter = []
        self.condition_or_parameter = []
        self.group_by_parameter = []
        self.asc_parameter = []
        self.desc_parameter = []

    def join(self, table_list: typing.List[Condition] = None) -> object:
        if table_list:
            for t in table_list:
                self.join_parameter.append(t.to_string())
        return self

    def where(self, conditions: typing.List[Condition], ops: str = None) -> object:
        # 默认是条件and
        if not ops or ops == OPERATION.OP_AND:
            # 遍历，然后添加字符串到condition_parameter列表中
            for c in conditions:
                self.condition_and_parameter.append(c.to_string())
        # 添加到或的条件中
        elif ops == OPERATION.OP_OR:
            for c in conditions:
                self.condition_or_parameter.append(c.to_string())
        return self

    def group_by(self, columns: typing.List[str]):
        self.group_by_parameter.append(",".join(columns))

    def asc(self, column: typing.List[str] = None) -> object:
        if column:
            self.asc_parameter.append(",".join(column))
        return self

    def desc(self, column: typing.List[str] = None) -> object:
        if column:
            self.desc_parameter.append(",".join(column))
        return self

    def build(self) -> str:
        return self.sql


class Select(SqlBuilder):
    def __init__(self, table, column: str = None):
        super().__init__(table)
        self.colunm = "*"
        if column:
            self.colunm = column

    def build(self) -> str:
        self.sql = "SELECT {} FROM {} ".format(self.colunm, self.table)
        # 判断是否存在表连接操作
        if self.join_parameter:
            self.sql += " ".join(self.join_parameter)
        """
        添加条件，存在4种情况需要处理
        1.同时存在or与 and条件 ,那么在使用"."拼接的时候会漏掉最开始的or，要再拼接第一个or 
        2.只存在and  
        3.只存在or ,2,3都只需要直接使用join函数将列表转为字符串即可
        4.不存在and与or条件，不做处理
        """
        if self.condition_and_parameter and self.condition_or_parameter:
            self.sql += " WHERE {} ".format(
                " and ".join(self.condition_and_parameter) + " or " + " or ".join(self.condition_or_parameter))
        elif self.condition_and_parameter:
            self.sql += " WHERE {} ".format(" and ".join(self.condition_and_parameter))
        elif self.condition_or_parameter:
            self.sql += " WHERE {} ".format(" or ".join(self.condition_or_parameter))

        if self.group_by_parameter:
            self.sql += " group by {}".format(" ".join(self.group_by_parameter))
        if self.asc_parameter:
            self.sql += " order by {} ".format("".join(self.asc_parameter))
        if self.desc_parameter:
            self.sql += " order by {} desc ".format("".join(self.desc_parameter))
        self.sql += ";"
        return self.sql


class Update(SqlBuilder):
    def __init__(self, table, key_value: typing.List[Condition]):
        super().__init__(table)
        self.key_value = key_value

    def build(self) -> str:
        self.sql = "UPDATE  {} SET {}".format(self.table, ",".join([i.to_string() for i in self.key_value]))
        """
        添加条件，存在4种情况需要处理
        1.同时存在or与 and条件 ,那么在使用"."拼接的时候会漏掉最开始的or，要再拼接第一个or 
        2.只存在and  
        3.只存在or ,2,3都只需要直接使用join函数将列表转为字符串即可
        4.不存在and与or条件，不做处理
        """
        if self.condition_and_parameter and self.condition_or_parameter:
            self.sql += " WHERE {} ".format(
                " and ".join(self.condition_and_parameter) + " or " + " or ".join(self.condition_or_parameter))
        elif self.condition_and_parameter:
            self.sql += " WHERE {} ".format(" and ".join(self.condition_and_parameter))
        elif self.condition_or_parameter:
            self.sql += " WHERE {} ".format(" or ".join(self.condition_or_parameter))
        self.sql += ";"
        return self.sql


class Delete(SqlBuilder):
    def __init__(self, table):
        super().__init__(table)

    def build(self) -> str:
        self.sql = "DELETE FROM {} ".format(self.table)
        """
        添加条件，存在4种情况需要处理
        1.同时存在or与 and条件 ,那么在使用"."拼接的时候会漏掉最开始的or，要再拼接第一个or 
        2.只存在and  
        3.只存在or ,2,3都只需要直接使用join函数将列表转为字符串即可
        4.不存在and与or条件，不做处理
        """
        if self.condition_and_parameter and self.condition_or_parameter:
            self.sql += " WHERE {} ".format(
                " and ".join(self.condition_and_parameter) + " or " + " or ".join(self.condition_or_parameter))
        elif self.condition_and_parameter:
            self.sql += " WHERE {} ".format(" and ".join(self.condition_and_parameter))
        elif self.condition_or_parameter:
            self.sql += " WHERE {} ".format(" or ".join(self.condition_or_parameter))
        self.sql += ";"
        return self.sql


class Insert(SqlBuilder):
    def __init__(self, table, columns: typing.List[str], values: typing.List):
        super().__init__(table)
        self.columns = columns
        self.values = []
        for v in values:
            # 如果是字符串，那么value值应该加单引号
            if isinstance(v, str):
                self.values.append("'" + v + "'")
            # 数字需要转为字符串方便后面拼接，但是不用加单引号
            else:
                self.values.append(str(v))

    def build(self) -> str:
        self.sql = "INSERT INTO {} ({}) value ({})".format(self.table, " , ".join(self.columns),
                                                           " , ".join(self.values))
        self.sql += ";"
        return self.sql
