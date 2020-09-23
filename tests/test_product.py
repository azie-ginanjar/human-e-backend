import json
import time

from grocery_mart_api.models import Inventory


def test_add_product_by_admin(client, admin_access_token):
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
    print(res_json)
    assert res.status_code == 200
    assert res_json['product']['price'] == 200.01

    # validate that record generated on inventory
    inventories = Inventory.query.all()

    assert len(inventories) == 1


def test_add_product_by_user(client, access_token):
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
    res = client.put(
        "/api/v1/product/",
        json={
            "id": product.id,
            "price": 200.01
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + admin_access_token
        },
    )
    print(res.data)
    res_json = json.loads(res.data)
    assert res.status_code == 200
    assert res_json['product']['price'] == 200.01


def test_update_product_by_user(client, access_token, product):
    res = client.put(
        "/api/v1/product/",
        json={
            "id": product.id,
            "price": 200.01
        },
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        },
    )

    assert res.status_code == 403


def test_stock_in_product_by_admin(client, admin_access_token):
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
    assert res.status_code == 200
    assert res_json['product']['price'] == 200.01

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
    assert res.status_code == 200
    # validate that record generated on inventory
    inventory = Inventory.query.filter(
        Inventory.product_id == product_id
    ).first()

    assert inventory.stock == 10
