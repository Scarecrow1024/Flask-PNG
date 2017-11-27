import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    ES_HOST = '*'
    ES_PORT = 9200
    SQLALCHEMY_RECORD_QUERIES = True

    QQ_APP_ID = '*'
    QQ_APP_KEY = '*'

    aliyun_pic_id = '*'
    aliyun_pic_pass = '*'
    aliyun_pic_bucket = '*'
    aliyun_pic_endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'

    CELERY_BROKER_URL = 'redis://localhost:6379/3'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/4'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/flaskpng'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}