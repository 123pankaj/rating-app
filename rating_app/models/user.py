from datetime import datetime

from sqlalchemy.orm import relationship

from rating_app.extensions import db


class User(db.Model):
    """Basic user model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    orders = relationship("Order", backref="user")

    def __repr__(self):
        return "<User %s>" % self.username
