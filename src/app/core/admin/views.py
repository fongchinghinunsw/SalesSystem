"""Admin blueprint views"""

from flask import render_template
from app.core.models.order import Order
from . import bp as app  # Note that app = blueprint, current_app = flask context


@app.route("/")
def home():
  return render_template('admin/landing.html')


@app.route("/orderlist", methods=['GET'])
def order():
  orders = Order.query.order_by(Order.updated_at.desc()).all()
  return render_template("admin/order.html", orders=orders)
