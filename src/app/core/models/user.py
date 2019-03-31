"""User module"""

import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
  """User class"""

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(60))
  user_type = db.Column(db.Integer)

  def __repr__(self):
    return f"User({self.id}, {self.email}, password, {self.user_type})"

  def GetUserID(self):
    """Return an integer which is the user's ID"""
    return self.id

  def GetEmail(self):
    """Return a string which is the user's email"""
    return self.email

  def GetType(self):
    """Return 1 or 2 such that 1 means the user is a normal user, 2
      means the user is a staff"""
    return self.user_type

  def SetPassword(self, password):
    """A hashed password with a randomly generated salt will be generated
    and save in self.password"""
    new_password = b"{0}".format(password)
    self.password = bcrypt.hashpw(new_password, bcrypt.gensalt())

  def VerifyPassword(self, password):
    """Verify the password by comparing the user input password and the hashed
    password, if the password is correct return True, else return False"""
    return bcrypt.checkpw(password, self.passward)
