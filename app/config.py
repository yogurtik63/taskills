class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Parol_999@localhost/istoki_api?auth_plugin=mysql_native_password&charset=utf8'
    SECRET_KEY = 'my site its very mega secret!'

    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'