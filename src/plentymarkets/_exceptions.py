class PlentyError(Exception):
    """Base exception for all plentymarkets client errors."""


class AuthError(PlentyError):
    """Raised on 401 responses or when login credentials are rejected."""


class NotFoundError(PlentyError):
    """Raised on 404 responses."""


class RateLimitError(PlentyError):
    """Raised on 429 responses.

    Attributes:
        retry_after: Seconds to wait before retrying, taken from the
            ``Retry-After`` response header. ``0`` if the header is absent.
    """

    def __init__(self, message: str, retry_after: int = 0) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class ServerError(PlentyError):
    """Raised on 5xx responses."""


class ConnectionError(PlentyError):
    """Raised when the network is unreachable, DNS fails, or a timeout occurs."""
