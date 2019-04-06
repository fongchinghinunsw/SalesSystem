"""Customer blueprint views"""

import json
from flask import render_template
from app.core.models.order import Order
from app.core.helpers.order import GetDetailsString
from . import bp as app  # Note that app = blueprint, current_app = flask context

@app.route("/")
def Home():
  return render_template('customer/landing.html')


@app.route("/order/<oid>")
def OrderDetailsPage(oid):
  """This page shows the details of the order."""
  order = Order.query.get(oid)
  content = json.loads(order.content)
  details = ""
  for item in content:
    details += GetDetailsString(item)

  return render_template(
      "customer/orderDetailsPage.html", order=order, details=details)
