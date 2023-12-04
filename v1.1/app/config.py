username = 'root'
password = 'Parol999'
link = 'localhost/delivery'


class Configuration(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{username}:{password}@{link}?charset=utf8'
    SECRET_KEY = 'my site its very mega secret!'
    JWT_SECRET_KEY = 'jwt-secret-string'

    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'