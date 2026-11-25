"""The static extractor of specIR for Django REST Framework apps and their PostgreSQL schema.

`sldb.api.code.code_facts` gives the generic syntax (classes with `bases`, decorators with kwargs,
`calls`, assignments, calls of module level, SQL tables, columns and constraints); this package
interprets Django and DRF over those facts (`django_drf.py`, `sql.py`) and writes the domain types
of specIR, each with anchors on the facts it stands on (`write.py`). It reads no code itself.

    report = extract(project_root, store)    # an ExtractionReport
"""

from __future__ import annotations

from pathlib import Path

import sldb.api as api

from sldb.api.code import code_facts

from specir.extract.django_drf import interpret
from specir.extract.facts import Facts
from specir.extract.plan import Planned
from specir.extract.react_tsx import interpret_frontend
from specir.extract.routes import extract_routes
from specir.extract.write import ExtractionReport, write_plan
from specir.install import package_pythonpath

__all__ = ["ExtractionReport", "extract", "extract_frontend", "extract_routes"]


def extract(root: str | Path, store: str | Path | None = None, paths: list[str] | None = None) -> ExtractionReport:
    """Extract the backend and data nodes of the code under `root` into `store` (default
    `<root>/.sldb`), once per call and idempotent: the same code leaves the same store.

    Raises:
        ValueError: A fact's anchor does not match the fact; nothing is written.
    """
    root = Path(root).resolve()
    store_path = Path(store).resolve() if store is not None else root / ".sldb"
    facts = code_facts(root, paths)["facts"]
    plan = interpret(Facts(facts))
    nodes = [p for p in plan.nodes.values()]
    edges = [p for p in plan.edges.values()]
    return write_plan(store_path, root, package_pythonpath(), nodes, edges, list(dict.fromkeys(plan.not_derived)))


def extract_frontend(root: str | Path, store: str | Path | None = None, paths: list[str] | None = None) -> ExtractionReport:
    """Extract the interface nodes (InterfaceControlDoc, InterfaceActionDoc) of the TS, TSX, JS and JSX
    code under `root` into `store`, with `triggers` and `invokes` to the ApiOperationDoc already in the
    store (the backend extraction of `extract`). Idempotent; nothing is written if an anchor does not match.

    Raises:
        ValueError: A fact's anchor does not match the fact; nothing is written.
    """
    root = Path(root).resolve()
    store_path = Path(store).resolve() if store is not None else root / ".sldb"
    facts = code_facts(root, paths)["facts"]
    held = [d for d in api.load_runtime_documents(store_path, package_pythonpath()) if d.model_name == "ApiOperationDoc"]
    operations = [Planned("ApiOperationDoc", d.name, {"title": d.payload["title"], "method": d.payload.get("method"), "route": d.payload.get("route") or ""}, "derivado", "") for d in held if d.payload.get("method")]
    plan = interpret_frontend(Facts(facts), operations)
    return write_plan(store_path, root, package_pythonpath(), list(plan.nodes.values()), list(plan.edges.values()), list(dict.fromkeys(plan.not_derived)))
