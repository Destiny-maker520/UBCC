from flask import Flask, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'ubcc-2026-orientation-camp-secret-key'

    db.init_app(app)

    admin = Admin(name='UBCC 后台管理', template_mode='bootstrap4')
    admin.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    from .admin import register_admin
    register_admin(admin)

    # ============================================================
    # 整站强制登录（所有页面都需要先登录）
    # ============================================================
    @app.before_request
    def require_login():
        # 白名单：登录页面本身和静态资源不需要登录
        allowed_paths = ['/login', '/static']
        if request.path.startswith(tuple(allowed_paths)):
            return None

        # 如果未登录，跳转到登录页面
        if not session.get('logged_in'):
            return redirect(url_for('main.login'))

    # ============================================================
    # 后台管理认证（/admin 需要额外验证）
    # ============================================================
    @app.before_request
    def require_admin_auth():
        # 只保护 /admin 开头的路径（但排除 /admin/login）
        if request.path.startswith('/admin') and not request.path.startswith('/admin/login'):
            if not session.get('admin_logged_in'):
                return redirect(url_for('main.admin_login'))

    return app