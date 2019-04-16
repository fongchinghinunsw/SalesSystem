"""Module to test the order model module"""
import pytest
from app.core.models.inventory import Stock, Item, IngredientGroup
from app.core.models.order import Order, OrderStatus
from app.core.models import db


def test_create_order(app):
  """Test creating order and adding items to it"""
  with app.app_context():
    sburger = Stock(name="burger", amount=3)
    swrap = Stock(name="wrap", amount=0)
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

    order = Order()
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])
    order.AddRootItem(imain.GetID(), 1)
    with pytest.raises(RuntimeError):
      order.AddIG("0.0", [iburger.GetID()], [1])
    with pytest.raises(ValueError):
      order.AddIG("1.0", [iburger.GetID()], [2])
    with pytest.raises(ValueError):
      order.AddIG("1.0", [], [])
    with pytest.raises(RuntimeError):
      order.AddIG("1.0", [iwrap.GetID()], [1])
    swrap.IncreaseAmount(1)
    order.AddIG("1.0", [iwrap.GetID()], [1])


def test_order_details_string(app):
  """ Test GetDetailsString in Order class
  """
  with app.app_context():
    sburger = Stock(name="burger", amount=1)
    swrap = Stock(name="wrap", amount=1)
    db.session.add(sburger)
    db.session.add(swrap)
    imain = Item(name="main", price=0)
    iburger = Item(name="burger", price=5)
    iwrap = Item(name="wrap", price=3.3)
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

    order = Order()
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("1.0", [iwrap.GetID()], [1])

    assert order.GetDetailsString() == """main\n  type:burger ......$5.00\nmain
  type:wrap ......$3.30\n\n\nTotal price: $8.30"""


def test_pay_order_1(app):
  """ Test pay for order
  """
  with app.app_context():
    sburger = Stock(name="burger", amount=3)
    swrap = Stock(name="wrap", amount=3)
    db.session.add(sburger)
    db.session.add(swrap)
    imain = Item(name="main", price=0)
    iburger = Item(name="burger", price=5)
    iwrap = Item(name="wrap", price=3.3, stock_unit=2)
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

    order = Order()
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])
    assert order.GetPrice() == 5
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("1.0", [iwrap.GetID()], [1])
    assert order.GetPrice() == 8.3
    db.session.add(order)
    db.session.commit()

    assert order.GetStatus() == OrderStatus.CREATED

    order.Pay()
    db.session.commit()

    assert order.GetStatus() == OrderStatus.PAID
    assert order.GetPrice() == 8.3
    assert sburger.GetAmount() == 2
    assert swrap.GetAmount() == 1


def test_pay_order_2(app):
  """ Test pay order with complicated types of food
  """
  with app.app_context():
    sburger = Stock(name="burger", amount=3)
    swrap = Stock(name="wrap", amount=3)
    ssesamebun = Stock(name="sesamebun", amount=2)
    snormalbun = Stock(name="normalbun", amount=6)

    db.session.add(sburger)
    db.session.add(swrap)
    db.session.add(ssesamebun)
    db.session.add(snormalbun)

    imain = Item(name="main", price=0)
    iburger = Item(name="burger", price=5)
    iwrap = Item(name="wrap", price=3.3, stock_unit=2)
    isesamebun = Item(name="sesamebun", price=2)
    inormalbun = Item(name="normalbun", price=2)

    gtype = IngredientGroup(
        name="type", min_item=1, max_item=1, min_option=1, max_option=1)
    gbun = IngredientGroup(
        name="bun", min_item=2, max_item=3, min_option=1, max_option=3)
    db.session.add(imain)
    db.session.add(iburger)
    db.session.add(iwrap)

    db.session.add(isesamebun)
    db.session.add(inormalbun)

    db.session.add(gtype)
    db.session.add(gbun)

    sburger.items.append(iburger)
    swrap.items.append(iwrap)

    ssesamebun.items.append(isesamebun)
    snormalbun.items.append(inormalbun)

    gtype.options.append(iburger)
    gtype.options.append(iwrap)

    gbun.options.append(isesamebun)
    gbun.options.append(inormalbun)

    imain.ingredientgroups.append(gtype)
    iburger.ingredientgroups.append(gbun)
    db.session.commit()

    order = Order()
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("0.0", [iburger.GetID()], [1])
    assert order.GetPrice() == 5
    order.AddRootItem(imain.GetID(), 1)
    order.AddIG("1.0", [iwrap.GetID()], [1])
    assert order.GetPrice() == 8.3

    order.AddIG("0.0.0.0", [isesamebun.GetID()], [2])

    db.session.add(order)
    db.session.commit()

    assert order.GetStatus() == OrderStatus.CREATED

    order.Pay()
    db.session.commit()

    assert order.GetStatus() == OrderStatus.PAID
    assert order.GetPrice() == 12.3
    assert sburger.GetAmount() == 2
    assert swrap.GetAmount() == 1
    assert ssesamebun.GetAmount() == 0
    assert snormalbun.GetAmount() == 6
