from bcrypt import hashpw, gensalt, checkpw
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(60))
  hashed_pwd = db.Column(db.String(60))
  user_type = db.Column(db.Integer)

  def __repr__(self):
    return f"User({self.id}, {self.email}, password, {self.user_type})"

  def getUserID():
    """Return an integer which is the user's ID"""
    return self.id

  def getEmail():
    """Return a string which is the user's email"""
    return self.email

  def getType():
    """Return 1 or 2 such that 1 means the user is a normal user, 2 
      means the user is a staff"""
    return self.user_type

  def setPassword(password):
    """Set a new password for the user, a hashed password with a randomly-
      generated salt will then be generated and save as self.hashed_pwd"""
    self.password = b"{0}".format(password)
    self.hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt())

  def verifyPassword(password):
    """Verify the password by comparing the user input password and the hashed
      password, if the password is correct return True, else return False"""
    if bcrypt.checkpw(password, self.hashed_pwd):
        return True
    else:
        return False
