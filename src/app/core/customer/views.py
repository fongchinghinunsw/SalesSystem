"""Customer blueprint views"""

from flask import render_template, session, redirect
from app.core.models.order import Order
from app.core.models.user import User
from . import bp as app  # Note that app = blueprint, current_app = flask context

@app.route("/")
def Home():
  return render_template('customer/landing.html')


@app.route("/order/<oid>")
def OrderDetailsPage(oid):
  """This page shows the details of the order."""
  order = Order.query.get(oid)
  if "uid" not in session:
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if user.GetType() == 0 and user.GetID() != order.user.GetID():
    return "Access Denied!"

  return render_template(
      "customer/orderDetailsPage.html", order=order, usertype=user.GetType())
