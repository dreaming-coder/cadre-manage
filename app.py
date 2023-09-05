from datetime import timedelta

from flask import Flask, redirect
from flask_jwt_extended import JWTManager

from config import Config
from controller import user_bp
from db import reset_db
from util import ComplexEncoder

app = Flask(__name__)
app.json_encoder = ComplexEncoder
app.config.from_mapping(Config)

# JWT  配置
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# 初始化JWT
jwt = JWTManager(app)

# 初始化数据库
reset_db()

# 注册分组视图
app.register_blueprint(user_bp)


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    """过期重新登陆"""
    return redirect("/user/login")


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    """未授权的重定向"""
    return redirect("/user/login")


if __name__ == '__main__':
    app.run()
