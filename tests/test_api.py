import httpx
import pytest

BASE_URL = "https://ecom-fastapi-wnzl.onrender.com"  # 👈 Use local URL for local FastAPI run

product_id = None
order_id = None
user_id = "user123"


def test_create_product():
    global product_id

    payload = {
        "name": "Test Hoodie",
        "price": 899.0,
        "sizes": [
            {"size": "M", "quantity": 12},
            {"size": "L", "quantity": 7}
        ]
    }

    response = httpx.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 201
    product_id = response.json()["id"]
    assert isinstance(product_id, str)


def test_list_products():
    response = httpx.get(f"{BASE_URL}/products?size=M&limit=5&offset=0")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body and "page" in body
    assert isinstance(body["data"], list)
    for product in body["data"]:
        assert "id" in product
        assert "name" in product
        assert "price" in product
        assert "sizes" not in product  # ❗ very important


def test_create_order():
    global product_id, order_id

    payload = {
        "userId": user_id,
        "items": [
            {
                "productId": product_id,
                "qty": 2
            }
        ]
    }

    response = httpx.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 201
    order_id = response.json()["id"]
    assert isinstance(order_id, str)


def test_get_orders():
    response = httpx.get(f"{BASE_URL}/orders/{user_id}?limit=5&offset=0")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body and "page" in body
    assert isinstance(body["data"], list)
    for order in body["data"]:
        assert "id" in order
        assert "items" in order
        assert "total" in order
        for item in order["items"]:
            assert "productDetails" in item
            assert "qty" in item
            assert "name" in item["productDetails"]
            assert "id" in item["productDetails"]

