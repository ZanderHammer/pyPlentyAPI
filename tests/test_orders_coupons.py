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
