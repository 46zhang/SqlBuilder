from utils.log import Logger

from MySQLdb.compat import StandardError
from sqlorm.field import Field
from sqlorm.orm import select, execute

log = Logger('../log/orm.log', level='info')


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
    def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    def find(cls, pk):
        ' find object by primary key. '
        rs = select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    def __get__args(self) -> list:
        args = []
        for key in self.__fields__:
            args.append(self.get_value_or_default(key))
        return args

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
