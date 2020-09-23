from grocery_mart_api.extensions import ma, db
from grocery_mart_api.models import (
    User, Product
)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        sqla_session = db.session
