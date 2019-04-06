"""Module to test the admin blueprint"""

from app.core.models.order import Order
from app.core.models import db

def test_index(client):
  """ Test admin index
  Arguments:
    client: flask client
  """
  response = client.get('/admin/')
  assert b"Hello this is admin" in response.data

def test_order_list(client,app):
  response = client.get('/admin/orderlist/')
  rsp = str(response.data)
  assert "id" in rsp
  assert "user_name" in rsp
  assert "price" in rsp
  assert "created_at" in rsp
  assert "updated_at" in rsp
  assert "status" in rsp

  with app.app_context():
  order = Order()
  price = order.price(123)
  db.session.add(price)
  assert "123" in rsp
  status = order.status(321)
  db.session.add(status)
  assert "321" in rsp
  created_at = order.created_at(datetime(2019, 4, 5))
  db.session.add(created_at)
  assert "created_at.strftime("%x")" in rsp
  updated_at = order.updated_at(datetime(2019, 4, 6))
  db.session.add(updated_at)
  assert "updated_at.strftime("%x")" in rsp

>>>>>>> admin:tests of displaying order list
