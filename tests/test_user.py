import json

import factory
from pytest_factoryboy import register

from grocery_mart_api.constants import DefaultUserSetting, EmailTypes
from grocery_mart_api.models import User, ResetToken


@register
class UserFactory(factory.Factory):
    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@mail.com' % n)
    password = "mypwd"
    role = "user"

    class Meta:
        model = User


def test_login_with_email(client, db, admin_headers):
    # test generate reset token
    res = client.post("/auth/login", json={"username_or_email": "admin@admin.com", "password": "admin"})
    assert res.status_code == 200


def test_login_with_username(client, db, admin_headers):
    # test generate reset token
    res = client.post("/auth/login", json={"username_or_email": "admin", "password": "admin"})
    assert res.status_code == 200


def test_login_is_case_insensitive(client, db, admin_headers):
    # test generate reset token
    res = client.post("/auth/login", json={"username_or_email": "ADmIn", "password": "admin"})
    assert res.status_code == 200


def test_login_fails(client, db, admin_headers):
    # test generate reset token
    res = client.post("/auth/login", json={"username_or_email": "admin@admin.com", "password": "abcdef"})
    assert res.status_code == 200
    assert 'error' in str(res.data)


def test_registration(client, db):
    # test registration
    res = client.post("/auth/registration", json={
        "username": "test_user",  # use plan_id to make each username unique
        "email": "test_user@gmail.com",
        "password": "abc1231"
    })

    res_json = json.loads(res.data)
    print(res_json)
    assert res.status_code == 200
    assert res_json['username'] == 'test_user'


def test_duplicate_registration_fails(client, db, admin_headers):
    # test generate reset token

    res = client.post("/auth/registration", json={
        "username": "jeffdh5",
        "email": "jeffdh5r@gmail.com",
        "password": "abc",
        "registrationPlanId": "standard",
        "stripeToken": "faketoken"
    })
    assert res.status_code == 200

    res = client.post("/auth/registration", json={
        "username": "jeffdh5",
        "email": "jeffdh5r@gmail.com",
        "password": "abc",
        "registrationPlanId": "standard",
        "stripeToken": "faketoken"
    })
    assert res.status_code == 400
    assert 'error' in str(res.data)


def test_duplicate_registration_fails_even_if_case_changes(client, db, admin_headers):
    # test generate reset token

    res = client.post("/auth/registration", json={
        "username": "JeFfDh5",
        "email": "jeffdh5r@gmail.com",
        "password": "abc",
        "registrationPlanId": "standard",
        "stripeToken": "faketoken"
    })
    assert res.status_code == 200

    res = client.post("/auth/registration", json={
        "username": "jeffdh5",
        "email": "jeffdh5r@gmail.com",
        "password": "abc",
        "registrationPlanId": "standard",
        "stripeToken": "faketoken"
    })
    assert res.status_code == 400
    assert 'error' in str(res.data)
