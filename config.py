class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'emailengine!'
    DB_NAME = 'local.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'robinmishra413@gmail.com'
    MAIL_DEFAULT_SENDER = 'robinmishra413@gmail.com'
    MAIL_PASSWORD = 'vsdaqawdsaupxmmv'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
