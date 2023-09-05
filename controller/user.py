from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from mapper import userMapper

__all__ = [
    "user_bp"
]

user_bp = Blueprint("user", __name__, url_prefix="/user")

"""个人操作"""


@user_bp.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user, checked = userMapper.check_password(username, password)

    if checked:
        access_token = create_access_token(
            identity={
                "user_id": user.id,
                "username": user.username,
                "permission": user.permission
            }
        )
        return jsonify(access_token=access_token)
    else:
        return jsonify("用户名或密码错误")


@user_bp.route("/check_admin", methods=["GET"])
@jwt_required()
def check_admin():
    """判断当前登录用户是否是管理员"""
    user_info = get_jwt_identity()
    return jsonify({"is_admin": user_info["permission"] <= 0})


# noinspection PyBroadException
@user_bp.route("/modify_password", methods=["POST"])
@jwt_required()
def modify_password():
    """修改密码"""
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    user_info = get_jwt_identity()
    user, checked = userMapper.check_password(user_info["username"], old_password)
    if checked:
        userMapper.update_password(user_info["user_id"], old_password, new_password)
        return jsonify({"msg": "修改成功"})
    else:
        return jsonify({"msg": "原密码错误，修改失败！"})


"""管理员操作"""


@user_bp.route("/is_admin/<username>", methods=["GET"])
@jwt_required()
def is_admin(username):
    return jsonify({"is_admin": userMapper.is_admin(username)})


@user_bp.route("/list", methods=["POST"])
@jwt_required()
def get_users():
    user_info = get_jwt_identity()
    users = userMapper.get_all_users()
    users = [user for user in users if user.permission > user_info["permission"]]
    return jsonify(users)


@user_bp.route("/create", methods=["POST"])
@jwt_required()
def create_user():
    user_info = get_jwt_identity()
    if user_info["permission"] > 0:
        return jsonify({"msg": "权限不足"})

    username = request.form.get("username")
    permission = int(request.form.get("permission"))

    if permission <= user_info["permission"]:
        return jsonify({"msg": "权限不足"})

    user, created = userMapper.insert(username=username, permission=permission)
    if created:
        return jsonify({"user": user})
    else:
        return jsonify({"msg": "创建失败"})


@user_bp.route("/update_permission/<int:permission>", methods=["GET"])
@jwt_required()
def update_permission(permission):
    user_info = get_jwt_identity()
    """
    1. 当前用户不具备管理员权限，禁止更新
    2. 当前用户是管理员但不是超级管理员，禁止更新
    """
    if user_info["permission"] != 0 or user_info["permission"] > permission:
        return jsonify({"msg": "权限不足"})

    userMapper.update_permission(user_info["user_id"], permission=permission)
    return jsonify({"msg": "权限修改成功"})


# noinspection DuplicatedCode
@user_bp.route("/reset/<int:user_id>", methods=["GET"])
@jwt_required()
def reset_password(user_id):
    user_info = get_jwt_identity()
    if user_info["user_id"] == user_id:
        return jsonify({"msg": "权限不足"})

    user = userMapper.get_user_by_id(user_id)
    if user_info["permission"] > 0 or user_info["permission"] >= user.permission:
        return jsonify({"msg": "权限不足"})

    userMapper.reset_password(user_id)
    return jsonify({"msg": "重置成功"})


# noinspection DuplicatedCode
@user_bp.route("/delete/<int:user_id>", methods=["GET"])
@jwt_required()
def delete_user(user_id):
    user_info = get_jwt_identity()
    if user_info["user_id"] == user_id:
        return jsonify({"msg": "权限不足"})

    user = userMapper.get_user_by_id(user_id)
    if user_info["permission"] > 0 or user_info["permission"] >= user.permission:
        return jsonify({"msg": "权限不足"})

    userMapper.delete_by_id(user_id)
    return jsonify({"msg": "删除成功"})
