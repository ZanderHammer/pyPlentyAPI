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


async def test_get_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42",
        json={"id": 42, "statusId": 5.0},
    )
    result = await orders.get(42)
    assert result["id"] == 42


async def test_list_sends_pagination_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=2&itemsPerPage=25",
        json={"page": 2, "totalsCount": 50, "isLastPage": True, "entries": []},
    )
    result = await orders.list(page=2, items_per_page=25)
    assert result["page"] == 2


async def test_list_defaults_to_page_1_and_50(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    await orders.list()
    request = httpx_mock.get_request()
    assert "page=1" in str(request.url)
    assert "itemsPerPage=50" in str(request.url)


async def test_create_posts_data(httpx_mock, orders):
    payload = {"typeId": 1, "plentyId": 12345}
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders",
        json={"id": 99, "typeId": 1},
    )
    result = await orders.create(payload)
    assert result["id"] == 99


async def test_update_status_puts_to_order_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42",
        json={"id": 42, "statusId": 8.0},
    )
    result = await orders.update_status(42, status_id=8.0)
    assert result["statusId"] == 8.0


async def test_paginate_orders_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [order async for order in orders.paginate_orders(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_orders_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [o async for o in orders.paginate_orders()]
    assert results == []


async def test_delete_sends_delete_request(httpx_mock, orders):
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/rest/orders/42",
        json={},
    )
    result = await orders.delete(42)
    assert result == {}


async def test_cancel_puts_to_cancel_url_with_no_body(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42/cancel",
        json={"id": 42, "statusId": 8.0},
    )
    result = await orders.cancel(42)
    assert result["statusId"] == 8.0
    request = httpx_mock.get_request()
    assert request.content == b"{}"


async def test_cancel_sends_status_id_and_message(httpx_mock, orders):
    httpx_mock.add_response(
        method="PUT",
        url=f"{BASE_URL}/rest/orders/42/cancel",
        json={"id": 42, "statusId": 8.0},
    )
    await orders.cancel(42, status_id=8.0, message="Cancelled by customer")
    request = httpx_mock.get_request()
    import json as _json

    assert _json.loads(request.content) == {
        "statusId": 8.0,
        "message": "Cancelled by customer",
    }


async def test_get_family_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/family",
        json={"originOrderId": 10, "mainSalesOrderId": 42},
    )
    result = await orders.get_family(42)
    assert result["originOrderId"] == 10


async def test_get_my_account_url_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/my_account_url",
        json=["https://shop.example.com/my-account/orders/42"],
    )
    result = await orders.get_my_account_url(42)
    assert result == ["https://shop.example.com/my-account/orders/42"]


async def test_search_defaults_to_page_1_and_50(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/search?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search()
    assert result["page"] == 1


async def test_search_sends_filters_with_and_sort_params(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/search?statusId=5.0&with=documents%2Caddress"
            "&page=1&itemsPerPage=50&sortBy=updatedAt&sortOrder=desc"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search(
        filters={"statusId": 5.0},
        with_=["documents", "address"],
        sort_by="updatedAt",
        sort_order="desc",
    )
    assert result["page"] == 1


async def test_search_use_post_hits_post_endpoint(httpx_mock, orders):
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/rest/orders/search?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.search(use_post=True)
    assert result["page"] == 1


async def test_paginate_search_yields_all_items_across_pages(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/search?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/search?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [o async for o in orders.paginate_search(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_paginate_search_stops_on_empty_entries(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/search?page=1&itemsPerPage=50",
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    results = [o async for o in orders.paginate_search()]
    assert results == []


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


async def test_list_status_history_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/status-history?page=1&itemsPerPage=50",
        json={
            "page": 1,
            "totalsCount": 1,
            "isLastPage": True,
            "entries": [{"id": 1, "orderId": 42, "statusId": 5.0}],
        },
    )
    result = await orders.list_status_history()
    assert result["entries"][0]["orderId"] == 42


async def test_list_status_history_sends_filters(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=(
            f"{BASE_URL}/rest/orders/status-history"
            "?orderId=42&statusId=5.0&page=1&itemsPerPage=50"
        ),
        json={"page": 1, "totalsCount": 0, "isLastPage": True, "entries": []},
    )
    result = await orders.list_status_history(order_id=42, status_id=5.0)
    assert result["page"] == 1


async def test_paginate_status_history_yields_all_items(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/status-history?page=1&itemsPerPage=2",
        json={
            "page": 1,
            "totalsCount": 3,
            "isLastPage": False,
            "entries": [{"id": 1}, {"id": 2}],
        },
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/status-history?page=2&itemsPerPage=2",
        json={
            "page": 2,
            "totalsCount": 3,
            "isLastPage": True,
            "entries": [{"id": 3}],
        },
    )
    results = [h async for h in orders.paginate_status_history(items_per_page=2)]
    assert [r["id"] for r in results] == [1, 2, 3]


async def test_get_order_status_history_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/status-history",
        json=[{"id": 1, "orderId": 42, "statusId": 3.0}],
    )
    result = await orders.get_order_status_history(42)
    assert result[0]["statusId"] == 3.0


async def test_list_date_types_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/dates/types",
        json=[{"id": 2, "isErasable": False, "position": 1}],
    )
    result = await orders.list_date_types()
    assert result[0]["id"] == 2


async def test_get_date_type_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/dates/types/7",
        json={"id": 7, "isErasable": True, "position": 3},
    )
    result = await orders.get_date_type(7)
    assert result["id"] == 7


async def test_list_date_type_names_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/dates/types/7/names",
        json=[{"id": 1, "typeId": 7, "lang": "en", "name": "Payment due date"}],
    )
    result = await orders.list_date_type_names(7)
    assert result[0]["lang"] == "en"


async def test_get_date_type_name_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/dates/types/7/names/de",
        json={"id": 1, "typeId": 7, "lang": "de", "name": "Zahlungsziel"},
    )
    result = await orders.get_date_type_name(7, "de")
    assert result["name"] == "Zahlungsziel"


async def test_list_order_dates_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/dates",
        json=[{"id": 1, "orderId": 42, "typeId": 2}],
    )
    result = await orders.list_order_dates(42)
    assert result[0]["orderId"] == 42


async def test_get_order_date_calls_correct_url(httpx_mock, orders):
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/rest/orders/42/dates/7",
        json={"id": 1, "orderId": 42, "typeId": 7},
    )
    result = await orders.get_order_date(42, 7)
    assert result["typeId"] == 7
