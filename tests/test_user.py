import json


def test_login(client, admin_access_token):
    # test generate reset token
    res = client.post("/auth/login", json={"username": "admin", "password": "admin"})
    assert res.status_code == 200


def test_login_not_case_insensitive(client, admin_access_token):
    # test generate reset token
    res = client.post("/auth/login", json={"username": "ADmIn", "password": "admin"})
    assert res.status_code == 200


def test_login_fails(client, admin_access_token):
    # test generate reset token
    res = client.post("/auth/login", json={"username": "admin", "password": "abcdef"})
    assert res.status_code == 200
    assert 'error' in str(res.data)


def test_registration(client, db):
    # test registration
    res = client.post("/auth/registration", json={
        "username": "test_user",
        "password": "abc1231"
    })

    res_json = json.loads(res.data)
    assert res.status_code == 200
    assert res_json['user']['username'] == 'test_user'


def test_duplicate_registration_fails(client, db):
    # test duplicate registration

    res = client.post("/auth/registration", json={
        "username": "jeffdh5",
        "password": "abc"
    })
    assert res.status_code == 200

    res = client.post("/auth/registration", json={
        "username": "jeffdh5",
        "password": "abc"
    })
    print(res.data)
    assert res.status_code == 400
    assert 'error' in str(res.data)


def test_duplicate_registration_fails_even_if_case_changes(client, db):
    # test generate reset token

    res = client.post("/auth/registration", json={
        "username": "JeFfDh5",
        "password": "abc"
    })
    assert res.status_code == 200

    res = client.post("/auth/registration", json={
        "username": "jeffdh5",
        "password": "abc"
    })
    assert res.status_code == 400
    assert 'error' in str(res.data)
