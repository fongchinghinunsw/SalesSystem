"""Module to test the order model module"""
import pytest
from app.core.models.inventory import Stock, Item, IngredientGroup
from app.core.models.order import Order
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

    assert order.GetDetailsString(
    ) == """main ......$0.00\n  type:burger ......$5.00\nmain ......$0.00
  type:wrap ......$3.30\n"""
