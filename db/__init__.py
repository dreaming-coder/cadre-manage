import functools
import hashlib
import importlib
import inspect
import json
from datetime import datetime
from sqlite3 import register_adapter, register_converter

from peewee import SqliteDatabase, Model

from entity import User
from settings import database, admin_username, default_password
from util import ComplexEncoder
from .adapter import adapt_datetime, adapt_date, adapt_time
from .converter import convert_datetime, convert_date, convert_time

db = SqliteDatabase(database=database)

__all__ = [
    "table_name",
    "init_db",
]


def table_name(name, **kwargs):
    """
    给实体类设置表名，并设置数据库连接对象
    :param name: 表名
    """

    def wrap(cls):
        if issubclass(cls, Model):
            cls._meta.database = db
            cls._meta.table_name = name

            def obj2json(self):
                fields_map = {}
                for field in self.__data__.keys():
                    fields_map[field] = getattr(self, field)
                return json.dumps(fields_map, cls=ComplexEncoder, **kwargs)

            def obj_print(self):
                result = "\033[36;1m" + cls.__name__ + "\033[0m(\n"
                for field in self.__data__.keys():
                    result += f"    \033[32;1m{field}\033[0m=\033[31;1m{getattr(self, field)}\033[0m\n"
                result += ")"

                return result

            cls.__str__ = functools.wraps(cls.__str__)(obj_print)
            cls.json = obj2json
        return cls

    return wrap


register_adapter(datetime, adapt_datetime)
register_adapter(datetime, adapt_date)
register_adapter(datetime, adapt_time)

register_converter("datetime", convert_datetime)
register_converter("date", convert_date)
register_converter("time", convert_time)


def init_admin():
    """
    初始化管理员密码
    """
    md5 = hashlib.md5()
    md5.update(default_password.encode("utf-8"))
    admin = User(username=admin_username, password=md5.hexdigest(), permission=0)
    admin.save()


def init_db():
    """
    初始化数据库
    """
    try:
        db.connect()
        # 动态获取指定模块
        module = importlib.import_module("entity")
        # 动态获取指定模块的所有类，返回值是列表，每个元素是元祖：(类名: str，类本身: class)
        class_list = inspect.getmembers(module, inspect.isclass)
        tables = list(zip(*class_list))[1]
        db.create_tables(tables)
        init_admin()
    except Exception as e:
        print(e)
    finally:
        db.close()


def __reset_db():
    """
    重置数据库
    """
    try:
        db.connect()
        module = importlib.import_module("entity")
        class_list = inspect.getmembers(module, inspect.isclass)
        tables = list(zip(*class_list))[1]
        db.drop_tables(tables)
        db.create_tables(tables)
        init_admin()
    except Exception as e:
        print(e)
    finally:
        db.close()


if __name__ == '__main__':
    __reset_db()
