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


# --- campaigns and coupon codes ---


async def test_list_campaigns_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns",
        json={"page": 1, "totalsCount": 1, "isLastPage": True, "entries": [{"id": 1}]},
    )
    result = await orders.list_campaigns()
    assert result["entries"][0]["id"] == 1


async def test_delete_coupon_code_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/codes/SAVE10",
        json={},
    )
    result = await orders.delete_coupon_code("SAVE10")
    assert result == {}


async def test_get_coupon_code_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/codes/SAVE10",
        json={"code": "SAVE10", "campaignId": 1, "value": 10.0},
    )
    result = await orders.get_coupon_code("SAVE10")
    assert result["value"] == 10.0


async def test_set_coupon_code_disabled_puts_no_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/codes/SAVE10/disabled/1",
        json={},
    )
    result = await orders.set_coupon_code_disabled("SAVE10", 1)
    assert result == {}
    request = httpx_mock.get_request()
    assert request.content == b""


async def test_get_campaign_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/1",
        json={"id": 1, "name": "Summer Sale"},
    )
    result = await orders.get_campaign(1)
    assert result["name"] == "Summer Sale"


async def test_create_coupon_code_posts_data(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/coupons/campaigns/1/codes",
        json={"code": "SAVE20", "campaignId": 1, "value": 20.0},
    )
    result = await orders.create_coupon_code(1, {"code": "SAVE20", "value": 20.0})
    assert result["code"] == "SAVE20"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "code": "SAVE20",
        "value": 20.0,
        "campaignId": 1,
    }


# --- validation and redemption ---


async def test_validate_coupons_sends_params_and_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=(
            f"{BASE_URL}/rest/orders/coupons/codes?coupons=SAVE10"
            "&plentyId=12345&shipToCountry=1"
        ),
        json=[{"campaignId": 1, "couponCode": "SAVE10"}],
    )
    result = await orders.validate_coupons(
        coupons=["SAVE10"],
        plenty_id=12345,
        ship_to_country=1,
        data={"contactId": 7, "items": [{"itemId": 100, "quantity": 1}]},
    )
    assert result[0]["couponCode"] == "SAVE10"
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "contactId": 7,
        "items": [{"itemId": 100, "quantity": 1}],
    }


async def test_list_redeemed_coupon_codes_sends_pagination_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/codes/contacts/7?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_redeemed_coupon_codes(7)
    assert result["page"] == 1


async def test_paginate_redeemed_coupon_codes_yields_all_items_across_pages(
    httpx_mock, orders
):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/codes/contacts/7?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"code": "A"}, {"code": "B"}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/coupons/codes/contacts/7?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"code": "C"}],
        },
    )
    results = [
        c
        async for c in orders.paginate_redeemed_coupon_codes(7, items_per_page=2)
    ]
    assert [r["code"] for r in results] == ["A", "B", "C"]


async def test_validate_coupon_sends_params_and_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=(
            f"{BASE_URL}/rest/orders/coupons/codes/SAVE10?plentyId=12345"
            "&shipToCountry=1"
        ),
        json={"campaignId": 1, "couponCode": "SAVE10"},
    )
    result = await orders.validate_coupon(
        "SAVE10",
        plenty_id=12345,
        ship_to_country=1,
        data={"contactId": 7, "items": [{"itemId": 100, "quantity": 1}]},
    )
    assert result["couponCode"] == "SAVE10"


async def test_redeem_coupon_posts_with_no_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/coupons/SAVE10",
        json={"campaignId": 1, "couponCode": "SAVE10"},
    )
    result = await orders.redeem_coupon(42, "SAVE10")
    assert result["couponCode"] == "SAVE10"


async def test_validate_order_coupon_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/42/coupons/SAVE10/validate",
        json=[{"valid": True}],
    )
    result = await orders.validate_order_coupon(42, "SAVE10")
    assert result == [{"valid": True}]
