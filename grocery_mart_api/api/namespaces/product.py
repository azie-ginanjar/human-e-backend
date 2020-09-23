from flask import request
from flask_restx import Namespace, Resource, fields

from grocery_mart_api.commons.decorators import admin_required
from grocery_mart_api.commons.schemas import ProductSchema
from grocery_mart_api.extensions import db
from grocery_mart_api.models import Product

api = Namespace('product', description='products related endpoint')

add_product_fields = api.model('AddProductFields', {
    'price': fields.Float(required=True, description='product price'),
    'merchant': fields.String(required=True, description='merchant'),
    'expiry': fields.Integer(required=True, description='product expiry in epoch'),
})

update_product_fields = api.model('UpdateProductFields', {
    'price': fields.Float(required=False, description='product price'),
    'merchant': fields.String(required=False, description='merchant'),
    'expiry': fields.Integer(required=False, description='product expiry in epoch'),
})

parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers')


@api.route('/')
class ProductResource(Resource):
    method_decorators = [admin_required]

    @api.expect(add_product_fields, validate=True)
    def post(self):
        """
        add new product
        """
        price = request.json.get('price')
        merchant = request.json.get('merchant')
        expiry = request.json.get('expiry')

        product = Product(
            price=float(price),
            merchant=merchant,
            expiry=expiry
        )

        db.session.add(product)

        try:
            db.session.commit()
            product_dump = ProductSchema().dump(product)

            return {
                'product': product_dump
            }
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400


@api.route('/<int:product_id>')
class ProductResource(Resource):
    method_decorators = [admin_required]

    @api.expect(update_product_fields, validate=True)
    def put(self, product_id):
        """
        add new product
        """
        product = Product.query.filter(
            Product.id == product_id
        ).first()

        req = request.json

        if 'price' in req:
            product.price = req['price']

        if 'merchant' in req:
            product.merchant = req['merchant']

        if 'expiry' in req:
            product.expiry = req['expiry']

        try:
            db.session.commit()
            product_dump = ProductSchema().dump(product)

            return {
                'product': product_dump
            }
        except Exception as e:
            db.session.rollback()
            return {
                       'error': str(e)
                   }, 400
