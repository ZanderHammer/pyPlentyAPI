from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

_JsonDict = dict[str, Any]

import httpx

from ._exceptions import (
    AuthError,
    ConnectionError,
    NotFoundError,
    PlentyError,
    RateLimitError,
    ServerError,
)

_REFRESH_BUFFER_SECONDS = 60


class _Session:
    """Manages the httpx client, login state, and token lifecycle.

    Args:
        base_url: PlentyMarkets shop base URL, e.g. ``https://your-shop.plentymarkets.com``.
        username: PlentyMarkets back-end user e-mail.
        password: PlentyMarkets back-end user password.
        client: Shared ``httpx.AsyncClient`` instance.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        client: httpx.AsyncClient,
    ) -> None:
        stripped = base_url.rstrip("/")
        if "/rest" in stripped.split("//", 1)[-1]:
            raise ValueError(
                f"base_url must be the shop root without '/rest', got: {base_url!r}. "
                "Example: 'https://your-shop.plentymarkets.com'"
            )
        self._base_url = stripped
        self._username = username
        self._password = password
        self._client = client
        self._access_token: str | None = None
        self._token_expiry: datetime | None = None

    @staticmethod
    def _raise_for_status(response: httpx.Response, path: str = "/rest/login") -> None:
        """Map HTTP error responses to PlentyError subclasses.

        Args:
            response: The httpx response to check.
            path: Path string used in error messages.

        Raises:
            AuthError: On 401 responses.
            NotFoundError: On 404 responses.
            RateLimitError: On 429 responses.
            ServerError: On 5xx responses.
        """
        if response.status_code == 401:
            raise AuthError(f"Authentication failed: {path}")
        if response.status_code == 404:
            raise NotFoundError(f"{path} returned 404")
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 0))
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        if response.status_code >= 500:
            raise ServerError(f"Server error {response.status_code}: {path}")

    def _is_token_expiring(self) -> bool:
        """Return True if the token is absent or within the refresh buffer window.

        Returns:
            True when re-authentication is required before the next request.
        """
        if self._access_token is None or self._token_expiry is None:
            return True
        return datetime.now(tz=timezone.utc) >= self._token_expiry - timedelta(
            seconds=_REFRESH_BUFFER_SECONDS
        )

    async def login(self) -> None:
        """Authenticate and store the access token.

        Raises:
            AuthError: If the server rejects the credentials (HTTP 401).
            ServerError: On 5xx responses from the login endpoint.
            RateLimitError: On 429 responses from the login endpoint.
            ConnectionError: On network failures reaching the login endpoint.
        """
        try:
            response = await self._client.post(
                f"{self._base_url}/rest/login",
                json={"username": self._username, "password": self._password},
            )
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            raise ConnectionError(str(exc)) from exc
        self._raise_for_status(response, "/rest/login")
        if response.status_code >= 400:
            raise PlentyError(f"Login error {response.status_code}")
        data = response.json()
        self._access_token = data["accessToken"]
        self._token_expiry = datetime.now(tz=timezone.utc) + timedelta(
            seconds=data["expiresIn"]
        )

    async def logout(self) -> None:
        """Invalidate the current session token on the server and clear local state.

        If there is no active token, this method is a no-op and makes no network
        calls. Local state is always cleared, even if the DELETE request fails.
        """
        if self._access_token is None:
            return
        try:
            await self._client.delete(
                f"{self._base_url}/rest/login",
                headers={"Authorization": f"Bearer {self._access_token}"},
            )
        finally:
            self._access_token = None
            self._token_expiry = None

    async def _request(self, method: str, path: str, **kwargs: Any) -> _JsonDict:
        """Send an authenticated HTTP request, refreshing the token if needed.

        Args:
            method: HTTP method (``GET``, ``POST``, ``PUT``, ``DELETE``).
            path: URL path appended to ``base_url``, e.g. ``/rest/orders/1``.
            **kwargs: Extra arguments forwarded to ``httpx.AsyncClient.request``.

        Returns:
            Parsed JSON response body, or ``{}`` for empty responses (HTTP 204).

        Raises:
            AuthError: On persistent 401 after one re-login attempt.
            NotFoundError: On HTTP 404.
            RateLimitError: On HTTP 429.
            ServerError: On HTTP 5xx.
            ConnectionError: On network-level failures.
        """
        if self._is_token_expiring():
            await self.login()

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._access_token}"

        try:
            response = await self._client.request(
                method,
                f"{self._base_url}{path}",
                headers=headers,
                **kwargs,
            )
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            raise ConnectionError(str(exc)) from exc

        if response.status_code == 401:
            await self.login()
            headers["Authorization"] = f"Bearer {self._access_token}"
            try:
                response = await self._client.request(
                    method,
                    f"{self._base_url}{path}",
                    headers=headers,
                    **kwargs,
                )
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                raise ConnectionError(str(exc)) from exc
            if response.status_code == 401:
                raise AuthError("Authentication failed after token refresh")

        if response.status_code == 404:
            raise NotFoundError(f"{method} {path} returned 404")
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 0))
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        if response.status_code >= 500:
            raise ServerError(f"Server error {response.status_code}: {method} {path}")
        if response.status_code >= 400:
            raise PlentyError(f"Client error {response.status_code}: {method} {path}")

        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    async def get(self, path: str, **kwargs: Any) -> _JsonDict:
        """Send an authenticated GET request.

        Args:
            path: URL path appended to ``base_url``.
            **kwargs: Extra arguments forwarded to ``httpx.AsyncClient.request``.

        Returns:
            Parsed JSON response body.
        """
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> _JsonDict:
        """Send an authenticated POST request.

        Args:
            path: URL path appended to ``base_url``.
            **kwargs: Extra arguments forwarded to ``httpx.AsyncClient.request``.

        Returns:
            Parsed JSON response body.
        """
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> _JsonDict:
        """Send an authenticated PUT request.

        Args:
            path: URL path appended to ``base_url``.
            **kwargs: Extra arguments forwarded to ``httpx.AsyncClient.request``.

        Returns:
            Parsed JSON response body.
        """
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> _JsonDict:
        """Send an authenticated DELETE request.

        Args:
            path: URL path appended to ``base_url``.
            **kwargs: Extra arguments forwarded to ``httpx.AsyncClient.request``.

        Returns:
            Parsed JSON response body.
        """
        return await self._request("DELETE", path, **kwargs)
