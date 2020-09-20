import datetime
import time

from sqlalchemy import func

from grocery_mart_api.extensions import db, pwd_context


class User(db.Model):
    __tablename__ = "user_v2"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    business_name = db.Column(db.String(), nullable=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String())
    phone = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.String())
    epoch_created_at = db.Column(db.Integer())

    # I made user_id and created_at could be set when instantiate user for unit test purpose

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = pwd_context.hash(kwargs.get('password'))
        self.created_at = datetime.datetime.utcnow().isoformat()
        self.epoch_created_at = int(time.time())

    def update_password(self, password):
        self.password = pwd_context.hash(password)

    @staticmethod
    def get(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def find_user_by_username(username):
        return User.query.filter(func.lower(User.username) == func.lower(username)).first()

    @staticmethod
    def find_user_by_email(email):
        return User.query.filter(func.lower(User.email) == func.lower(email)).first()

    @staticmethod
    def get_users():
        return User.query.all()

