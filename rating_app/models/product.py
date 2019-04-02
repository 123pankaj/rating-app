from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from rating_app.extensions import db


class Product(db.Model):
    """Basic user model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    orders = relationship("Order", backref="product")

    @hybrid_property
    def avg_ratings(self):
        valid_orders = [order for order in self.orders if order.ratings is not None]
        if valid_orders:
            return sum(order.ratings for order in valid_orders) / len(valid_orders)
        else:
            return 0.0

    def __repr__(self):
        return "<Product %s>" % self.name
