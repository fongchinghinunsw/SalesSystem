from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class order(db.Model):
    self.id = db.Column(db.Integer, primary_key=True)
    self.user_id = db.Column(db.Integer)
    self.status = db.Column(db.Integer)
    self.price = db.Column(db.Float)
    self.create_at = db.Column(db.Datetime)
    self.update_at = db.Column(db.Datetime)
    self.content = db.Column(db.Text)

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}', '{self.price}', '{create_at}', '{update_at}', '{content}')"

    def getID():
	return self.id

    def getUserID():
	return self.user_id

    def getStatus():
	return self.status

    def getPrice():
	return self.price

    def getCreateAt():
	return self.create_at

    def getUpdateAt():
	return self.update_at

    def getContent():
	return self.content

    def setID(id):
	self.id = id

    def setStatus(status):
	self.status = status
