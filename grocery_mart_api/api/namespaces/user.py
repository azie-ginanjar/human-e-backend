from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields

from grocery_mart_api.commons.schemas import UserSchema
from grocery_mart_api.extensions import db
from grocery_mart_api.models import User

api = Namespace('user', description='User related operations')

parser = api.parser()
parser.add_argument('Authorization', type=str, location='headers')


@api.route("/")
class UserResource(Resource):
    method_decorators = [jwt_required]

    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.get(current_user_id)
        schema = UserSchema(partial=True)
        user_dump = schema.dump(current_user).data
        user_dump.pop("password", None)
        return user_dump


@api.route("/password")
class UpdatePasswordResource(Resource):
    method_decorators = [jwt_required]

    @api.expect(api.model('PasswordPostFields', {
        'password': fields.String(required=True, description='New Password'),
        'password_2': fields.String(required=True, description='Confirmed New Password'),
    }))
    def post(self):
        reset_password_fields = request.json
        password = reset_password_fields.get('password')
        password_2 = reset_password_fields.get('password_2')
        if not password == password_2:
            return {'error': 'Passwords do not match.'}, 400

        user = User.get(get_jwt_identity())
        user.update_password(password_2)
        try:
            db.session.commit()
            return {'error': None, 'msg': 'Password successfully updated.'}
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to save password in database update'}, 400
