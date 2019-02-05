from datetime import datetime

from .app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.name


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    products = db.relationship('Product', backref='orders', lazy=False)
    completed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return self.created
