from sqlalchemy import ForeignKey, UniqueConstraint

from grocery_mart_api.extensions import db


class Inventory(db.Model):
    id = db.Column(db.String(), primary_key=True)
    product_id = db.Column(db.String(), ForeignKey('product.id', ondelete='CASCADE'))
    stock = db.Column(db.Integer())

    product = db.relationship(
        'Product',
        back_populates='inventory'
    )

    __table_args__ = (
        UniqueConstraint('product_id', name='unique_product_id'),
    )

    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)