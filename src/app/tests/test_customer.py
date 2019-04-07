"""Module to test the customer blueprint"""

from app.core.models.inventory import Stock, Item, IngredientGroup
from app.core.models.order import Order
from app.core.models.user import User
from app.core.models import db


def login(client, email, password):
  return client.post(
      '/accounts/signin',
      data={
          "email": email,
          "password": password
      },
      follow_redirects=True)


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

    user = User(name="Dickson", email="dickon@gmail.com", user_type=1)
    user.SetPassword("123456")
    user1 = User(name="123", email="123@gmail.com", user_type=0)
    user1.SetPassword("123456")
    user2 = User(name="Superman", email="Superman@gmail.com", user_type=0)
    user2.SetPassword("123456")

    order = Order(status=0, price=100)
    user2.orders.append(order)
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])

    db.session.add(user)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(order)
    db.session.commit()

    login(client, "Superman@gmail.com", "654321")
    response = client.get('/order/%d' % order.GetID())
    assert b"redirected automatically to target URL" in response.data

    login(client, "dickon@gmail.com", "123456")

    response = client.get('/order/%d' % order.GetID())
    assert b"Superman" in response.data
    assert order.GetDetailsString().encode("utf-8") in response.data
    assert b"Mark as done" in response.data

    login(client, "123@gmail.com", "123456")
    response = client.get('/order/%d' % order.GetID())
    assert b"Access Denied!" in response.data

    login(client, "Superman@gmail.com", "123456")
    response = client.get('/order/%d' % order.GetID())
    assert b"Superman" in response.data

    # Check if the user can see his unique order ID in the details page.
    assert "ORDER {0}".format(order.GetID()).encode("utf-8") in response.data


def test_checkout_page(client, app):
  """ Test GetDetailsString in Order class
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
    user = User(name="Dickson", email="dickon@gmail.com", user_type=1)
    user.SetPassword("123456")
    user2 = User(name="Superman", email="Superman@gmail.com", user_type=0)
    user2.SetPassword("123456")
    order = Order(status=1, price=100)
    user2.orders.append(order)
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])
    db.session.add(user)
    db.session.add(user2)
    db.session.add(order)
    db.session.commit()
    login(client, "dickon@gmail.com", "123456")
    order = Order.query.get(order.GetID())
    response = client.get('/order/%d' % order.GetID())
    # Check if the customer can see the unique ID for the order.
    assert str(order.GetID()).encode("utf-8") in response.data
    client.get('/admin/order/%d/done' % order.GetID())
    # Check if the customer can see the details of his order.
    assert order.GetDetailsString().encode("utf-8") in response.data
