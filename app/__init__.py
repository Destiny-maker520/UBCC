from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import Config

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    admin = Admin(name='UBCC后台管理', template_mode='bootstrap4')
    admin.init_app(app)

    # 注册前台路由蓝图
    from .routes import bp
    app.register_blueprint(bp)

    # 注册后台管理视图（把 admin 实例传进去）
    from .admin import register_admin
    register_admin(admin)

    return app