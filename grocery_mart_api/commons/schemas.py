from grocery_mart_api.extensions import ma, db
from grocery_mart_api.models import (
    User, Product, Inventory, StockIn, OrderDetail, Order
)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        sqla_session = db.session


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        sqla_session = db.session


class StockInSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StockIn
        sqla_session = db.session


class OrderDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderDetail
        sqla_session = db.session


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        sqla_session = db.session

    order_details = ma.Nested(OrderDetailSchema, many=True)
