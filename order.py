from flaskext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    price = db.Column(db.Float)
    create_at = db.Column(db.Datetime)
    update_at = db.Column(db.Datetime)
    content = db.Column(db.String(200))

    def __repr__(self):
        return f"Offer('{self.id}', '{self.user_id}', '{self.price}', '{create_at}', '{updare_at}', '{content}')"
