import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config(object):
    """Parent configuration class."""

    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.environ.get('SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_PORT=os.environ.get('MAIL_PORT')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    JWT_KEY=os.environ.get('JWT_KEY')
    CONFIRM_MAIL_REDIRECT_LINK=os.environ.get('CONFIRM_MAIL_REDIRECT_LINK')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
