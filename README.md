# pyPlentyAPI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![UV: Sync](https://img.shields.io/badge/uv-sync-3178C6.svg?logo=python&logoColor=white)](https://github.com/astral-sh/uv)
[![Tests: Pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)

Async Python client for the [PlentyMarkets REST API](https://developers.plentymarkets.com/en-gb/plentymarkets-rest-api/index.html).

## Features
- **Async-first**: Built on `httpx.AsyncClient` for high-performance async/await support.
- **Lazy-loaded modules**: Access `orders`, `items`, `stock`, and `contacts` as properties of `PlentyClient`.
- **Auto-refreshing auth**: Tokens are refreshed automatically when within 60 seconds of expiry.
- **Comprehensive error handling**: Custom exceptions for HTTP status codes (e.g., `NotFoundError`, `RateLimitError`).
- **Pagination support**: Async generators for iterating across all pages of results.
- **Type hints**: Full type annotations for IDE support and static analysis.

## Installation
```bash
pip install plentymarkets-api-client
```

Or with `uv`:
```bash
uv add plentymarkets-api-client
```

## Quickstart
```python
import asyncio
from plentymarkets import PlentyClient

async def main():
    async with PlentyClient(username="your_username", password="your_password") as client:
        # Fetch an order by ID
        order = await client.orders.get(123)
        print(order)
        
        # List all items (paginated)
        async for item in client.items.paginate_items():
            print(item)

asyncio.run(main())
```

## Modules
| Module    | Description                          | Key Methods                                                                                     |
|-----------|--------------------------------------|-------------------------------------------------------------------------------------------------|
| **Orders**    | Manage orders, order items, item transactions, serial numbers, and reorders. | `get()`, `list()`, `create()`, `update_status()`, `search()`, `delete()`, `cancel()`, `list_order_items()`, `search_item_transactions()`, `create_order_transactions()`, `paginate_orders()` |
| **Items**     | Manage items and item variants.      | `get()`, `list()`, `create()`, `update()`, `paginate_items()`                                   |
| **Stock**     | Manage stock, warehouses, storage locations, and stock movements. | `get_by_warehouse()`, `correct()`, `list_warehouses()`, `book_incoming_items()`, `book_outgoing_items()`, `redistribute_stock()`, `paginate_stock()` |
| **Contacts**  | Manage customer and supplier data.   | `get()`, `list()`, `create()`, `update()`, `paginate_contacts()`                                |
| **Pim**       | Product Information Management — variations, attributes, categories, sales prices, barcodes, and more. | `client.pim.*` (70+ methods) |

## API Coverage

Endpoint totals are counted against the [PlentyMarkets OpenAPI spec](https://raw.githubusercontent.com/plentymarkets/api-doc/master/plentymarkets/openApiV3/openApiV3.json), grouped by its own tags.

| Module      | Endpoints  | Status                          |
|-------------|------------|----------------------------------|
| **Pim**         | 41 / 41    | ✅ Complete                      |
| **Stock**       | 17 / 17    | ✅ Complete                      |
| **Order**       | 45 / 307   | Lifecycle, items & transactions  |
| **Item**        | 2 / 146    | Core operations                  |
| **Account**     | 2 / 87     | Core operations                  |

`Pim` reached full endpoint coverage in `v0.2.0`, `Stock` shortly after — see [ROADMAP.md](ROADMAP.md) for the endpoint-by-endpoint breakdown and the rest of the API surface still planned. `Stock`'s 17 endpoints live under the API's `StockManagement` tag.

## Authentication
1. Initialize `PlentyClient` with your PlentyMarkets username and password.
2. The client automatically logs in and manages the `accessToken` lifecycle.
3. Tokens are sent as `Authorization: Bearer <token>` in all requests.
4. If a 401 error occurs, the client attempts to re-login once before failing.

## Error Handling
Custom exceptions are raised for HTTP errors:
- `AuthError`: 401 Unauthorized
- `NotFoundError`: 404 Not Found  
- `RateLimitError`: 429 Too Many Requests
- `ServerError`: 5xx Server Errors
- `ConnectionError`: Network failures

Example:
```python
try:
    order = await client.orders.get(99999)
except plentymarkets.NotFoundError:
    print("Order not found")
except plentymarkets.RateLimitError:
    print("Rate limit exceeded")
```

## Pagination
Use async generators to iterate across all pages:
```python
async for order in client.orders.paginate_orders():
    print(order)
```

## Development
### Setup
```bash
uv sync --extra dev
uv run pre-commit install --hook-type commit-msg
```

### Running Tests
```bash
uv run pytest                        # Unit tests
uv run pytest -m integration         # Integration tests (requires live credentials)
```

## License
MIT
