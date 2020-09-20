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
    marketplace_id = db.Column(db.String())
    customer_id = db.Column(db.String())
    has_active_subscription = db.Column(db.Boolean())
    is_trialing = db.Column(db.String())
    plan = db.Column(db.String())
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

    # def update_credentials(self, seller_id, access_token, marketplace_id, auth_profile):
    #     self.seller_id = seller_id
    #     self.access_token = access_token
    #     self.marketplace_id = marketplace_id
    #     self.auth_profile = auth_profile

    def cancel_membership(self):
        self.has_active_subscription = False
        self.is_trialing = False

    def restart_membership(self):
        self.has_active_subscription = True
        self.is_trialing = False

    def mark_as_completed_trial(self):
        self.has_active_subscription = True
        self.is_trialing = False

    def get_formatted_user_details(self):
        return {
            "username": self.username,
            "businessName": self.business_name,
            "marketplaceId": self.marketplace_id,
            "authProfile": self.auth_profile,
            "email": self.email,
            "plan": self.plan,
            "phone": self.phone,
            "active": self.has_active_subscription,
            "isTrialing": self.is_trialing,
        }

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
    def find_user_by_customer_id(customer_id):
        return User.query.filter_by(customer_id=customer_id).first()

    @staticmethod
    def find_user_by_phone(phone):
        return User.query.filter_by(phone=phone).first()

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
    def get_active_users():
        return User.query.filter_by(has_active_subscription=True)

