import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50

    @staticmethod
    def init_app(app):
        app['SECRET_KEY'] = os.environ.get(
            'SECRET_KEY') or 'hard to guess string'
        app['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app['MAIL_SERVER'] = 'smtp.163.com'
        app['MAIL_PORT'] = 25
        app['MAIL_USE_TLS'] = True
        app['MAIL_USERNAME'] = os.environ.get(
            'MAIL_USERNAME')
        app['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
        app['FLASKY_MAIL_SUBJECT_PREFIX'] = '[RWL]'
        app['FLASKY_MAIL_SENDER'] = 'RWL Admin <eclipse_sv@163.com>'
        app['FLASKY_ADMIN'] = os.environ.get('RWL')
        app['FLASKY_POSTS_PER_PAGE'] = 20
        app['FLASKY_FOLLOWERS_PER_PAGE'] = 50
        return app
