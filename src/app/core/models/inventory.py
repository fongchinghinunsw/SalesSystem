"""Inventory module"""

from functools import reduce
from . import db

item_ig = db.Table(
    'item_ig',
    db.Column(
        'item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
    db.Column(
        'ig_id',
        db.Integer,
        db.ForeignKey('ingredient_group.id'),
        primary_key=True))

ig_item = db.Table(
    'ig_item',
    db.Column(
        'item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
    db.Column(
        'ig_id',
        db.Integer,
        db.ForeignKey('ingredient_group.id'),
        primary_key=True))


class Item(db.Model):
  """Item class"""
  id = db.Column(db.Integer, primary_key=True)
  root = db.Column(db.Boolean)
  stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
  stock_unit = db.Column(db.Integer, default=1)
  max_item = db.Column(db.Integer)
  price = db.Column(db.Float, default=0)
  image = db.Column(db.Text)
  name = db.Column(db.Text)
  ingredientgroups = db.relationship('IngredientGroup', secondary=item_ig)

  def GetID(self):
    return self.id

  def IsRoot(self):
    return self.root

  def GetStockID(self):
    return self.stock_id

  def GetStockUnit(self):
    return self.stock_unit

  def GetPrice(self):
    return self.price

  def GetImage(self):
    return self.image

  def GetName(self):
    return self.name

  def ToOrderNode(self, number):
    """Convert Item to Node in order content tree"""
    if self.max_item is not None and number > self.max_item:
      raise ValueError(
          'Number of %s can\'t exceed %d' % (self.name, self.max_item))
    ret = {
        "type": "item",
        "id": self.id,
        "num": number,
        "name": self.name,
        "price": self.price * number,
        "igs": []
    }
    for ig in self.ingredientgroups:
      ret['igs'].append(ig.ToOrderNode())
    return ret

  def HasEnoughStock(self, number):
    return self.stock is None or self.stock.GetAmount(
    ) >= number * self.stock_unit


class IngredientGroup(db.Model):
  """IngredientGroup class"""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text)
  max_item = db.Column(db.Integer)
  min_item = db.Column(db.Integer)
  max_option = db.Column(db.Integer)
  min_option = db.Column(db.Integer)
  options = db.relationship('Item', secondary=ig_item)

  def GetID(self):
    return self.id

  def GetName(self):
    return self.name

  def GetMaxItem(self):
    return self.max_item

  def GetMinItem(self):
    return self.min_item

  def GetMaxOption(self):
    return self.max_option

  def GetMinOption(self):
    return self.min_option

  def ToOrderNode(self):
    """Convert IG to Node in order content tree"""
    return {
        "type": "ig",
        "id": self.id,
        "name": self.name,
        "fulfilled": False,
        "options": []
    }

  def CheckOrderNode(self, element):
    """Check whether an order node fulfills all requirements
    for this ingredient group"""
    options = len({x['id'] for x in element['options'] if x['num'] > 0})
    items = reduce((lambda x, y: x + y['num']), element['options'], 0)
    if self.min_option is not None and options < self.min_option:
      raise ValueError(
          "At least %d different offerings must be selected from %s" %
          (self.min_option, self.name))
    if self.max_option is not None and options > self.max_option:
      raise ValueError("At most %d different offerings can be selected from %s"
                       % (self.max_option, self.name))
    if self.min_item is not None and items < self.min_item:
      raise ValueError(
          "At least %d items must be chosen in %s" % (self.min_item, self.name))
    if self.max_item is not None and items > self.max_item:
      raise ValueError(
          "At most %d items can be chosen in %s" % (self.max_item, self.name))
    return True


class Stock(db.Model):
  """Stock class"""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text)
  amount = db.Column(db.Integer, default=0)
  items = db.relationship('Item', backref='stock')

  def GetID(self):
    return self.id

  def GetName(self):
    return self.name

  def GetAmount(self):
    return self.amount

  def AdjustAmount(self, amount):
    """adjust amount by a variance
    If amount is negative after applying the variance, set it to 0.
    """
    self.amount += amount
    if self.amount < 0:
      self.amount = 0
    return self.amount

  def IncreaseAmount(self, amount):
    if amount < 0:
      raise ValueError("Cannot increase by negative stock")
    self.amount += amount

  def DecreaseAmount(self, amount):
    if amount < 0:
      raise ValueError("Cannot decrease by negative stock")
    if self.amount - amount < 0:
      raise ValueError("Stock not enough")
    self.amount -= amount
