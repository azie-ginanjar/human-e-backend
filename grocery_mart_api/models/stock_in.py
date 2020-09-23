import time

from sqlalchemy import ForeignKey, UniqueConstraint

from grocery_mart_api.extensions import db


class StockIn(db.Model):
    id = db.Column(db.String(), primary_key=True)
    product_id = db.Column(db.String(), ForeignKey('product.id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer())
    created_at = db.Column(db.Integer())

    def __init__(self, **kwargs):
        super(StockIn, self).__init__(**kwargs)
        self.created_at = int(time.time())
