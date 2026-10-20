"""Las vistas del catalogo HTML desde la misma fuente que graph_ui: `notation_view`.

Para cada spec de una vista, `catalog build` dibuja el mermaid que sale de su vista resuelta
(`resolve_view`), con la notacion de la vista (`notation:` en vistas.yml, o la builtin del tipo):
glifos, keyword, forma, compartimentos, estilo con su precedencia y links. La vista resuelta sale:

1. del store del proyecto (el `.sldb` mas cercano al vistas.yml), si el spec ya esta sincronizado
   ahi con el mismo contenido (sha256) y la misma notacion: es exactamente lo que ve graph_ui;
2. si no, de un store temporal donde se sincroniza el spec con esa notacion (no toca el repo).

Sin sldb instalado, con una notacion que solo existe en el store y no esta sincronizada, o con un
layout que no es un grafo (secuencia, matriz), la vista usa su fuente renderizada (`src`) como antes.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


def _warn(message: str) -> None:
    print(f"catalog: {message}", file=sys.stderr)


def _project_view(store: Path, spec_id: str, spec_path: Path, notation_ref: str | None) -> dict[str, Any] | None:
    import sldb.api as api
    from spec2viz.notation_view import resolve_view

    sha = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    for doc in api.load_runtime_documents(store, None, include_linked=False):
        if str(doc.model_name) == "SpecDoc" and doc.name == spec_id:
            payload = dict(doc.payload or {})
            if payload.get("sha256") != sha or (notation_ref and payload.get("notation") != notation_ref):
                return None
            return resolve_view(store, spec_id)
    return None


def _scratch_view(spec_path: Path, notation: str | Path | None) -> dict[str, Any]:
    import sldb.api as api
    from spec2viz.notation_view import resolve_view
    from spec2viz.sldb_sync import SpecSync

    root = Path(tempfile.mkdtemp(prefix="spec2viz-catalog-"))
    try:
        api.init_store(root)
        report = SpecSync(root / ".sldb", out_dir=root / "sldb" / "specs").sync(spec_path, notation=notation)
        return resolve_view(root / ".sldb", report.spec_id)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def resolved_views(spec_paths: list[Path], notation: str | Path | None, config_dir: Path) -> list[dict[str, Any]] | None:
    """Las vistas resueltas de los specs de una vista del catalogo, o None si no se pueden
    resolver (sin sldb, layout que no es un grafo, notacion solo de store sin sincronizar)."""
    try:
        import sldb.api  # noqa: F401
    except Exception:
        return None
    import yaml

    from spec2viz.notation import DEFAULT_NOTATIONS, builtin_notations
    from spec2viz.sldb_sync import find_store

    store = find_store(config_dir)
    views: list[dict[str, Any]] = []
    for spec_path in spec_paths:
        spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
        spec_id, diagram_type = str(spec.get("id") or ""), str(spec.get("type") or "")
        chosen = notation if notation is not None else DEFAULT_NOTATIONS.get(diagram_type)
        if chosen is None:
            return None
        if isinstance(chosen, Path):
            notation_ref = None  # su nombre sale del YAML; el store del proyecto se reconoce por sha y nombre abajo
            name = (yaml.safe_load(Path(chosen).read_text(encoding="utf-8")) or {}).get("name")
            notation_ref = f"NotationDoc:{name}" if name else None
        else:
            notation_ref = f"NotationDoc:{chosen}"
        view = None
        if store is not None:
            try:
                view = _project_view(Path(store), spec_id, spec_path, notation_ref)
            except Exception as exc:  # un store roto no frena el catalogo: se resuelve aparte
                _warn(f"{spec_id}: project store not usable ({type(exc).__name__}: {exc})")
        if view is None:
            if not isinstance(chosen, Path) and str(chosen) not in builtin_notations():
                _warn(f"{spec_id}: notation {chosen!r} lives only in the store and the spec is not synced there; using the view's src")
                return None
            view = _scratch_view(spec_path, chosen)
        if (view.get("layout") or {}).get("kind", "graph") != "graph":
            return None
        views.append(view)
    return views


def resolved_board(spec_paths: list[Path], notation: str | Path | None, config_dir: Path) -> str | None:
    """El HTML de los tableros mermaid de una vista, desde sus vistas resueltas; None si no aplica."""
    import html

    from spec2viz.linters.mermaid import assert_mermaid_ok
    from spec2viz.renderers.view_mermaid import view_to_mermaid

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


__all__ = ["resolved_views", "resolved_board"]
