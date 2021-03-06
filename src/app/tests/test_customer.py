"""Module to test the customer blueprint"""

from app.core.models.inventory import Stock, Item, IngredientGroup
from app.core.models.order import Order, OrderStatus
from app.core.models.user import User, UserType
from app.core.models import db


def login(client, email, password):
  return client.post(
      '/accounts/signin',
      data={
          "email": email,
          "password": password
      },
      follow_redirects=True)


def test_index(client, app):
  """ Test customer index
  """
  with app.app_context():
    response = client.get('/')
    assert b"Welcome!" in response.data
    user = User(
        name="Jeff", email="jeff@google.com", user_type=UserType.CUSTOMER)
    user.SetPassword("123456")
    db.session.add(user)
    db.session.commit()
    login(client, "jeff@google.com", "123456")
    response = client.get('/')
    assert b"Welcome, Jeff" in response.data


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

    user = User(
        name="Dickson", email="dickon@gmail.com", user_type=UserType.ADMIN)
    user.SetPassword("123456")
    user1 = User(name="123", email="123@gmail.com", user_type=UserType.CUSTOMER)
    user1.SetPassword("123456")
    user2 = User(
        name="Superman",
        email="Superman@gmail.com",
        user_type=UserType.CUSTOMER)
    user2.SetPassword("123456")

    order = Order(status=OrderStatus.PAID, price=100)
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
    assert response.status == '302 FOUND'

    login(client, "dickon@gmail.com", "123456")
    response = client.get('/order/%d' % order.GetID())
    assert b"Superman" in response.data
    assert order.GetDetailsString().encode("utf-8") in response.data
    if order.GetStatusText() != "ready":
      assert b"Mark as done" in response.data

    login(client, "123@gmail.com", "123456")
    response = client.get('/order/%d' % order.GetID())
    assert response.status == '302 FOUND'

    login(client, "Superman@gmail.com", "123456")
    response = client.get('/order/%d' % order.GetID())
    assert b"Superman" in response.data

    # Check if the user can see his unique order ID in the details page.
    assert "ORDER {0}".format(order.GetID()).encode("utf-8") in response.data

    # Customer shouldn't have access to details page of unpaid orders
    order.SetStatus(OrderStatus.CREATED)
    db.session.commit()
    response = client.get('/order/%d' % order.GetID())
    assert response.status == '302 FOUND'


def test_checkout_page(client, app):
  """ Test checkout page
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
    user = User(
        name="Dickson", email="dickon@gmail.com", user_type=UserType.ADMIN)
    user.SetPassword("123456")
    user2 = User(
        name="Superman",
        email="Superman@gmail.com",
        user_type=UserType.CUSTOMER)
    user2.SetPassword("123456")
    order = Order(status=OrderStatus.PAID, price=100)
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
