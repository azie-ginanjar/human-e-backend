from sqlalchemy import ForeignKey

from grocery_mart_api.extensions import db


class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey('user_v2.id', ondelete='CASCADE'))
    status = db.Column(db.String())  # could be unpaid or paid
    delivery_date = db.Column(db.Integer())

    order_details = db.relationship(
        'OrderDetail',
        backref='order'
    )

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.status = 'unpaid'
