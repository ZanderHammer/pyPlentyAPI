from __future__ import annotations

from typing import Any

from ..._session import Session


class OrdersBase:
    """Shared state and helpers for every ``OrdersModule`` mixin.

    ``_session`` is declared here only as a class-level type annotation (no
    ``__init__``) so every mixin's methods can reference ``self._session``
    with type-checker support; the attribute is actually assigned once, in
    ``OrdersModule.__init__``.
    """

    _session: Session

    @staticmethod
    def _build_params(
        filters: dict[str, Any] | None = None,
        with_: list[str] | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        params: dict[str, Any] = dict(filters) if filters else {}
        if with_:
            params["with"] = ",".join(with_)
        params.update({k: v for k, v in extra.items() if v is not None})
        return params
