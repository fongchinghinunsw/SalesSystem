"""Admin blueprint views"""

from flask import render_template, session, redirect, request, flash
from app.core.models.order import Order, OrderStatus
from app.core.models.user import User, UserType
from app.core.models.inventory import Stock
from app.core.models import db
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def Home():
  return render_template('admin/landing.html')


@app.route("/inventory", methods=['GET', 'POST'])
def Inventory():
  """Display list of stock or adjust stock"""
  if 'uid' not in session:
    flash("Please sign in first", "error")
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if user.GetType() == UserType.CUSTOMER:
    flash("Access denied", "error")
    return redirect("/")
  if request.method == 'GET':
    stocks = Stock.query.all()
    return render_template("admin/inventory.html", stocks=stocks)
  stock = Stock.query.get(int(request.form['id']))
  if stock is None:
    flash("Stock doesn't exist", "error")
    return redirect("/admin/inventory")
  amount = request.form.get('amount', 0)
  if amount == '':
    amount = 0
  stock.AdjustAmount(int(amount))
  db.session.commit()
  stocks = Stock.query.all()
  flash("Success!", "success")
  return redirect("/admin/inventory")


@app.route("/orderlist")
def OrderList():
  """Display list of current oders"""
  if 'uid' not in session:
    flash("Please sign in first", "error")
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if user.GetType() == UserType.CUSTOMER:
    flash("Access denied", "error")
    return redirect("/")
  orders = Order.query.filter(Order.status == OrderStatus.PAID).order_by(
      Order.updated_at.desc()).all()
  return render_template("admin/orderlist.html", orders=orders)


@app.route("/order/<oid>/done")
def MarkOrder(oid):
  """mark order as ready"""
  if 'uid' not in session:
    flash("Please sign in first", "error")
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if user.GetType() == UserType.CUSTOMER:
    flash("Access denied", "error")
    return redirect("/")
  order = Order.query.get(oid)
  order.SetStatus(OrderStatus.READY)
  db.session.commit()
  return redirect("/order/%d" % order.GetID())


@app.route("/join", methods=["GET", "POST"])
def BecomeAdmin():
  """set user type to admin with correct password"""
  if 'uid' not in session:
    flash("Please sign in first", "error")
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if user.GetType() == UserType.ADMIN:
    flash("You are already admin", "error")
    return redirect("/admin/orderlist")
  if request.method == 'POST':
    if request.form.get('password', '') == "bestburger":
      user.SetType(UserType.ADMIN)
      db.session.commit()
      flash("You are admin now", "success")
      return redirect("/admin/orderlist")
    flash("Wrong password", "error")
  return render_template("admin/join.html")
