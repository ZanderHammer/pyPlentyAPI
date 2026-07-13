import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import Session
from plentymarkets.modules.pim import PimModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def pim(session):
    return PimModule(session)


async def test_list_item_serial_numbers(httpx_mock, pim):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/pim/item-serial-numbers",
        json={"entries": [{"id": 1, "itemId": 42, "serialNumber": "SN-001"}], "totalsCount": 1},
    )
    result = await pim.list_item_serial_numbers()
    assert result["totalsCount"] == 1


async def test_create_item_serial_numbers_posts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/pim/item-serial-numbers",
        json={"created": 1},
    )
    result = await pim.create_item_serial_numbers(
        [{"itemId": 42, "serialNumber": "SN-002"}]
    )
    assert result["created"] == 1


async def test_update_item_serial_numbers_puts_data(httpx_mock, pim):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/pim/item-serial-numbers",
        json={"updated": 1},
    )
    result = await pim.update_item_serial_numbers(
        [{"itemId": 42, "serialNumber": "SN-002", "orderId": 100}]
    )
    assert result["updated"] == 1


async def test_delete_item_serial_numbers_sends_ids(httpx_mock, pim):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/pim/item-serial-numbers",
        json={"deleted": 1},
    )
    result = await pim.delete_item_serial_numbers([1])
    assert result["deleted"] == 1
