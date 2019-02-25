import os
basedir = os.path.abspath(os.path.dirname(__file__))


# 基类
class Config:
    SECRET_KEY = 'one more seconds'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flask]'
    FLASKY_MAIL_SENDER = 'Flask Admin'
    FLASKY_ADMIN = ['16130120129']
    QINIU_AK = 'L5hqPtAUVS6Xe9UwxFO6WIw64_O6kpQhWByXVf'
    QINIU_SK = 'gFkEghbNYGMBSdPZ1I8EaH50pbpDRwDUCkfzqH2H'
    @staticmethod
    def init_app(app):
        pass


# 开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')  # 我本机的测试数据库,暂时使用sqlite


# 测试环境
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@39.105.64.7:3306/GuoChuangTest'
    REDIS_URL = "redis://:123456@39.105.64.7:6379/1"
    AVATAR_BUCKET = 'avatar'
    AVATAR_NAMESPACE = 'http://pm0u1c1yp.bkt.clouddn.com'
    PICTURE_BUCKET = 'picture'
    PICTURE_NAMESPACE = 'http://pm6sz0oub.bkt.clouddn.com'

    star_cache = 'blog_star'

# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/GuoChuang'

# 设置一个config 字典中,注册了不同的配置环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}