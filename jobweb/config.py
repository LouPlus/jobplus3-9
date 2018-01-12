class BaseConfig(object):
    SECRET_KEY = ''

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass


configs = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'testing' : TestingConfig
}
