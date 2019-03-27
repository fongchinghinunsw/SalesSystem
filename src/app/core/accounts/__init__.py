"""Accounts blueprint"""

from flask import Blueprint

bp = Blueprint(
    "accounts",
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/static/accounts",
    url_prefix="/accounts")

from . import views  #pylint: disable=wrong-import-position
