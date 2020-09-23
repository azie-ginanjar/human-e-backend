import io
import json
import time
import uuid

import pytest

from grocery_mart_api.models import User, Product
from grocery_mart_api.app import create_app
from grocery_mart_api.extensions import db as _db


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def client(app):
    flask_app = app
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture
def admin_user(db):
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        username='admin',
        password='admin',
        role='admin'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_access_token(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    res = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    json_data = json.loads(res.data)
    return json_data['access_token']


@pytest.fixture
def test_user(db):
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        username='test',
        password='test',
        role='user',
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def access_token(client, test_user):
    res = client.post("/auth/login", json={
        "username": test_user.username,
        "password": "test"
    })
    json_data = json.loads(res.data)
    return json_data['access_token']


@pytest.fixture
def product(db):
    product = Product(
        id=str(uuid.uuid4()),
        merchant='admin',
        price=10.9,
        expiry=int(time.time())
    )

    db.session.add(product)
    db.session.commit()

    return product
