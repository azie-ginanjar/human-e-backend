import uuid

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields

from grocery_mart_api.commons.decorators import admin_required
from grocery_mart_api.commons.pagination import paginate
from grocery_mart_api.commons.schemas import ProductSchema, InventorySchema
from grocery_mart_api.extensions import db
from grocery_mart_api.models import Product, Inventory, StockIn

api = Namespace('product', description='products related endpoint')

add_product_fields = api.model('AddProductFields', {
    'price': fields.Float(required=True, description='product price'),
    'name': fields.String(required=True, description='product name'),
    'merchant': fields.String(required=True, description='merchant'),
    'expiry': fields.Integer(required=True, description='product expiry in epoch'),
})

add_stock_fields = api.model('AddStockFields', {
    'product_id': fields.String(required=True, description='product id'),
    'quantity': fields.Integer(required=True, description='quantity'),
})

update_product_fields = api.model('UpdateProductFields', {
    'id': fields.String(required=True, description='product id'),
    'price': fields.Float(required=False, description='product price'),
    'merchant': fields.String(required=False, description='merchant'),
    'name': fields.String(required=False, description='product name'),
    'expiry': fields.Integer(required=False, description='product expiry in epoch'),
})

parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers')


@api.route('/')
class ProductResource(Resource):

    @admin_required
    @api.expect(add_product_fields, validate=True)
    def post(self):
        """
        add new product
        """
        price = request.json.get('price')
        merchant = request.json.get('merchant')
        name = request.json.get('name')
        expiry = request.json.get('expiry')

        product_id = str(uuid.uuid4())
        product = Product(
            id=product_id,
            price=float(price),
            merchant=merchant,
            name=name,
            expiry=expiry
        )

        db.session.add(product)

        inventory_id = str(uuid.uuid4())
        inventory = Inventory(
            id=inventory_id,
            product_id=product_id,
            stock=0
        )

        db.session.add(inventory)

        try:
            db.session.commit()
            product_dump = ProductSchema().dump(product)

            return {
                'product': product_dump
            }
        except Exception as e:
            db.session.rollback()
            return {
                       'error': 'failed to saved to database'
                   }, 400

    @admin_required
    @api.expect(update_product_fields, validate=True)
    def put(self):
        """
        update specified product
        """
        req = request.json

        product = Product.query.filter(
            Product.id == req['id']
        ).first()

        if 'price' in req:
            product.price = req['price']

        if 'merchant' in req:
            product.merchant = req['merchant']

        if 'expiry' in req:
            product.expiry = req['expiry']

        if 'name' in req:
            product.name = req['name']

        try:
            db.session.commit()
            product_dump = ProductSchema().dump(product)

            return {
                'product': product_dump
            }
        except Exception as e:
            db.session.rollback()
            return {
                       'error': 'failed to updated to database'
                   }, 400

    query_parser = api.parser()
    query_parser.add_argument('keyword', required=False, location='args', type=str)
    query_parser.add_argument('page', required=False, type=int, help='by default equal to 1')
    query_parser.add_argument('page_size', required=False, type=int, help='by default equal to 10')

    @jwt_required
    @api.expect(query_parser, validate=True)
    def get(self):
        """
        search products
        """
        keyword = request.args.get('keyword')

        products = Product.query

        if keyword:
            products = products.filter(
                Product.name.contains(keyword)
            )

        schema = ProductSchema(many=True)
        products = paginate(products, schema)

        try:
            return {
                'products': products
            }
        except Exception as e:
            db.session.rollback()
            return {
                       'error': 'failed to updated to database'
                   }, 400


@api.route('/stockin')
class ProductResource(Resource):
    method_decorators = [admin_required]

    @api.expect(add_stock_fields, validate=True)
    def post(self):
        """
        add stock
        """
        quantity = request.json.get('quantity')
        product_id = request.json.get('product_id')

        stock_in_id = str(uuid.uuid4())
        stock_in = StockIn(
            id=stock_in_id,
            quantity=int(quantity),
            product_id=product_id
        )

        db.session.add(stock_in)

        # add quantity on inventory
        inventory = Inventory.query.filter(
            Inventory.product_id == product_id
        ).first()

        inventory.stock += quantity

        try:
            db.session.commit()
            inventory_dump = InventorySchema().dump(inventory)

            return {
                'inventory': inventory_dump
            }
        except Exception as e:
            db.session.rollback()
            return {
                       'error': 'failed to saved to database'
                   }, 400
