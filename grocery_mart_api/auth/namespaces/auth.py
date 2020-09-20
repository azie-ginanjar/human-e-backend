import datetime
import traceback
import uuid

from flask import request, current_app
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
)
from flask_restx import Namespace, Resource, fields

from grocery_mart_api.commons.decorators import admin_required
from grocery_mart_api.commons.schemas import UserSchema
from grocery_mart_api.extensions import (
    db,
    pwd_context
)
from grocery_mart_api.libraries.auth_lib.auth_utils import validate_user_registration_payload
from grocery_mart_api.models import User, ResetToken

api = Namespace('', description='Registration/Login/API Authorization related operations')

registration_resource_fields = api.model('UserRegistrationDetails', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
})

login_resource_fields = api.model('LoginDetails', {
    'username_or_email': fields.String(required=True),
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
        request_data = request.json

        registration_data = validate_user_registration_payload(request_data)
        is_payload_valid = registration_data['is_valid']

        if not is_payload_valid:
            return {
                'error': registration_data['message']
            }, 400

        username = registration_data['username']
        password = registration_data['password']
        email = registration_data['email']

        user = User(
            username=username.lower(),
            email=email.lower(),
            password=password,
            role='user',
            phone=None
        )

        db.session.add(user)

        try:
            db.session.commit()
            user_dump = UserSchema().dump(user)
            print(user_dump)
            user_dump.pop("password", None)
            ret = {
                'error': None,
                'username': user.username,
                'user': user_dump
            }
        except Exception as e:
            db.session.rollback()
            ret = {
                'error': str(e)
            }

        return ret


@api.route('/login')
class LoginResource(Resource):
    method_decorators = []

    @api.expect(login_resource_fields, validate=True)
    def post(self):
        """Authenticate user and return token"""
        if not request.is_json:
            return {'error': 'Missing JSON in request'}

        username_or_email = request.json.get('username_or_email', None)
        password = request.json.get('password', None)
        if not username_or_email or not password:
            return {'error': 'Missing username or password'}

        user = User.find_user_by_username(username_or_email.lower())
        if user is None:
            user = User.find_user_by_email(username_or_email.lower())

        if user is None or not pwd_context.verify(password, user.password):
            return {'error': 'Bad credentials'}

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        ret = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return ret


@api.route('/admin_login')
@api.doc(parser=parser)
class AdminLoginResource(Resource):
    method_decorators = [admin_required]

    @api.expect(api.model('AdminLoginDetails', {
        'username': fields.String(required=True),
    }),validate=True)
    def post(self):

        """Authenticate user and return token"""
        if not request.is_json:
            return {'error': 'Missing JSON in request'}

        username = request.json.get('username', None)
        if not username:
            return {'error': 'Missing username'}

        user = User.find_user_by_username(username.lower())
        if user is None:
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
