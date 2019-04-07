"""Admin blueprint views"""

from flask import render_template, session, redirect, flash
from app.core.models.order import Order
from app.core.models.user import User
from app.core.models import db
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def Home():
  return render_template('admin/landing.html')


@app.route("/orderlist")
def OrderList():
  """Display list of current oders"""
  if 'uid' not in session:
    flash("Please sign in first", "error")
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if user.GetType() == 1:
    orders = Order.query.filter(Order.status == 1).order_by(
        Order.updated_at.desc()).all()
    return render_template("admin/order.html", orders=orders)
  flash("Access denied", "error")
  return redirect("/")


@app.route("/order/<oid>/done")
def MarkOrder(oid):
  """mark order as ready"""
  if 'uid' not in session:
    flash("Please sign in first", "error")
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if user.GetType() == 1:
    order = Order.query.get(oid)
    order.SetStatus(2)
    db.session.commit()
    return redirect("/order/%d" % order.GetID())
  flash("Access denied", "error")
  return redirect("/")
