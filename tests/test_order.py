import json
import time

from grocery_mart_api.models import Inventory


def setup_initial_coondition(client, admin_access_token):
    # create new product
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

    product_id = res_json['product']['id']
    # add stock
    res = client.post(
        "/api/v1/product/stockin",
        json={
            "product_id": product_id,
            "quantity": 10
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + admin_access_token
        },
    )

    return product_id


def test_add_to_cart(client, access_token, admin_access_token):
    product_id = setup_initial_coondition(client, admin_access_token)

    res = client.post(
        "/api/v1/order/cart",
        json={
            "product_id": product_id,
            "quantity": 5
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
    )
    res_json = json.loads(res.data)
    assert res.status_code == 200
    assert len(res_json['order']['order_details']) == 1


def test_add_to_cart_with_insufficient_stocks(client, access_token, admin_access_token):
    product_id = setup_initial_coondition(client, admin_access_token)

    res = client.post(
        "/api/v1/order/cart",
        json={
            "product_id": product_id,
            "quantity": 15
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
    )
    res_json = json.loads(res.data)
    assert res.status_code == 400


def test_get_active_cart(client, access_token, admin_access_token):
    product_id = setup_initial_coondition(client, admin_access_token)

    # there should not be order and active cart before we add product into cart
    res = client.get(
        "/api/v1/order/cart",
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
    )

    res_json = json.loads(res.data)
    assert res.status_code == 200
    assert res_json['order'] == {}

    # add product into cart
    res = client.post(
        "/api/v1/order/cart",
        json={
            "product_id": product_id,
            "quantity": 5
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
    )
    res_json = json.loads(res.data)
    assert res.status_code == 200
    assert len(res_json['order']['order_details']) == 1

    # there should be active cart after we add product into cart
    res = client.get(
        "/api/v1/order/cart",
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
    )

    res_json = json.loads(res.data)
    assert res.status_code == 200
    assert len(res_json['order']['order_details']) == 1
