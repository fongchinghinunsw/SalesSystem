# pylint: skip-file

from app.settings import *

DEBUG = True
TESTING = True
SECRET_KEY = "lmao_very_very_secret"
SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
