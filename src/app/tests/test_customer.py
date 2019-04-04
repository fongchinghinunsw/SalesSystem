"""Module to test the customer blueprint"""

from app.core.models.inventory import Stock, Item, IngredientGroup
from app.core.models.order import Order
from app.core.models.user import User
from app.core.models import db


def test_index(client):
  """ Test customer index
  Arguments:
    client: flask client
  """
  response = client.get('/')
  assert b"Hello this is customer" in response.data


def test_order_details(client, app):
  """ Test correct order details on front end
  """
  with app.app_context():
    sburger = Stock(name="burger", amount=10)
    swrap = Stock(name="wrap", amount=10)
    db.session.add(sburger)
    db.session.add(swrap)
    imain = Item(name="main")
    iburger = Item(name="burger")
    iwrap = Item(name="wrap")
    gtype = IngredientGroup(
        name="type", min_item=1, max_item=1, min_option=1, max_option=1)
    db.session.add(imain)
    db.session.add(iburger)
    db.session.add(iwrap)
    db.session.add(gtype)
    sburger.items.append(iburger)
    swrap.items.append(iwrap)
    gtype.options.append(iburger)
    gtype.options.append(iwrap)
    imain.ingredientgroups.append(gtype)
    db.session.commit()

    user = User(email="dickon@gmail.com", user_type=1)

    order = Order(status=0, price=100)
    user.orders.append(order)
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])

    db.session.add(user)
    db.session.add(order)
    db.session.commit()

    response = client.get('/order/%d' % order.GetID())
    assert b"dickon@gmail.com" in response.data
    assert order.GetDetailsString().encode("utf-8") in response.data
