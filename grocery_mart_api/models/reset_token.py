from grocery_mart_api.extensions import db
import datetime
from sqlalchemy import ForeignKey

EXPIRATION_MINUTES = 15


class ResetToken(db.Model):
    user_id = db.Column(db.String(), ForeignKey('user_v2.id'), primary_key=True)
    token_str = db.Column(db.String())
    expiration_date = db.Column(db.String())

    def __init__(self, user_id, token_str):
        self.user_id = user_id
        self.token_str = token_str
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=EXPIRATION_MINUTES)
        self.expiration_date = expiration_date.isoformat()
