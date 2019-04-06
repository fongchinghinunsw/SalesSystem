"""Admin blueprint views"""

from flask import render_template, session, redirect
from app.core.models.order import Order
from app.core.models.user import User
from app.core.models import db
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def Home():
  return render_template('admin/landing.html')


@app.route("/orderlist")
def OrderList():
  user = User.query.get(session['uid'])
  if user.GetType() == 1:
    orders = Order.query.order_by(Order.updated_at.desc()).all()
    return render_template("admin/order.html", orders=orders)
  return "Access denied"


@app.route("/order/<oid>/done")
def MarkOrder(oid):
  user = User.query.get(session['uid'])
  if user.GetType() == 1:
    order = Order.query.get(oid)
    order.SetStatus(2)
    db.session.commit()
    return redirect("/order/%d" % order.GetID())
  return "Access denied"
