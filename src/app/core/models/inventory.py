"""Inventory module"""

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
  stock_unit = db.Column(db.Integer)
  max_item = db.Column(db.Integer)
  price = db.Column(db.Float)
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


class Stock(db.Model):
  """Stock class"""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text)
  amount = db.Column(db.Integer)
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
