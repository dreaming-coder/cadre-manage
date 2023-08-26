from typing import Optional

from entity import User
from util import encrypt


class UserMapper:

    @staticmethod
    def check_password(username: str, password: str) -> bool:
        user = UserMapper.get_user_by_name(username)
        if user is not None:
            return user.password == encrypt(password)
        return False

    @staticmethod
    def is_admin(username: str) -> bool:
        """是否是管理员"""
        return User.select().where((User.username == username) & (User.permission == 0)).exists()

    @staticmethod
    def get_user_by_id(pk: int) -> Optional[User]:
        return User.get_by_id(pk)

    @staticmethod
    def get_user_by_name(username: str) -> Optional[User]:
        """
        :param username: 用户名
        :return: 查到的实例，不存在则返回 None
        """
        query = User.select().where(User.username == username)
        if query.exists():
            return query.get()
        else:
            return None

    @staticmethod
    def get_all_users() -> list[User]:
        return [user for user in User.select()]

    @staticmethod
    def insert(username: str, password: str, permission: int = 1) -> bool:
        """
        :param username: 用户名
        :param password: 密码
        :param permission: 权限，默认值 1
        :return: 是否创建成功
        """
        user, created = User.get_or_create(username=username, password=encrypt(password), permission=permission)
        return created

    @staticmethod
    def update_password(username: str, new_password: str) -> None:
        User.update(password=encrypt(new_password)).where(User.username == username).execute()

    @staticmethod
    def delete_by_pk(pk: int) -> None:
        User.delete_by_id(pk)

    @staticmethod
    def delete_by_name(username: str) -> None:
        User.delete().where(User.username == username).execute()

    @staticmethod
    def delete_instance(user: User) -> None:
        user.delete_instance()
