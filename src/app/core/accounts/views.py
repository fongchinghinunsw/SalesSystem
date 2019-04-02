"""Accounts blueprint views"""

from . import bp as app  # Note that app = blueprint, current_app = flask context
from flask import render_template


@app.route("/")
def home():
  return render_template('accounts/landing.html')
