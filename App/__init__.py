from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Config import config
from flask_cors import CORS
from flask_redis import FlaskRedis

app = Flask(__name__)
db = SQLAlchemy()
cors = CORS()
cache = FlaskRedis()


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    # 跨域请求
    cors.init_app(app=app, supports_credentials=True)
    # 缓存
    cache.init_app(app)
    return app
