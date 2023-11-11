class Configuration(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Parol_999@localhost/istoki_api?charset=utf8'
    SECRET_KEY = 'my site its very mega secret!'
    JWT_SECRET_KEY = 'jwt-secret-string'

    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'