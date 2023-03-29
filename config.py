class Config:
    SECRET_KEY = 'my-secret-key'
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = 'jwt-secret-key'


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    JWT_ACCESS_TOKEN_EXPIRES = False


class TestConfig(Config):
    TESTING = True
    JWT_ACCESS_TOKEN_EXPIRES = False