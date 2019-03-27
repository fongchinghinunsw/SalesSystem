"""Order module"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
  """Order class"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
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
