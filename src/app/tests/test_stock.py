"""Module to test the user model class"""
import pytest
from app.core.models.inventory import Stock


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
  with pytest.raises(ValueError):
    stock.DecreaseAmount(1)
  assert stock.GetAmount() == 0
  stock.AdjustAmount(-1)
  assert stock.GetAmount() == 0
  stock.IncreaseAmount(0)
  assert stock.GetAmount() == 0
  stock.DecreaseAmount(0)
  assert stock.GetAmount() == 0
