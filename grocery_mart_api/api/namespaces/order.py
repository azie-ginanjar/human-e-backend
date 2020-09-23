import uuid

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from grocery_mart_api.commons.schemas import OrderSchema
from grocery_mart_api.extensions import db
from grocery_mart_api.models import Order, OrderDetail, Inventory

api = Namespace('order', description='order related endpoint')

add_to_cart_fields = api.model('AddToCartFields', {
    'product_id': fields.String(required=True, description='product id'),
    'quantity': fields.Integer(required=True, description='quantity')
})

parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers')


@api.route('/cart')
class ProductResource(Resource):
    method_decorators = [jwt_required]

    def get(self):
        """
        get active cart (unpaid order)
        """

        order = Order.query.filter(
            Order.user_id == get_jwt_identity(),
            Order.status == 'unpaid'
        ).first()

        try:
            order = OrderSchema().dump(order)

            return {
                'order': order
            }
        except Exception as e:
            db.session.rollback()
            return {
                       'error': 'failed to retrieved data from database'
                   }, 400

    @api.expect(add_to_cart_fields, validate=True)
    def post(self):
        """
        add to cart
        """
        product_id = request.json.get('product_id')
        quantity = request.json.get('quantity')

        user_id = get_jwt_identity()

        # create new order if no unpaid order otherwise update the unpaid one.
        unpaid_order = Order.query.filter(
            Order.user_id == user_id,
            Order.status == 'unpaid'
        ).first()

        if not unpaid_order:
            order = Order(
                id=str(uuid.uuid4()),
                user_id=user_id
            )

            db.session.add(order)
        else:
            order = unpaid_order

        inventory = Inventory.query.filter(
            Inventory.product_id == product_id
        ).first()

        if inventory.stock < quantity:
            return {
                'error': 'insufficient stocks.'
            }, 400

        order_detail = OrderDetail(
            id=str(uuid.uuid4()),
            order_id=order.id,
            product_id=product_id,
            quantity=quantity
        )

        db.session.add(order_detail)

        try:
            db.session.commit()
            order = OrderSchema().dump(order)

            return {
                'order': order
            }
        except Exception as e:
            db.session.rollback()
            return {
                       'error': 'failed to saved to database'
                   }, 400
