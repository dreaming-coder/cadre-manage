import hashlib
import importlib

from peewee import SqliteDatabase, Model
import inspect

from entity import User
from settings import database, admin_username, default_password

db = SqliteDatabase(database=database)

__all__ = [
    "table_name",
    "init_db",
    "reset_db"
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
        return cls

    return wrap


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


def reset_db():
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
    reset_db()
