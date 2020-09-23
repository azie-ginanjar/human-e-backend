from sqlalchemy import ForeignKey, UniqueConstraint

from grocery_mart_api.extensions import db


class OrderDetail(db.Model):
    id = db.Column(db.String(), primary_key=True)
    order_id = db.Column(db.String(), ForeignKey('order.id', ondelete='CASCADE'))
    product_id = db.Column(db.String(), ForeignKey('product.id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer())

    def __init__(self, **kwargs):
        super(OrderDetail, self).__init__(**kwargs)
