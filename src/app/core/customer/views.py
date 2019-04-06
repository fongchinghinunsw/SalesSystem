"""Customer blueprint views"""

from flask import render_template, request
from app.core.models.inventory import IngredientGroup
from app.core.models.order import Order
from app.core.models.inventory import Item
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def Home():
  return render_template('customer/landing.html')


@app.route("/order/<oid>")
def OrderDetailsPage(oid):
  """This page shows the details of the order."""
  order = Order.query.get(oid)

  return render_template("customer/orderDetailsPage.html", order=order)


@app.route("/order")
def NewOrder():
  order = Order(user_id=session['uid'], status=0)
  db.session.add(order)
  db.session.commit()
  return redirect("/order/%d/menu" % order.GetID())


@app.route("/order/<oid>/menu", methods=["GET", "POST"])
def OrderMenuPage(oid):
  """This page allows ordering the main."""
  order = Order.query.get(oid)
  if order.user.GetID() != session['uid']:
    return "Access denied"

  if request.method == "POST":
    items = request.form.getlist('items')
    numbers = request.form.getlist('numbers')
    for idx, item in enumerate(items):
      if numbers[idx] > 0:
        order.AddRootItem(item, numbers[idx])
    db.session.commit()
    return redirect("/order/<oid>/configure" % order.id)
  items = Item.query.filter(root=True).all()
  return render_template("/customer/menu.html", items=items)


@app.route("/order/<oid>/configure", methods=['GET', 'POST'])
def IGConfPage(oid):
  order = Order.query.get(oid)
  if order.user.GetID() != session['uid']:
    return "Access denied"

  if request.method == 'POST':
    path = request.form['path']
    items = request.form.getlist('items')
    numbers = request.form.getlist('numbers')
    order.AddIG(path, items, numbers)
    db.session.commit()

  igdetails = order.GetUnfulfilledIGDetails()
  if igdetails is None:
    return redirect("/order/%d/menu" % oid)
  ig = IngredientGroup.query.get(igdetails['id'])
  return render_template(
      "customer/ig.html",
      ig=ig,
      path=igdetails['path'],
      item_name=igdetails['item_name'])
