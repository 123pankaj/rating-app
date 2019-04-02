from datetime import datetime

from rating_app.extensions import db


class Order(db.Model):
    """Basic user model
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    product_id = db.Column(db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    ratings = db.Column(db.SmallInteger, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<Order %s>" % self.ratings
