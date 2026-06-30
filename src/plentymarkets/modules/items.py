from __future__ import annotations

from .._session import _Session


class ItemsModule:
    def __init__(self, session: _Session) -> None:
        self._session = session
