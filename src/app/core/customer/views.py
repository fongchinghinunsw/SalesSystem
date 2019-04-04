"""Customer blueprint views"""

import json
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
  content = json.loads(order.content)
  details = ""
  for item in content:
    details += GetDetailsString(item)

  return render_template(
      "customer/orderDetailsPage.html", order=order, details=details)


def GetDetailsString(item, prefix=""):
  """Recursively get the details string for an order item node
  for invoice and order details"""
  ret = ""
  if item["type"] == "ig":
    prefix += item["name"] + ":"
    for child in item["options"]:
      ret += GetDetailsString(child, prefix)
  else:
    ret = "%s%s%s ......$%.2f\n" % (prefix, item['name'], "*%d" % item['num']
                                    if item['num'] > 1 else "", item['price'])

    prefix = (len(prefix) - len(prefix.lstrip()) + 2) * " "
    for child in item["igs"]:
      ret += GetDetailsString(child, prefix)
  return ret
