from sqlalchemy import func, UniqueConstraint

from grocery_mart_api.extensions import db, pwd_context


class User(db.Model):
    __tablename__ = "user_v2"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String())
    created_at = db.Column(db.Integer())

    __table_args__ = (
        UniqueConstraint('username', name='unique_username'),
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = pwd_context.hash(kwargs.get('password'))

    def update_password(self, password):
        self.password = pwd_context.hash(password)

    @staticmethod
    def get(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def find_user_by_username(username):
        return User.query.filter(User.username == username).first()

