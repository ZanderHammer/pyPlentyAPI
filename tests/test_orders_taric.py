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


async def test_list_taric_vat_assignments_defaults_to_page_1_and_50(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_taric_vat_assignments()
    assert result["page"] == 1


async def test_paginate_taric_vat_assignments_yields_all_items_across_pages(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [
        t async for t in orders.paginate_taric_vat_assignments(items_per_page=2)
    ]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_delete_taric_vat_assignment_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment/8471/1",
        json={},
    )
    result = await orders.delete_taric_vat_assignment("8471", 1)
    assert result == {}
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_get_taric_vat_assignment_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment/8471/1",
        json={"id": 1, "taricCode": "8471", "countryId": 1, "vatField": "1"},
    )
    result = await orders.get_taric_vat_assignment("8471", 1)
    assert result["taricCode"] == "8471"


async def test_create_taric_vat_assignment_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment/8471/1",
        json={"id": 1, "taricCode": "8471", "countryId": 1, "vatField": "1"},
    )
    result = await orders.create_taric_vat_assignment("8471", 1, vat_field="1")
    assert result["id"] == 1
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "taricCode": "8471",
        "countryId": 1,
        "vatField": "1",
    }


async def test_update_taric_vat_assignment_puts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/system/settings/taric_vat_assignment/8471/1",
        json={"id": 1, "taricCode": "8471", "countryId": 1, "vatField": "2"},
    )
    result = await orders.update_taric_vat_assignment("8471", 1, vat_field="2")
    assert result["vatField"] == "2"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "taricCode": "8471",
        "countryId": 1,
        "vatField": "2",
    }
