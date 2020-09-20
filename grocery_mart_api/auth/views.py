from flask import Blueprint
from flask_restx import Api

from grocery_mart_api.models import User
from grocery_mart_api.extensions import jwt
from grocery_mart_api.auth.namespaces.auth import api as auth_namespace

blueprint = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(blueprint)
api.add_namespace(auth_namespace)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.get(identity)
