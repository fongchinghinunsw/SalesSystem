# pylint: skip-file

from app.settings import *
DEBUG = True
SECRET_KEY = "lmao_very_very_secret"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://sales:SECURE_SALES_PWD@db/sales"
SQLALCHEMY_TRACK_MODIFICATIONS = False
