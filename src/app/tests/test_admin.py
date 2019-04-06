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


def test_order_list(client, app):
  """test order list page"""
  with app.app_context():
    order = Order(price=123, status=321)
    db.session.add(order)
    db.session.commit()
    timestamp = order.GetCreatedAt()

  response = client.get('/admin/orderlist')
  rsp = str(response.data)
  assert "ID" in rsp
  assert "User Name" in rsp
  assert "Price" in rsp
  assert "Created at" in rsp
  assert "Updated at" in rsp
  assert "Status" in rsp
  assert "123" in rsp
  assert "321" in rsp
  assert str(timestamp) in rsp

  with app.app_context():
    order1 = Order(price=231, status=222)
    db.session.add(order1)
    db.session.commit()

  response = client.get('/admin/orderlist')
  rsp = str(response.data)
  assert "231" in rsp
  position = rsp.find("123")
  position1 = rsp.find("231")
  assert position1 < position
