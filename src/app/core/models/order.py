"""Order module"""

from datetime import datetime
import json
import uuid
from app.core.models.inventory import Item, IngredientGroup
from . import db


class Order(db.Model):
  """Order class"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  status = db.Column(db.Integer)
  price = db.Column(db.Float)
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(
      db.DateTime, default=datetime.now, onupdate=datetime.now)
  content = db.Column(db.Text)

  def __repr__(self):
    return f"Order('{self.id}', '{self.user_id}', '{self.price}'," \
      f"'{self.created_at}', '{self.updated_at}', '{self.content}')"

  def GetID(self):
    return self.id

  def GetUserID(self):
    return self.user_id

  def GetStatus(self):
    return self.status

  def GetPrice(self):
    return self.price

  def GetCreatedAt(self):
    return self.created_at

  def GetUpdatedAt(self):
    return self.updated_at

  def GetContent(self):
    return self.content

  def SetID(self, oid):
    self.id = oid

  def SetStatus(self, status):
    self.status = status

  def AddIG(self, path, items, numbers):
    """fulfill an ingredient group of an existing item in the order"""
    content = json.loads(self.content)
    fids = path.split('.')
    element = content
    for fid in fids:
      element = element[fid]
    ig = IngredientGroup.query.filter_by(id=element['id']).first()
    if ig is None:
      raise ValueError('Cannot find IngredientGroup')
    for i, item_id in enumerate(items):
      if numbers[i] == 0:
        continue
      item = Item.query.filter_by(id=item_id).first()
      if item is None:
        raise ValueError('Item doesn\'t exist!' % item_id)
      if not item.HasEnoughStock(numbers[i]):
        raise ValueError('We don\'t have enough stock for %s' % item.GetName())
      element[item_id] = item.ToOrderElement(numbers[i])
    if not ig.CheckOrderElement(element):
      raise ValueError('Items do not fulfill requirements for %s' % ig.name)
    element['fulfilled'] = True
    self.content = json.dumps(content)

  def AddRootItem(self, item_id):
    """add a new root item to the order"""
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
      raise ValueError('Item doesn\'t exist!' % item_id)
    if not item.HasEnoughStock(1):
      raise ValueError('We don\'t have enough stock for %s' % item.GetName())
    element = item.ToOrderElement(1)
    eid = str(uuid.uuid4())
    if self.content is None:
      content = {}
    else:
      content = json.loads(self.content)
    content[eid] = element
    self.content = json.dumps(content)
    return eid
