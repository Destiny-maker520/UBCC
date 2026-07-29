from flask import Flask, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'ubcc-admin-secret-key'  # 需要设置 session 密钥

    db.init_app(app)

    admin = Admin(name='UBCC 后台管理', template_mode='bootstrap4')
    admin.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    from .admin import register_admin
    register_admin(admin)

    # ===== 修改认证逻辑 =====
    @app.before_request
    def require_admin_auth():
        # 排除登录页面本身和静态资源
        if request.path.startswith('/admin') and not request.path.startswith('/admin/login'):
            if not session.get('admin_logged_in'):
                return redirect(url_for('main.admin_login'))
    # ========================

    return app