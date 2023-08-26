from typing import Optional
from settings import default_password
from entity import User
from util import encrypt


# noinspection PyShadowingBuiltins
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
    def get_user_by_id(id: int) -> Optional[User]:
        return User.get_by_id(id)

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
    def insert(username: str, permission: int = 1) -> bool:
        """
        :param username: 用户名
        :param permission: 权限，默认值 1
        :return: 是否创建成功
        """
        user, created = User.get_or_create(username=username, password=encrypt(default_password), permission=permission)
        return created

    @staticmethod
    def update_password(id: int, new_password: str) -> None:
        User.update(password=encrypt(new_password)).where(User.id == id).execute()

    @staticmethod
    def reset_password(id: int) -> None:
        UserMapper.update_password(id=id, new_password=default_password)

    @staticmethod
    def update_permission(id: int, permission: int) -> None:
        User.update(permission=permission).where(User.id == id).execute()

    @staticmethod
    def delete_by_id(id: int) -> None:
        User.delete_by_id(id)

    @staticmethod
    def delete_by_name(username: str) -> None:
        User.delete().where(User.username == username).execute()

    @staticmethod
    def delete_instance(user: User) -> None:
        user.delete_instance()
