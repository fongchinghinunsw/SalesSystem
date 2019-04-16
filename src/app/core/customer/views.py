"""Customer blueprint views"""

from flask import render_template, request, session, redirect, flash
from app.core.models.inventory import IngredientGroup
from app.core.models.order import Order
from app.core.models.inventory import Item
from app.core.models.user import User
from app.core.models import db
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def Home():
  if 'uid' in session:
    user = User.query.get(session['uid'])
    return render_template('customer/landing.html', user=user)
  return render_template('customer/landing.html')


@app.route("/order/check", methods=['POST'])
def RedirectToOrderDetails():
  if 'oid' not in request.form or request.form['oid'] == "":
    flash("Please enter order ID", "error")
    return redirect("/")
  return redirect("/order/%s" % request.form['oid'])


@app.route("/order/<oid>")
def OrderDetailsPage(oid):
  """This page shows the details of the order."""
  order = Order.query.get(oid)
  if "uid" not in session:
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if order is None:
    if user.GetType() == 0:
      flash("Wrong order ID", "error")
      return redirect("/")
    flash("Order doesn't exist", "error")
    return render_template("common/base.html"), 404

  if user.GetType() == 0 and user.GetID() != order.user.GetID():
    flash("Wrong order ID", "error")
    return redirect("/")

  return render_template(
      "customer/orderDetailsPage.html", order=order, usertype=user.GetType())


@app.route("/order")
def NewOrder():
  order = Order(user_id=session['uid'], status=0, price=0)
  db.session.add(order)
  db.session.commit()
  return redirect("/order/%d/menu" % order.GetID())


@app.route("/order/<oid>/menu", methods=["GET", "POST"])
def OrderMenuPage(oid):
  """This page allows ordering root items and customizing ingredient group"""
  order = Order.query.get(oid)
  if order is None or order.user.GetID() != session['uid']:
    flash("Wrong order ID. Do you want to create an order instead?", "error")
    return redirect("/")

  try:
    if request.method == "POST":
      path = request.form['path']
      items = list(map(int, request.form.getlist('items')))
      numbers = list(map(int, request.form.getlist('numbers')))
      if path == "root":
        for idx, item in enumerate(items):
          if numbers[idx] > 0:
            order.AddRootItem(item, numbers[idx])
      else:
        order.AddIG(path, items, numbers)
      db.session.commit()
  except ValueError as e:
    flash(str(e), "error")
  except RuntimeError as e:
    flash(str(e), "error")

  igdetails = order.GetUnfulfilledIGDetails()
  if igdetails is None:
    items = Item.query.filter(Item.root).all()
    return render_template(
        "customer/menu.html",
        order=order,
        items=items,
        path="root",
        header="Menu",
        style="multi")
  ig = IngredientGroup.query.get(igdetails['id'])
  style = "pickone" if ig.GetMinOption() == 1 and ig.GetMaxOption(
  ) == 1 and ig.GetMinItem() == 1 and ig.GetMaxItem() == 1 else "multi"
  return render_template(
      "customer/menu.html",
      order=order,
      items=ig.options,
      path=igdetails['path'],
      header="Choose %s for %s" % (ig.name, igdetails['item_name']),
      style=style)


@app.route("/order/<oid>/checkout", methods=["GET", "POST"])
def OrderCheckout(oid):
  """Display checkout page of an order"""
  order = Order.query.get(oid)
  if order is None or order.user.GetID() != session['uid']:
    flash("Wrong order ID. Do you want to create an order instead?", "error")
    return redirect("/")
  if request.method == "GET":
    return render_template("/customer/checkout.html", order=order)
  order.Pay()
  db.session.commit()
  return redirect("/order/%d" % int(oid))
