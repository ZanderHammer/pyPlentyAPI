import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.orders import OrdersModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def orders(session):
    return OrdersModule(session)


async def test_list_status_definitions_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/statuses?page=1&itemsPerPage=50",
        json={
            "page": 1,
            "totalsCount": 1,
            "isLastPage": True,
            "entries": [{"statusId": 5.0}],
        },
    )
    result = await orders.list_status_definitions()
    assert result["entries"][0]["statusId"] == 5.0


async def test_list_status_definitions_sends_filters(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/statuses"
            "?statusIdFrom=1.0&statusIdTo=9.0&language=en&page=1&itemsPerPage=50"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_status_definitions(
        status_id_from=1.0, status_id_to=9.0, language="en"
    )
    assert result["page"] == 1


async def test_paginate_status_definitions_yields_all_items(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/statuses?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"statusId": 1.0}, {"statusId": 2.0}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/statuses?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"statusId": 3.0}],
        },
    )
    results = [s async for s in orders.paginate_status_definitions(items_per_page=2)]
    assert [r["statusId"] for r in results] == [1.0, 2.0, 3.0]


async def test_list_all_status_definitions_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/statuses/all",
        json=[{"statusId": 1.0}, {"statusId": 2.0}],
    )
    result = await orders.list_all_status_definitions()
    assert result[0]["statusId"] == 1.0


async def test_create_status_definition_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/statuses",
        json={"statusId": 10.0, "color": "#ff0000"},
    )
    result = await orders.create_status_definition(
        10.0, [{"lang": "en", "name": "Custom"}]
    )
    assert result["statusId"] == 10.0
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "statusId": 10.0,
        "names": [{"lang": "en", "name": "Custom"}],
    }


async def test_get_status_definition_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/statuses/5.0",
        json={"statusId": 5.0, "color": "#00ff00"},
    )
    result = await orders.get_status_definition(5.0)
    assert result["color"] == "#00ff00"


async def test_rename_status_definition_puts_names(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/statuses/5.0",
        json={"statusId": 5.0},
    )
    await orders.rename_status_definition(
        5.0, [{"lang": "de", "name": "Warten auf Zahlung"}]
    )
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "names": [{"lang": "de", "name": "Warten auf Zahlung"}]
    }


async def test_delete_status_definition_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/statuses/5.0",
        json={},
    )
    result = await orders.delete_status_definition(5.0)
    assert result == {}


async def test_update_status_definition_properties_sends_query_params(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="POST",
        url=(
            f"{BASE_URL}/rest/orders/statuses/group_functions"
            "?newStatusValues=color%3Ared&selectedStatusList=3.0%2C5.0"
        ),
        json={},
    )
    result = await orders.update_status_definition_properties(
        [3.0, 5.0], ["color:red"]
    )
    assert result == {}
