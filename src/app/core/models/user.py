"""User module"""
import bcrypt
from . import db


class User(db.Model):
  """User class"""

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(60))
  user_type = db.Column(db.Integer)
  orders = db.relationship('Order', backref='user')

  def GetID(self):
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
    if 4 <= len(password) <= 20:
      new_password = password.encode('utf-8')
      self.password = bcrypt.hashpw(new_password,
                                    bcrypt.gensalt()).decode('utf-8')
    else:
      raise ValueError("Length should be between 4 and 20 inclusively")

  def VerifyPassword(self, password):
    """Verify the password by comparing the user input password and the hashed
    password, if the password is correct return True, else return False"""
    try:
      check_password = password.encode('utf-8')
      return bcrypt.checkpw(check_password, self.password.encode('utf-8'))
    except AttributeError:
      return False
    except TypeError:
      return False
    except ValueError:
      return False
