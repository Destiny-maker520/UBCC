import os
from urllib.parse import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 优先读取 Render 提供的数据库地址，如果没有则使用本地的 SQLite
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Render 的 PostgreSQL 要求使用 'postgresql' 协议
        database_url = database_url.replace('postgres://', 'postgresql://')
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'ubcc.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'UBCC-2026-OCAMP')  # 优先用环境变量