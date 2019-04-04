"""Admin blueprint views"""

from flask import render_template
from . import bp as app  # Note that app = blueprint, current_app = flask context
from app.core.models.order import Order
from flask import render_template


@app.route("/")
def home():
  return render_template('admin/landing.html')

@app.route("/order", methods = ['GET', 'POST'])
def order():
  Order.query.all()
  return render_template("admin/order.html", order=order)
