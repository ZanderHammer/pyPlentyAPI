import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


async def test_attach_order_item_warehouse_locations_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/items/warehouse_locations/attach",
        json={},
    )
    payload = {"orderItemId": 77, "warehouseLocationId": 5}
    result = await orders.attach_order_item_warehouse_locations(42, payload)
    assert result == {}
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == payload


async def test_detach_order_item_warehouse_locations_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/items/warehouse_locations/detach",
        json={},
    )
    payload = {"orderItemId": 77, "warehouseLocationId": 5}
    result = await orders.detach_order_item_warehouse_locations(42, payload)
    assert result == {}
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == payload


async def test_generate_order_item_reorders_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/items/reorders/generate",
        json=[{"id": 1}],
    )
    payload = {"orderItemIds": [77]}
    result = await orders.generate_order_item_reorders(42, payload)
    assert result == [{"id": 1}]
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == payload


async def test_generate_order_item_reorders_posts_without_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/items/reorders/generate",
        json=[],
    )
    result = await orders.generate_order_item_reorders(42)
    assert result == []
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_create_order_reorder_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/reorders",
        json={"id": 99, "typeId": 12, "statusId": 1.0},
    )
    payload = {"quantity": 2}
    result = await orders.create_order_reorder(42, payload)
    assert result["id"] == 99
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == payload


async def test_generate_order_reorders_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/reorders/generate",
        json=[{"id": 1}],
    )
    payload = {"orderIds": [1, 2]}
    result = await orders.generate_order_reorders(42, payload)
    assert result == [{"id": 1}]
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == payload


async def test_generate_order_reorders_posts_without_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/reorders/generate",
        json=[],
    )
    result = await orders.generate_order_reorders(42)
    assert result == []
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_validate_order_reorders_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/reorders/generate/validate",
        json=[{"valid": True}],
    )
    payload = {"orderItemIds": [77]}
    result = await orders.validate_order_reorders(42, payload)
    assert result == [{"valid": True}]
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == payload


async def test_validate_order_reorders_posts_without_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/reorders/generate/validate",
        json=[],
    )
    result = await orders.validate_order_reorders(42)
    assert result == []
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_create_order_transactions_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/transactions",
        json=[{"id": 1, "orderItemId": 77, "direction": "in", "status": "regular"}],
    )
    result = await orders.create_order_transactions(
        42, {"direction": "in", "status": "regular"}
    )
    assert result[0]["orderItemId"] == 77
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {"direction": "in", "status": "regular"}
