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


# --- property types ---


async def test_list_property_types_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/properties/types",
        json=[{"id": 1, "isErasable": False, "position": 1, "cast": "string"}],
    )
    result = await orders.list_property_types()
    assert result[0]["id"] == 1


async def test_list_property_types_sends_lang_filter(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/properties/types?lang=en%2Cde",
        json=[],
    )
    await orders.list_property_types(lang=["en", "de"])


async def test_create_property_type_posts_data(httpx_mock, orders):
    payload = {
        "lang": "en",
        "name": "Gift wrap",
        "names": [{"lang": "de", "name": "Geschenkverpackung"}],
    }
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/properties/types",
        json={"id": 1001, "isErasable": True, "position": 1},
    )
    result = await orders.create_property_type(payload)
    assert result["id"] == 1001
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == payload


async def test_delete_property_type_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/properties/types/1001",
        json={},
    )
    result = await orders.delete_property_type(1001)
    assert result == {}


async def test_get_property_type_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/properties/types/1001",
        json={"id": 1001, "isErasable": True, "position": 1},
    )
    result = await orders.get_property_type(1001)
    assert result["id"] == 1001


async def test_update_property_type_puts_data(httpx_mock, orders):
    payload = {"lang": "en", "name": "Gift wrap (updated)"}
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/properties/types/1001",
        json={"id": 1001, "isErasable": True, "position": 1},
    )
    result = await orders.update_property_type(1001, payload)
    assert result["id"] == 1001
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == payload


# --- order-level property values ---


async def test_delete_order_property_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/properties/501",
        json={},
    )
    result = await orders.delete_order_property(501)
    assert result == {}


async def test_update_order_property_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/properties/501",
        json={"id": 501, "orderId": 42, "typeId": 1, "value": "A1"},
    )
    result = await orders.update_order_property(501, type_id=1, value="A1")
    assert result["value"] == "A1"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {"id": 501, "typeId": 1, "value": "A1"}


async def test_create_order_property_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/properties",
        json={"id": 501, "orderId": 42, "typeId": 1, "value": "A1"},
    )
    result = await orders.create_order_property(42, type_id=1, value="A1")
    assert result["id"] == 501
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "orderId": 42,
        "typeId": 1,
        "value": "A1",
    }


async def test_list_order_properties_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/properties/1",
        json=[{"id": 501, "orderId": 42, "typeId": 1, "value": "A1"}],
    )
    result = await orders.list_order_properties(42, type_id=1)
    assert result[0]["value"] == "A1"


async def test_delete_order_property_by_type_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/42/properties/1",
        json={},
    )
    result = await orders.delete_order_property_by_type(42, type_id=1)
    assert result == {}


async def test_update_order_property_by_type_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42/properties/1",
        json={"id": 501, "orderId": 42, "typeId": 1, "value": "A2"},
    )
    result = await orders.update_order_property_by_type(42, type_id=1, value="A2")
    assert result["value"] == "A2"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "orderId": 42,
        "typeId": 1,
        "value": "A2",
    }
