import pytest
import httpx
from datetime import datetime, timedelta, timezone

from plentymarkets._session import _Session
from plentymarkets.modules.contacts import ContactsModule

BASE_URL = "https://shop.example.com"


@pytest.fixture
def session(httpx_mock):
    client = httpx.AsyncClient()
    s = _Session(BASE_URL, "u", "p", client)
    s._access_token = "tok"
    s._token_expiry = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    return s


@pytest.fixture
def contacts(session):
    return ContactsModule(session)


async def test_get_calls_correct_url(httpx_mock, contacts):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts/7",
        json={"id": 7, "firstName": "Max"},
    )
    result = await contacts.get(7)
    assert result["id"] == 7


async def test_list_sends_pagination_params(httpx_mock, contacts):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await contacts.list()
    assert result["page"] == 1


async def test_create_posts_data(httpx_mock, contacts):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/accounts/contacts",
        json={"id": 88, "firstName": "Anna"},
    )
    result = await contacts.create({"firstName": "Anna", "typeId": 1})
    assert result["id"] == 88


async def test_update_puts_to_contact_url(httpx_mock, contacts):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/accounts/contacts/7",
        json={"id": 7, "firstName": "Max Updated"},
    )
    result = await contacts.update(7, {"firstName": "Max Updated"})
    assert result["firstName"] == "Max Updated"


async def test_paginate_contacts_yields_all_contacts(httpx_mock, contacts):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/accounts/contacts?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [c async for c in contacts.paginate_contacts(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]
