"""Test ES3: As a staff member, I'd like to check and update inventory."""
import pytest
from app.core.models.inventory import Stock, Item
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


def test_stock_list(app, client):
  """test inventory list"""
  names = [
      "Muffin Bun", "Sesame Bun", "Standard Bun", "Wrap", "Chicken Patty",
      "Beef Patty", "Vegetarian Patty", "Tuna Patty", "Tomato", "Tomato Sauce",
      "BBQ Sauce", "Mint Sauce", "Chocolate Sauce", "Cheddar Cheese", "Nuggets",
      "Fries (g)", "Coke (ml)", "Sundaes (ml)"
  ]
  with app.app_context():
    user = User(
        name="Dickson", email="dickon@gmail.com", user_type=UserType.ADMIN)
    user.SetPassword("123456")
    db.session.add(user)
    db.session.commit()
    stock_amount = 100
    for name in names:
      db.session.add(Stock(name=name, amount=stock_amount))
      stock_amount += 1
    db.session.commit()

  response = client.get('/admin/inventory')
  assert response.status == '302 FOUND'

  login(client, "dickon@gmail.com", "123456")
  response = client.get('/admin/inventory')
  rsp = str(response.data)
  print(rsp)
  stock_amount = 100
  for name in names:
    assert name in rsp
    rsp = rsp[rsp.find(name) + 1:]
    assert str(stock_amount) in rsp
    rsp = rsp[rsp.find(str(stock_amount)) + 1:]
    stock_amount += 1


def test_update_stock():
  """ Test adjusting stock amount
  """
  stock = Stock(name="test", amount=0)
  stock.AdjustAmount(1000)
  assert stock.GetAmount() == 1000
  with pytest.raises(ValueError):
    stock.DecreaseAmount(-1)
  assert stock.GetAmount() == 1000
  with pytest.raises(ValueError):
    stock.IncreaseAmount(-1)
  assert stock.GetAmount() == 1000
  stock.AdjustAmount(-100)
  assert stock.GetAmount() == 900
  stock.IncreaseAmount(100)
  assert stock.GetAmount() == 1000
  stock.DecreaseAmount(200)
  assert stock.GetAmount() == 800
  stock.DecreaseAmount(800)
  assert stock.GetAmount() == 0
  with pytest.raises(RuntimeError):
    stock.DecreaseAmount(1)
  assert stock.GetAmount() == 0
  stock.AdjustAmount(-1)
  assert stock.GetAmount() == 0
  stock.IncreaseAmount(0)
  assert stock.GetAmount() == 0
  stock.DecreaseAmount(0)
  assert stock.GetAmount() == 0


def test_item_stock_check():
  """ Test item.HasEnoughStock
  """
  stock = Stock(name="burger", amount=5)
  item = Item(name="burger", stock_unit=10)
  stock.items.append(item)
  assert item.HasEnoughStock(0)
  assert not item.HasEnoughStock(1)
  stock.IncreaseAmount(8)
  assert item.HasEnoughStock(0)
  assert item.HasEnoughStock(1)
  assert not item.HasEnoughStock(2)
