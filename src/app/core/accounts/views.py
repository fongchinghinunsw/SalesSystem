"""Accounts blueprint views"""

from flask import render_template
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def home():
  return render_template('accounts/landing.html')
