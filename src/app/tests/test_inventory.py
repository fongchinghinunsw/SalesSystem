"""Module to test the inventory module"""
import pytest
from app.core.models.inventory import Stock, Item


def test_stock_amount():
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
