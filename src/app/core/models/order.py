"""Order module"""

from datetime import datetime
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
