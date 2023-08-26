from datetime import datetime

from peewee import Model, IntegerField, TextField, DateTimeField

from db import table_name

__all__ = [
    "User"
]


@table_name("user")
class User(Model):
    """
    username：用户名
    password：密码的 hash 值
    permission：用户权限，0 是管理员，1 是普通查看权限，其他值待定具体权限
    create_datetime：账号开通时间
    last_login_datetime：上次登录时间
    deleted：是否删除，0 表示正常用户，1 表示删除
    """
    username = TextField(unique=True)
    password = TextField()
    permission = IntegerField(default=1)
    create_datetime = DateTimeField(default=datetime.now(), formats="%Y-%m-%d %H:%M:%S")
    last_login_datetime = DateTimeField(null=True, formats="%Y-%m-%d %H:%M:%S")
    deleted = IntegerField(default=0)
