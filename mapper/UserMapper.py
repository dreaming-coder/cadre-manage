from typing import Optional

from config import Config
from entity import User
from util import encrypt


# noinspection PyShadowingBuiltins
class UserMapper:

    @staticmethod
    def check_password(username: str, password: str) -> tuple[Optional[User], bool]:
        user = UserMapper.get_user_by_name(username)
        if user is not None and user.deleted == 0 and user.password == encrypt(password):
            return user, True
        return None, False

    @staticmethod
    def is_admin(username: str) -> bool:
        """是否是管理员"""
        return User.select().where((User.username == username) & (User.permission <= 0)).exists()

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
        return [user for user in User.select() if user.permission >= 0]

    @staticmethod
    def insert(username: str, permission: int = 1) -> tuple[User, bool]:
        """
        :param username: 用户名
        :param permission: 权限，默认值 1
        :return: 是否创建成功
        """
        user, created = User.get_or_create(username=username, password=encrypt(Config["default_password"]),
                                           permission=permission)
        return user, created

    @staticmethod
    def update_password(id: int, old_password: Optional[str], new_password: str) -> bool:
        user = User.get_by_id(id)
        if old_password is not None and user.password != encrypt(old_password):
            return False
        else:
            User.update(password=encrypt(new_password)).where(User.id == id).execute()
            return True

    @staticmethod
    def reset_password(id: int) -> None:
        UserMapper.update_password(id=id, old_password=None, new_password=Config["default_password"])

    @staticmethod
    def update_permission(id: int, permission: int) -> None:
        User.update(permission=permission).where(User.id == id).execute()

    @staticmethod
    def delete_by_id(id: int) -> None:
        User.update(deleted=1).where(User.id == id).execute()

    @staticmethod
    def delete_by_name(username: str) -> None:
        User.update(deleted=1).where(User.username == username).execute()

    @staticmethod
    def delete_instance(user: User) -> None:
        User.update(deleted=1).where(User.id == user.id).execute()


userMapper = UserMapper()
