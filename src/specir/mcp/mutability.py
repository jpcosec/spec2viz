"""The write level the server allows, fixed when it starts (IR02 D3-A).

Levels follow the contract adopted from pron §5 and are cumulative: 0 reads only (the
default, IR03); 1 writes content (documents of registered models and authored edges,
`RelationDoc`); 2 also writes the store's rules as data (`RelationTypeDoc`, `RuleDoc`).
Level 3 (models as Python code) is never served: no tool creates or modifies a Python module.

The level is a server argument, never a tool argument. Every check here reads only the
typed arguments of the call, so a call above the level fails before the store is read."""

from __future__ import annotations

READ, CONTENT, RULES = 0, 1, 2
LEVELS = {READ: "read", CONTENT: "content", RULES: "rules"}
#: Models whose documents are the store's rules: writing them changes what is valid.
RULE_MODELS = frozenset({"RelationTypeDoc", "RuleDoc"})


class LevelError(PermissionError):
    """A call above the write level the server was started with."""


def server_level(value: int) -> int:
    """The level to serve, checked: 0, 1 or 2 (3, models as code, is never served)."""
    if value not in LEVELS:
        raise ValueError(f"write level {value} is not served; choose one of {sorted(LEVELS)} ({', '.join(f'{k}={v}' for k, v in LEVELS.items())})")
    return value


def model_level(model: str) -> int:
    """The level a change to a document of `model` needs."""
    return RULES if model in RULE_MODELS else CONTENT


def require(allowed: int, needed: int, what: str) -> None:
    """Refuse `what` when it needs a level above `allowed`."""
    if needed > allowed:
        raise LevelError(f"{what} needs write level {needed} ({LEVELS[needed]}); this server was started with level {allowed} ({LEVELS[allowed]}). The level is set by the operator (`--level`), not by a tool argument.")
