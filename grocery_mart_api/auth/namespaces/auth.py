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
            business_name=None,
            marketplace_id=None,
            auth_profile="lazada_test",
            customer_id=None,
            plan=None,
            has_active_subscription=True,
            is_trialing=True,
            phone=None
        )

        db.session.add(user)

        try:
            db.session.commit()
            user_dump = UserSchema().dump(user).data
            user_dump.pop("password", None)
            ret = {
                'error': None,
                'username': user.username, # @TODO: Double check if this is actually being used. May be deprecated.
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


@api.route('/generate_reset_token')
class ResetTokenResource(Resource):
    method_decorators = []

    @api.expect(api.model('GenerateResetTokenPostResourceFields', {
        'email': fields.String(required=True, description='Required if method is email')
    }))
    def post(self):
        """
        Start of password recovery.
        System generates reset password token and sends it to the email user specified.
        """


        email = request.json.get('email')
        if not email:
            return {'error': 'No email in request.'}

        user = User.find_user_by_email(email)
        if not user:
            return {'error': 'No user found for this email.'}

        ResetToken.query.filter_by(user_id=user.id).delete()
        reset_token = ResetToken(user_id=user.id, token_str=str(uuid.uuid4()))
        db.session.add(reset_token)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            return {'error': None, 'msg': 'Failed to save reset token to database.'}


        if not current_app.testing:
            # @TODO actually send the email using SendGrid
            return {'error': None, 'msg': 'Successfully sent email.'}


@api.route('/reset_password')
class ResetPasswordResource(Resource):
    method_decorators = []

    @api.expect(reset_password_resource_resource_fields)
    def post(self):
        """
        Second and final step for resetting password. Grabs the token correct token,
        and finds the corresponding user and updates the password.
        """
        reset_password_fields = request.json
        token_str = reset_password_fields['token_str']
        password = reset_password_fields['password']
        password_2 = reset_password_fields['password_2']
        reset_token = ResetToken.query.filter_by(token_str=token_str).first()
        if not password == password_2:
            return {'error': 'Passwords do not match.'}

        if not reset_token:
            return {'error': 'Reset token not found.'}

        if reset_token.expiration_date < datetime.datetime.utcnow().isoformat():
            return {'error': 'Reset token has already expired.'}

        user = User.query.filter_by(id=reset_token.user_id).first()
        user.update_password(password_2)
        try:
            db.session.commit()
            return {'error': None, 'msg': 'Password successfully updated.'}
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to save password in database update'}
