import functools
import hashlib
import importlib
import inspect
from datetime import datetime
from sqlite3 import register_adapter, register_converter

from peewee import SqliteDatabase, Model

import entity
from settings import database, admin_username, default_password
from util import encrypt
from .adapter import adapt_datetime, adapt_date, adapt_time
from .converter import convert_datetime, convert_date, convert_time

db = SqliteDatabase(database=database)

__all__ = [
    "table_name",
    "reset_db",
]


def table_name(name):
    """
    给实体类设置表名，并设置数据库连接对象
    :param name: 表名
    """

    def wrap(cls):
        if issubclass(cls, Model):
            cls._meta.database = db
            cls._meta.table_name = name

            def obj_dict(self):
                fields_map = {}
                for field in self.__data__.keys():
                    fields_map[field] = getattr(self, field)
                return fields_map

            def obj_print(self):
                result = "\033[36;1m" + cls.__name__ + "\033[0m(\n"
                for field in self.__data__.keys():
                    result += f"    \033[32;1m{field}\033[0m=\033[31;1m{getattr(self, field)}\033[0m\n"
                result += ")"

                return result

            cls.__str__ = functools.wraps(cls.__str__)(obj_print)
            cls.json = obj_dict
        return cls

    return wrap


register_adapter(datetime, adapt_datetime)

register_converter("datetime", convert_datetime)


def init_admin():
    """
    初始化管理员密码
    """
    admin = entity.User(username=admin_username, password=encrypt("123456"), permission=0)
    admin.save()


def init_tables():
    try:
        db.connect()
        # 动态获取指定模块
        module = importlib.import_module("entity")
        # 动态获取指定模块的所有类，返回值是列表，每个元素是元祖：(类名: str，类本身: class)
        class_list = inspect.getmembers(module, inspect.isclass)
        tables = list(zip(*class_list))[1]
        db.create_tables(tables)
    except Exception as e:
        print(e)
    finally:
        db.close()


def reset_db():
    """
    初始化数据库
    """
    init_tables()
    init_admin()


if __name__ == '__main__':
    reset_db()
