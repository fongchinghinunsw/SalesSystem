from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  user_type = db.Column(db.Integer, nullable=False)
    
  def __repr__(self):
      return f"User('{self.id}', '{self.username}')"
