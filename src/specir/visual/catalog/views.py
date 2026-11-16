"""The boards of the HTML catalog from the resolved view, the same source graph_ui draws from
(migrated from spec2viz's `catalog_views`).

For each spec of a view, the catalog draws the mermaid of its resolved view
(`sldb.api.notations.resolve_view`) with the view's notation (`notation:` in vistas.yml, or the
builtin of its type), through IR12's `view_to_mermaid`. The resolved view comes:

1. from the project's store (the nearest `.sldb` above the vistas.yml) when the spec is synced
   there with the same content (sha256) and the same notation: exactly what graph_ui shows;
2. otherwise from a scratch store where sldb's `SpecSync` syncs the spec with that notation (the
   repository is not touched).

With a notation that only lives in a store where the spec is not synced, or a layout that is not a
graph (sequence, matrix), the view keeps its rendered source (`src`)."""

from __future__ import annotations

import hashlib
import html
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import sldb.api as api
import yaml
from sldb.api.notations import SpecSync, find_store, resolve_view

from specir.visual.lint_mermaid import assert_mermaid_ok
from specir.visual.notation_style import DEFAULT_NOTATIONS, builtin_notations
from specir.visual.renderers.view_mermaid import view_to_mermaid


def _warn(message: str) -> None:
    print(f"catalog: {message}", file=sys.stderr)


def _project_view(store: Path, spec_id: str, spec_path: Path, notation_ref: str | None) -> dict[str, Any] | None:
    sha = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    for doc in api.load_runtime_documents(store, None, include_linked=False):
        if str(doc.model_name) == "SpecDoc" and doc.name == spec_id:
            payload = dict(doc.payload or {})
            if payload.get("sha256") != sha or (notation_ref and payload.get("notation") != notation_ref):
                return None
            return resolve_view(store, spec_id)
    return None


def _scratch_view(spec_path: Path, notation: str | Path | None) -> dict[str, Any]:
    root = Path(tempfile.mkdtemp(prefix="specir-catalog-"))
    try:
        api.init_store(root)
        report = SpecSync(root / ".sldb", out_dir=root / "sldb" / "specs").sync(spec_path, notation=notation)
        return resolve_view(root / ".sldb", report.spec_id)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _notation_ref(chosen: str | Path) -> str | None:
    if isinstance(chosen, Path):
        name = (yaml.safe_load(Path(chosen).read_text(encoding="utf-8")) or {}).get("name")
        return f"NotationDoc:{name}" if name else None
    return f"NotationDoc:{chosen}"


def _view_of(spec_path: Path, notation: str | Path | None, store: Path | None) -> dict[str, Any] | None:
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    spec_id, diagram_type = str(spec.get("id") or ""), str(spec.get("type") or "")
    chosen = notation if notation is not None else DEFAULT_NOTATIONS.get(diagram_type)
    if chosen is None:
        return None
    view = None
    if store is not None:
        try:
            view = _project_view(Path(store), spec_id, spec_path, _notation_ref(chosen))
        except Exception as exc:  # a broken store does not stop the catalog: the view is resolved apart
            _warn(f"{spec_id}: project store not usable ({type(exc).__name__}: {exc})")
    if view is None:
        if not isinstance(chosen, Path) and str(chosen) not in builtin_notations():
            _warn(f"{spec_id}: notation {chosen!r} lives only in the store and the spec is not synced there; using the view's src")
            return None
        view = _scratch_view(spec_path, chosen)
    return view if (view.get("layout") or {}).get("kind", "graph") == "graph" else None


def resolved_views(spec_paths: list[Path], notation: str | Path | None, config_dir: Path) -> list[dict[str, Any]] | None:
    """The resolved views of a catalog view's specs, or None when one cannot be resolved (a layout
    that is not a graph, a store-only notation the spec is not synced with)."""
    store = find_store(config_dir)
    views = []
    for spec_path in spec_paths:
        view = _view_of(spec_path, notation, store)
        if view is None:
            return None
        views.append(view)
    return views


def resolved_board(spec_paths: list[Path], notation: str | Path | None, config_dir: Path) -> str | None:
    """The HTML of a view's mermaid boards, from its resolved views; None when it does not apply."""
    views = resolved_views(spec_paths, notation, config_dir)
    if not views:
        return None
    boards = []
    for view in views:
        source = view_to_mermaid(view, theme="dark")
        assert_mermaid_ok(source, source=view["spec"], check_html=False)
        indented = "\n".join("      " + line for line in html.escape(source).splitlines())
        boards.append(f'  <div class="board" data-resolved-from="{html.escape(view["spec"])}" data-notation="{html.escape(view["notation"])}">\n'
                      f'    <pre class="mermaid">\n{indented}\n    </pre>\n  </div>')
    return "\n".join(boards)


__all__ = ["resolved_board", "resolved_views"]
