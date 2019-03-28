from flask.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    price = db.Column(db.Float)
    create_at = db.Column(db.Datetime)
    update_at = db.Column(db.Datetime)
    content = db.Column(db.Text)

    def __repr__(self):
        return f"Offer('{self.id}', '{self.user_id}', '{self.price}', '{create_at}', '{updare_at}', '{content}')"

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
	
