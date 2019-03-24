"""Admin Blueprint"""

from flask import Blueprint

bp = Blueprint(
    "admin",
    __name__,
    static_folder="static",
    static_url_path="/static/admin",
    template_folder="templates",
    url_prefix="/admin")

from . import views  #pylint: disable=wrong-import-position
