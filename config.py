import os


user = 'postgres' #os.environ.get('MYSQL_USER')
password = 'kidagibu' #os.environ.get('MYSQL_PASSWORD')
server = 'localhost:5432' #os.environ.get('MYSQL_SERVER')
database = "thecompany"  #os.environ.get('MYSQL_DATABASE')


class Config:
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}' \
                              f'@{server}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #"postgresql://postgres:kidagibu@localhost:5432/trypg"