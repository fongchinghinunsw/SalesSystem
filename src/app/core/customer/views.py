"""Customer blueprint views"""

from flask import render_template
from app.core.models.order import Order
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def Home():
  return render_template('customer/landing.html')


@app.route("/order/<oid>")
def OrderDetailsPage(oid):
  """This page shows the details of the order."""
  order = Order.query.get(oid)

  return render_template("customer/orderDetailsPage.html", order=order)
