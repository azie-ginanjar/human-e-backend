from grocery_mart_api.extensions import ma, db
from grocery_mart_api.models import (
    User, Product, Inventory, StockIn
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
