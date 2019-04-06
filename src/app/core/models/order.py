"""Order module"""

from datetime import datetime
import json
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

  def GetID(self):
    return self.id

  def GetUserID(self):
    return self.user_id

  def GetStatus(self):
    return self.status
    
  def GetStatusText(self, status):
    text = {0: "created", 1: "completed", 2: "paid"}
    return text[status]

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
      if "type" in element and element['type'] == 'ig':
        element = element['options']
      elif "type" in element and element['type'] == 'item':
        element = element['igs']
      element = element[int(fid)]
    if element['fulfilled']:
      raise ValueError('Cannot fulfill %s twice' % element['name'])
    ig = IngredientGroup.query.get(element['id'])
    if ig is None:
      raise ValueError('Cannot find IngredientGroup')
    for i, item_id in enumerate(items):
      if numbers[i] == 0:
        continue
      item = Item.query.get(item_id)
      if item is None:
        raise ValueError('Item doesn\'t exist!' % item_id)
      if not item.HasEnoughStock(numbers[i]):
        raise ValueError('We don\'t have enough stock for %s' % item.GetName())
      element['options'].append(item.ToOrderNode(numbers[i]))
    if not ig.CheckOrderNode(element):
      raise ValueError('Items do not fulfill requirements for %s' % ig.name)
    element['fulfilled'] = True
    self.content = json.dumps(content)

  def AddRootItem(self, item_id, num):
    """add a new root item to the order"""
    item = Item.query.get(item_id)
    if item is None:
      raise ValueError('Item doesn\'t exist!' % item_id)
    if not item.HasEnoughStock(num):
      raise ValueError('We don\'t have enough stock for %s' % item.GetName())
    node = item.ToOrderNode(num)
    if self.content is None:
      content = []
    else:
      content = json.loads(self.content)
    content.append(node)
    self.content = json.dumps(content)
