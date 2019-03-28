from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(60))
  user_type = db.Column(db.Integer)

  def __repr__(self):
    return f"User({self.id}, {self.email}, password, {self.user_type})"

  def getUserID():
    return self.id

  def getEmail():
    return self.email
   
  def getType():
    return self.user_type
  
  def setPassword(password):
    self.password = password
