import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
server = os.environ.get('MYSQL_SERVER')
database = os.environ.get('MYSQL_DATABASE')
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Default app configuration

    """
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}' \
                              f'@{server}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # "postgresql://postgres:kidagibu@localhost:5432/trypg"
    #SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/dbname[?key=value&key=value...]



    DATABASE_URL = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')


class TestingConfig(object):
    """
    Testing app configuration

    """
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'thecompany_app', 'tests', 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
