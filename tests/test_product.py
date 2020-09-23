import json
import time


def test_add_product_by_admin(client, admin_access_token):
    # test registration
    res = client.post(
        "/api/v1/product/",
        json={
            "merchant": "merchant1",
            "expiry": int(time.time()),
            "price": 200.01
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + admin_access_token
        },
    )

    res_json = json.loads(res.data)
    assert res.status_code == 200
    assert res_json['product']['price'] == 200.01


def test_add_product_by_user(client, access_token):
    # test registration
    res = client.post(
        "/api/v1/product/",
        json={
            "merchant": "merchant1",
            "expiry": int(time.time()),
            "price": 200.01
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
    )

    assert res.status_code == 403


def test_update_product_by_admin(client, admin_access_token, product):
    # test registration
    res = client.put(
        "/api/v1/product/{}".format(product.id),
        json={
            "price": 200.01
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + admin_access_token
        },
    )

    res_json = json.loads(res.data)
    assert res.status_code == 200
    assert res_json['product']['price'] == 200.01


def test_update_product_by_user(client, access_token, product):
    # test registration
    res = client.put(
        "/api/v1/product/{}".format(product.id),
        json={
            "price": 200.01
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
    )

    assert res.status_code == 403
