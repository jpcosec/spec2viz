"""The API operations of a backend that is not DRF, from a table of routes declared in YAML.

    routes:
      - {method: POST, route: /api/save, title: optional}

Each entry becomes an ApiOperationDoc with origen `declarado` and no facts (nothing anchors it), so
`extract_frontend` can link the `invokes` of the frontend to it. The only writer of `declarado` in the extractor."""

from __future__ import annotations

from pathlib import Path

import sldb.api as api
import yaml

from specir.extract.plan import Planned, node_name
from specir.extract.write import ExtractionReport, write_plan
from specir.install import package_pythonpath

METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
RULE = "routes-yaml"


def read_routes(yaml_path: str | Path) -> list[Planned]:
    """The declared routes as Planned ApiOperationDoc. `ValueError` naming the entry that is not valid."""
    path = Path(yaml_path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(f"{path}: cannot read the routes table: {error}") from error
    entries = data.get("routes") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise ValueError(f"{path}: the table needs a 'routes' list")
    planned: dict[str, Planned] = {}
    for index, entry in enumerate(entries, 1):
        label = f"{path} routes[{index}] {entry!r}"
        if not isinstance(entry, dict):
            raise ValueError(f"{label}: an entry must be a mapping with method and route")
        method, route, title = entry.get("method"), entry.get("route"), entry.get("title")
        if not isinstance(method, str) or method not in METHODS:
            raise ValueError(f"{label}: method {method!r} is not one of {', '.join(METHODS)} (uppercase)")
        if not isinstance(route, str) or not route.startswith("/"):
            raise ValueError(f"{label}: route {route!r} must be a string starting with '/'")
        if title is not None and not isinstance(title, str):
            raise ValueError(f"{label}: title must be a string")
        title = title or f"{method} {route}"
        name = node_name("ApiOperationDoc", title)
        if name in planned:
            raise ValueError(f"{label}: duplicates the entry that already makes {name}")
        description = f"Declarado en la tabla de rutas {path.name}: {method} {route}."
        planned[name] = Planned("ApiOperationDoc", name, {"title": title, "method": method, "route": route, "description": description}, "declarado", RULE)
    return list(planned.values())


def extract_routes(yaml_path: str | Path, store: str | Path) -> ExtractionReport:
    """Write one ApiOperationDoc (origen `declarado`) per route of the YAML into `store`; idempotent.
    Declared operations that left the table are listed in `stale_declared`, never deleted.

    Raises:
        ValueError: An entry is not valid, or its name is already an ApiOperationDoc of another origen
            (DRF derives the same `METHOD route` names); nothing is written.
    """
    store_path = Path(store).resolve()
    nodes = read_routes(yaml_path)
    held = {d.name: d for d in api.load_runtime_documents(store_path, package_pythonpath()) if d.model_name == "ApiOperationDoc"}
    for node in nodes:
        old = held.get(node.name)
        if old is not None and old.payload.get("origen") != "declarado":
            raise ValueError(f"{node.export_id} ({node.fields['title']}): already exists with origen {old.payload.get('origen')!r}; nothing written")
    report = write_plan(store_path, store_path.parent, package_pythonpath(), nodes, [], [])
    wanted = {n.name for n in nodes}
    report.stale_declared = [f"ApiOperationDoc:{n}" for n, d in sorted(held.items()) if d.payload.get("origen") == "declarado" and n not in wanted]
    return report
