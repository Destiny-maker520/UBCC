from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # 在函数内部创建 admin 实例
    admin = Admin(name='UBCC 后台管理', template_mode='bootstrap4')
    admin.init_app(app)

    # 注册前台路由蓝图
    from .routes import bp
    app.register_blueprint(bp)

    # 注册后台管理视图（把 admin 实例传进去）
    from .admin import register_admin
    register_admin(admin)

    # ========== 后台登录保护 ==========
    @app.before_request
    def require_admin_auth():
        # 如果访问路径以 /admin 开头，要求身份验证
        if request.path.startswith('/admin'):
            # 获取浏览器发送的用户名密码
            auth = request.authorization
            # 验证用户名和密码是否匹配
            if not auth or auth.username != app.config['BASIC_AUTH_USERNAME'] or auth.password != app.config['BASIC_AUTH_PASSWORD']:
                # 如果不匹配，返回 401 并弹出浏览器登录框
                return Response(
                    'Unauthorized',
                    401,
                    {'WWW-Authenticate': 'Basic realm="Admin Login"'}
                )
    # =========================================

    return app