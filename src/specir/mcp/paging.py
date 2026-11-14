"""Every set a tool returns travels as one page: its items, the total, and whether it was cut."""

from __future__ import annotations

from typing import Any, Sequence

DEFAULT_LIMIT = 50
MAX_LIMIT = 500


def page(items: Sequence[Any], offset: int = 0, limit: int = DEFAULT_LIMIT, explanation: str | None = None) -> dict[str, Any]:
    """`{items, total, offset, limit, truncated, next_offset}` for `items[offset:offset+limit]`.

    `truncated` is true when items remain after this page; `next_offset` is where the next
    page starts, or None on the last page. An empty set carries `explanation` (why it is
    empty) when the caller knows it.
    """
    if offset < 0:
        raise ValueError(f"offset must be >= 0, not {offset}")
    if not 1 <= limit <= MAX_LIMIT:
        raise ValueError(f"limit must be between 1 and {MAX_LIMIT}, not {limit}")
    total = len(items)
    end = offset + limit
    result: dict[str, Any] = {
        "items": list(items[offset:end]),
        "total": total,
        "offset": offset,
        "limit": limit,
        "truncated": end < total,
        "next_offset": end if end < total else None,
    }
    if explanation is not None:
        result["explanation"] = explanation
    return result
