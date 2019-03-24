"""Core module for sales system"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config_filename):
  """Create flask app

  Create flask app based on given configuration

  Arguments:
    config_filename: String, path to config file
  """
  app = Flask(__name__)
  app.config.from_object(config_filename)

  SQLAlchemy(app)

  from app.core.accounts import bp as accounts_bp
  from app.core.admin import bp as admin_bp
  from app.core.customer import bp as customer_bp

  app.register_blueprint(accounts_bp)
  app.register_blueprint(admin_bp)
  app.register_blueprint(customer_bp)

  return app
