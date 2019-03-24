"""Customer blueprint"""

from flask import Blueprint

bp = Blueprint(
    "customer",
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/static/customer",
    url_prefix="/")

from . import views  #pylint: disable=wrong-import-position
