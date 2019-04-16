import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.urandom(24)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    host = '0.0.0.0'
    port = 18081


class TestingConfig(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    port = 18081


config = {
    'development': DevelopmentConfig,
    'test': TestingConfig
}
