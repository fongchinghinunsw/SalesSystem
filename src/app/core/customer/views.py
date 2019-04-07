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
  return render_template('customer/landing.html')


@app.route("/order/<oid>")
def OrderDetailsPage(oid):
  """This page shows the details of the order."""
  order = Order.query.get(oid)
  if "uid" not in session:
    return redirect("/accounts/signin")
  user = User.query.get(session['uid'])
  if order is None:
    # if order doesn't exist, we can tell admin
    # but for normal users, just tell them access denied
    # otherwise normal user would know how many orders we have
    # since order id is incremental int.
    if user.GetType() == 0:
      flash("Access Denied!", "error")
      return render_template("common/base.html"), 403
    flash("Order doesn't exist", "error")
    return render_template("common/base.html"), 404

  if user.GetType() == 0 and user.GetID() != order.user.GetID():
    flash("Access Denied!", "error")
    return render_template("common/base.html"), 403

  return render_template(
      "customer/orderDetailsPage.html", order=order, usertype=user.GetType())


@app.route("/order")
def NewOrder():
  order = Order(user_id=session['uid'], status=0)
  db.session.add(order)
  db.session.commit()
  return redirect("/order/%d/menu" % order.GetID())


@app.route("/order/<oid>/menu", methods=["GET", "POST"])
def OrderMenuPage(oid):
  """This page allows ordering root items and customizing ingredient group"""
  order = Order.query.get(oid)
  if order is None or order.user.GetID() != session['uid']:
    flash("Access Denied!", "error")
    return render_template("common/base.html"), 403

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
        header="Menu")
  ig = IngredientGroup.query.get(igdetails['id'])
  return render_template(
      "customer/menu.html",
      order=order,
      items=ig.options,
      path=igdetails['path'],
      header="Choose %s for %s" % (ig.name, igdetails['item_name']))

@app.route("/order/<oid>/checkout", methods=["GET", "POST"])
def OrderCheckout(oid):
  if request.method == "GET":
    order = Order.query.get(oid)
    order.setStatus(0)
    return render_template("/customer/checkout.html", order = order)
  return redirect("/order/%d" % int(oid))
