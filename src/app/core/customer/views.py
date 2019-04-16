"""Customer blueprint views"""

from flask import render_template, request, session, redirect, flash
from app.core.models.inventory import IngredientGroup
from app.core.models.order import Order, OrderStatus
from app.core.models.inventory import Item
from app.core.models.user import User, UserType
from app.core.models import db
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def Home():
  if 'uid' in session:
    user = User.query.get(session['uid'])
    return render_template(
        'customer/landing.html',
        user=user,
        isadmin=(user.GetType() == UserType.ADMIN))
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
    if user.GetType() == UserType.CUSTOMER:
      flash("Wrong order ID", "error")
      return redirect("/")
    flash("Order doesn't exist", "error")
    return render_template("common/base.html"), 404

  if user.GetType() == UserType.CUSTOMER:
    if user.GetID() != order.user.GetID(
    ) or order.status == OrderStatus.CREATED:
      flash("Wrong order ID", "error")
      return redirect("/")

  return render_template(
      "customer/orderDetailsPage.html",
      order=order,
      isadmin=(user.GetType() == UserType.ADMIN))


@app.route("/order")
def NewOrder():
  order = Order(user_id=session['uid'], status=OrderStatus.CREATED, price=0)
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
  order.DeductStock()
  # WARNING: DON'T COMMIT DB AFTER THIS
  # this is to avoid the scenario where
  # we have stock for 3 cokes, and the user orders 5 separate ones
  # in this case we won't be able to tell coke is out of stock
  # we can only tell customer that we are out of stock when he/she checks out
  #
  # this is a hacky fix toward this issue for better user experience

  if igdetails is None:
    items = Item.query.filter(Item.root).all()
    return render_template(
        "customer/menu.html",
        order=order,
        items=items,
        path="root",
        header="Menu",
        showcheckout=True,
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
      showcheckout=False,
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
  try:
    order.Pay()
  except ValueError as e:
    flash("Something went wrong: " + str(e), "error")
    return render_template("/customer/checkout.html", order=order)
  except RuntimeError as e:
    flash("Something went wrong: " + str(e), "error")
    return render_template("/customer/checkout.html", order=order)
  db.session.commit()
  return redirect("/order/%d" % int(oid))
