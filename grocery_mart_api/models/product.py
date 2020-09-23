from grocery_mart_api.extensions import db


class Product(db.Model):
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float(precision=2))
    merchant = db.Column(db.String(length=255))
    expiry = db.Column(db.Integer())

    inventory = db.relationship(
        'Inventory',
        uselist=False,
        back_populates='product'
    )

    order_details = db.relationship(
        'OrderDetail',
        backref='product'
    )

    stock_ins = db.relationship(
        'StockIn',
        backref='product'
    )

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)
