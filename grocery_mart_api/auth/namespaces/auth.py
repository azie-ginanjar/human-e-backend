from flask import request, current_app
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
)
from flask_restx import Namespace, Resource, fields

from grocery_mart_api.commons.schemas import UserSchema
from grocery_mart_api.extensions import (
    db,
    pwd_context
)
from grocery_mart_api.models import User, ResetToken

api = Namespace('', description='Registration/Login/API Authorization related operations')

registration_resource_fields = api.model('UserRegistrationDetails', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

login_resource_fields = api.model('LoginDetails', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})

reset_password_resource_resource_fields = api.model('ResetPasswordFields', {
    'token_str': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
    'password_2': fields.String(required=True, description='Stripe Token')
})

parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers')


@api.route('/registration')
class RegistrationResource(Resource):
    method_decorators = []

    @api.expect(registration_resource_fields, validate=True)
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        user = User(
            username=username.lower(),
            password=password,
            role='user'
        )

        db.session.add(user)

        try:
            db.session.commit()
            user_dump = UserSchema().dump(user)
            print(user_dump)
            user_dump.pop("password", None)
            return {
                'user': user_dump
            }
        except Exception as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400


@api.route('/login')
class LoginResource(Resource):
    method_decorators = []

    @api.expect(login_resource_fields, validate=True)
    def post(self):
        """Authenticate user and return token"""
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        user = User.find_user_by_username(username)

        if user is None or not pwd_context.verify(password, user.password):
            return {'error': 'Bad credentials'}

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        ret = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return ret


@api.route('/refresh')
class RefreshTokenResource(Resource):
    method_decorators = [jwt_refresh_token_required]

    def post(self):
        """Refresh token for user to maintain user identity"""
        current_user = get_jwt_identity()
        ret = {
            'access_token': create_access_token(identity=current_user)
        }
        return ret
