"""Customer blueprint views"""

from flask import render_template, request
from app.core.models.inventory import IngredientGroup
from app.core.models.order import Order
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def Home():
  return render_template('customer/landing.html')


@app.route("/order/<oid>")
def OrderDetailsPage(oid):
  """This page shows the details of the order."""
  order = Order.query.get(oid)

  return render_template("customer/orderDetailsPage.html", order=order)


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
