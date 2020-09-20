from grocery_mart_api.extensions import ma, db
from grocery_mart_api.models import (
    User
)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
