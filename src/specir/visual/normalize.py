"""Structural normalization of an intermediate representation, to compare two of them.

`normalize(ir)` turns an IR (dataclasses of `specir.visual.ir` or of spec2viz, pydantic models such
as `EnforcementArtifact`, dicts and lists) into plain data: every object becomes a dict with its
type name under `"__type__"` and its fields. Collections whose order means nothing (nodes, edges,
states, transitions, artifacts, connections, packages, relations, spans, `contains`) are sorted
deterministically; the order is kept where it means something (activity steps, sequence
participants and messages, class members and parameters, matrix stages and rows, enforcement
facts). Only provenance metadata is left out (`PROVENANCE`: origin, timestamps, paths, hashes).
Two IRs are structurally equivalent when their normalized forms are equal."""

from __future__ import annotations

import dataclasses
import json
from typing import Any

#: Keys of provenance metadata, left out at any depth.
PROVENANCE = frozenset({
    "origen", "origin", "provenance", "source_path", "spec_path", "path", "generated_at",
    "created_at", "updated_at", "timestamp", "sha256",
})

#: Fields whose order means nothing, by IR type name. Anything else keeps its order.
UNORDERED: dict[str, frozenset[str]] = {
    "ComponentIR": frozenset({"nodes", "edges"}),
    "ComponentNode": frozenset({"contains"}),
    "StateIR": frozenset({"states", "transitions"}),
    "StateNode": frozenset({"contains"}),
    "DeploymentIR": frozenset({"nodes", "artifacts", "connections"}),
    "DeploymentNode": frozenset({"contains"}),
    "ClassIR": frozenset({"classes", "relations", "packages"}),
    "ClassPackageIR": frozenset({"contains"}),
    "MatrixIR": frozenset({"spans"}),
}


def type_name(value: Any) -> str:
    return type(value).__name__


def _fields(value: Any) -> dict[str, Any] | None:
    """The fields of a dataclass or pydantic object, else None."""
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {f.name: getattr(value, f.name) for f in dataclasses.fields(value)}
    if hasattr(value, "model_dump") and hasattr(type(value), "model_fields"):
        return {name: getattr(value, name) for name in type(value).model_fields}
    return None


def _key(item: Any) -> str:
    """Deterministic sort key: the `id` when there is one, then the whole normalized item."""
    ident = item.get("id") if isinstance(item, dict) else None
    return json.dumps([str(ident) if ident is not None else "", item], sort_keys=True, default=str)


def normalize(value: Any, unordered: bool = False) -> Any:
    """Plain, comparable data of `value` (see the module docstring)."""
    fields = _fields(value)
    if fields is not None:
        name = type_name(value)
        loose = UNORDERED.get(name, frozenset())
        out = {"__type__": name}
        for field, item in fields.items():
            if field not in PROVENANCE:
                out[field] = normalize(item, field in loose)
        return out
    if isinstance(value, dict):
        return {str(k): normalize(v) for k, v in sorted(value.items(), key=lambda kv: str(kv[0])) if k not in PROVENANCE}
    if isinstance(value, (list, tuple)):
        items = [normalize(v) for v in value]
        return sorted(items, key=_key) if unordered else items
    if hasattr(value, "value") and type(value).__module__ != "builtins" and isinstance(getattr(value, "value"), (str, int)):
        return value.value  # enums
    return value


def equivalent(left: Any, right: Any) -> bool:
    """True when both IRs are structurally equivalent."""
    return normalize(left) == normalize(right)


def differences(left: Any, right: Any, path: str = "$") -> list[str]:
    """Where two normalized forms differ (empty when equivalent), for failure messages."""
    left, right = (normalize(left), normalize(right)) if path == "$" else (left, right)
    if isinstance(left, dict) and isinstance(right, dict):
        found = []
        for key in sorted(set(left) | set(right)):
            if key not in left or key not in right:
                found.append(f"{path}.{key}: only in {'right' if key not in left else 'left'}")
            else:
                found += differences(left[key], right[key], f"{path}.{key}")
        return found
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            return [f"{path}: {len(left)} items != {len(right)} items"]
        return [d for i, (a, b) in enumerate(zip(left, right)) for d in differences(a, b, f"{path}[{i}]")]
    return [] if left == right else [f"{path}: {left!r} != {right!r}"]


__all__ = ["PROVENANCE", "UNORDERED", "differences", "equivalent", "normalize"]
