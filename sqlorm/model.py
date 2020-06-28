import typing

from utils.log import Logger

from MySQLdb.compat import StandardError
from sqlorm.field import Field
from sqlorm.orm import select, execute

log = Logger('../log/orm.log', level='error')

OPERATION_MSG = dict(
    ge='>=',
    gt='>',
    le='<=',
    lt='<'
)
# ge表示大于等于,le表示小于等于,gt表示大于,lt表示小于
VALID_OPERATION = ("=", "!=", "ge", "gt", "le", "lt", "in", "not in", "like", "not like")


def get__operation_from_key(key: str) -> typing.Tuple[str, str]:
    ops_list = key.split("__")
    if len(ops_list) < 2:
        return ops_list[0], '='
    else:
        ops = ops_list[1].replace('_', ' ')
        if ops not in VALID_OPERATION:
            raise KeyError
        # 如果是 <, > ,<= ,>=这四个符号，则需要进行转换
        if ops in OPERATION_MSG:
            ops = OPERATION_MSG[ops]
        return ops_list[0], ops


class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        table_name = attrs.get('__table__', None) or name
        log.logger.info('found model: %s (table: %s)' % (name, table_name))
        mappings = dict()
        fields = []
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                log.logger.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primary_key:
                        raise StandardError('Duplicate primary key for field: %s' % k)
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise StandardError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primary_key, ', '.join(escaped_fields), table_name)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            table_name, ', '.join(escaped_fields), primary_key, ','.join(["'%s'"] * (len(escaped_fields) + 1)))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            table_name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primary_key)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (table_name, primary_key)
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def __get__args(self) -> list:
        args = []
        for key in self.__fields__:
            args.append(self.get_value_or_default(key))
        return args

    def get_value(self, key):
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        # 获取属性值
        value = getattr(self, key, None)
        # 如果找不到对应的值，先获取key(Field类型)，判断是否在Filed字段中设置默认值，有的话就用默认值替换
        if value is None:
            field = self.__mappings__[key]
            # 如果不存在则用默认值替代
            if field.default is not None:
                # 如果default是一个函数则直接调用函数，如果是值对象则直接赋值
                value = field.default() if callable(field.default) else field.default
                log.logger.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    def filter(cls, pk=None, order_by=None, order_by_decs=None, size: int = None, **kw):
        ' find objects by where clause.'
        sql = [cls.__select__]
        # 如果存在主键，则直接按照主键进行搜索
        if pk:
            rs = select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
            return cls(**rs[0])
        args = []
        # 相等的键值对，key是属性，value属性值
        if kw:
            sql.append('where')
            first = True
            for k, v in kw.items():
                try:
                    k, ops = get__operation_from_key(k)
                    if first:
                        sql.append(" %s %s " % (k, ops) + " '%s' ")
                        first = False
                    else:
                        sql.append(" and %s %s " % (k, ops) + " '%s' ")
                    args.append(v)
                except Exception as e:
                    log.logger.error(e)
        if order_by:
            sql.append("order by %s")
            if isinstance(order_by, list):
                args.append(','.join(order_by))
            else:
                args.append(order_by)
        elif order_by_decs:
            sql.append("order by %s desc")
            if isinstance(order_by_decs, list):
                args.append(','.join(order_by_decs))
            else:
                args.append(order_by_decs)
        rs = select(' '.join(sql), args, size)
        # 把dict 转为 object类型
        return [cls(**r) for r in rs]

    @classmethod
    def query(cls, sql: str):
        rs = select(sql)

    def save(self):
        # 获取参数
        args = self.__get__args()
        # 获取主键,filed存放的是非主键元素
        args.append(self.get_value_or_default(self.__primary_key__))
        # 返回执行结果
        rows = execute(self.__insert__, args)
        if rows != 1:
            log.logger.warning('failed to insert record: affected rows: %s' % rows)

    def update(self):
        args = self.__get__args()
        args.append(self.getValue(self.__primary_key__))
        # rows = await execute(self.__update__, args)
        rows = execute(self.__update__, args)
        if rows != 1:
            log.logger.warning('failed to update by primary key: affected rows: %s' % rows)

    def remove(self):
        args = [self.getValue(self.__primary_key__)]
        # rows = await execute(self.__delete__, args)
        rows = execute(self.__delete__, args)
        if rows != 1:
            log.logger.warning('failed to remove by primary key: affected rows: %s' % rows)
