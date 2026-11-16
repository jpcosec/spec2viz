"""The atoms of the HTML catalog: the adapter from a catalog view to sldb's `SpecView` and what the
page embeds (migrated from spec2viz's `deskops`: the `CatalogItem` adapter, the store discovery of
`SldbAtomResolver`, `split_shared_atoms` and the atom part of `render_deskops`).

The matching itself is sldb's (`sldb.api.matching`, D4), called directly: the atoms of each view's
store or of an atoms folder (`build_atoms_by_view`), the explicit `atoms:` and `refs:` of the
elements (`build_explicit_atoms`, `build_explicit_refs`), the sldb edges of the atoms
(`attach_atom_edges`) and the coverage per view (`build_coverage_by_view`). An unknown atom id is a
`matching/unknown-atom` finding, an error with `strict` (`UnknownAtomError`). specIR only adapts a
view and lays the result in the page; the fuzzy matching in the browser is the template's
(`findAtomData`, `normKey`, which sldb's `label_key` matches)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sldb.api.matching import (
    SpecView,
    StoreReader,
    attach_atom_edges,
    build_coverage_by_view,
    build_explicit_atoms,
    build_explicit_refs,
    filter_atoms_payload,
    raw_atoms_by_view,
)
from sldb.api.notations import find_store

from specir.visual.catalog.loader import CatalogItem, find_monorepo_root, resolve_spec_path
from specir.visual.catalog.sections import resolve_item_path


def item_specs(item: CatalogItem) -> list[dict]:
    """The YAML specs of a view that could be read, as dicts."""
    specs = []
    for spec_ref in item.specs:
        spec_path = resolve_spec_path(spec_ref, Path(item.source_base_dir))
        if spec_path is None:
            continue
        try:
            spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if isinstance(spec, dict):
            specs.append(spec)
    return specs


def _src_path(item: CatalogItem) -> Path | None:
    if not item.src:
        return None
    return resolve_item_path(item.src.split("#", 1)[0], Path(item.source_base_dir), "src").resolve()


def _boundary(item: CatalogItem, src_path: Path | None) -> Path | None:
    """The project's folder (`<monorepo root>/<project>`) a view's store must live in, if any."""
    if not item.project:
        return None
    probe = src_path.parent if src_path is not None else Path(item.source_base_dir)
    root = find_monorepo_root(probe.resolve())
    boundary = (root / item.project).resolve() if root is not None else None
    return boundary if boundary is not None and boundary.exists() else None


def view_store(item: CatalogItem) -> Path | None:
    """The `.sldb` of a view: the nearest one sldb recognizes above its `src`, then above its
    config, inside its project's folder when it has one."""
    src_path = _src_path(item)
    boundary = _boundary(item, src_path)
    for start in [*([src_path.parent] if src_path is not None else []), Path(item.source_base_dir)]:
        store = find_store(start)
        if store is not None and (boundary is None or store.parent.is_relative_to(boundary)):
            return store
    return None


def spec_view(item: CatalogItem) -> SpecView:
    """A catalog view as sldb's `SpecView`: its specs loaded and its store found."""
    return SpecView(
        key=item.anchor_id, id=item.id, specs=item_specs(item), source=item.src or "", base_dir=item.source_base_dir,
        store=view_store(item), title=item.title, diagram_type=item.diagram_type, scope=item.project,
    )


def split_shared_atoms(atoms_by_view: dict[str, dict[str, dict]]) -> tuple[dict[str, dict], dict[str, dict[str, dict]]]:
    """Moves the most repeated (non empty) payload to a common `ATOMS_DB`, emitted once: the
    template falls back to `ATOMS_DB` when a view is not in `ATOMS_BY_VIEW`."""
    counts: dict[str, int] = {}
    for payload in (p for p in atoms_by_view.values() if p):
        key = json.dumps(payload, sort_keys=True)
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return {}, atoms_by_view
    shared_key, shared_count = max(counts.items(), key=lambda kv: kv[1])
    if shared_count < 2:
        return {}, atoms_by_view
    rest = {view: payload for view, payload in atoms_by_view.items() if not (payload and json.dumps(payload, sort_keys=True) == shared_key)}
    return json.loads(shared_key), rest


@dataclass
class CatalogAtoms:
    """What the page embeds about atoms, as the template reads it (`window.*`)."""

    shared: dict[str, dict] = field(default_factory=dict)
    by_view: dict[str, dict] = field(default_factory=dict)
    explicit: dict[str, dict] = field(default_factory=dict)
    linked: dict[str, dict] = field(default_factory=dict)
    refs: dict[str, dict] = field(default_factory=dict)
    coverage: dict[str, dict] = field(default_factory=dict)
    warnings: list[dict] = field(default_factory=list)
    coverage_warnings: list[dict] = field(default_factory=list)


def _report(findings: list[Any]) -> list[dict]:
    for finding in findings:
        print(f"[specir][atoms] {finding.subject}: {finding.what}", file=sys.stderr)
    return [finding.as_dict() for finding in findings]


def catalog_atoms(items: list[CatalogItem], atoms_dir: Path | None = None, atoms_tags: list[str] | None = None, strict: bool = False) -> CatalogAtoms:
    """The atoms of the catalog's views through `sldb.api.matching`; with `strict` an unknown atom
    or ref raises sldb's `UnknownAtomError`."""
    views, reader = [spec_view(item) for item in items], StoreReader()
    raw, warnings = raw_atoms_by_view(views, atoms_dir, reader)
    explicit, complete, explicit_warnings, linked = build_explicit_atoms(views, raw, strict=strict)
    refs, ref_warnings = build_explicit_refs(views, reader, strict=strict)
    attach_atom_edges(views, explicit, linked, reader, raw)
    by_view = {view: filter_atoms_payload(payload, atoms_tags) if atoms_tags else payload for view, payload in raw.items()}
    by_view.update({view: {} for view in complete})  # every node explicit: no fuzzy matching, nothing else embedded
    shared, by_view = split_shared_atoms(by_view)
    coverage, coverage_warnings = build_coverage_by_view(views)
    return CatalogAtoms(shared, by_view, explicit, linked, refs, coverage, _report([*warnings, *explicit_warnings, *ref_warnings]),
                        [finding.as_dict() for finding in coverage_warnings])


def atoms_script(atoms: CatalogAtoms, metadata: str) -> str:
    """The `<script>` that hands the atoms to the template, right before `</body>`."""
    return (
        "\n<script>"
        f"window.ATOMS_DB = {json.dumps(atoms.shared)}; "
        f"window.ATOMS_BY_VIEW = {json.dumps(atoms.by_view)}; "
        f"window.ATOMS_EXPLICIT = {json.dumps(atoms.explicit)}; "
        f"window.ATOMS_LINKED = {json.dumps(atoms.linked)}; "
        f"window.REFS_EXPLICIT = {json.dumps(atoms.refs)}; "
        f"window.COVERAGE_BY_VIEW = {json.dumps(atoms.coverage)}; "
        f"window.SPEC2VIZ_ATOM_WARNINGS = {json.dumps(atoms.warnings)}; "
        f"window.SPEC2VIZ_COVERAGE_WARNINGS = {json.dumps(atoms.coverage_warnings)}; "
        f"window.SPEC2VIZ_CATALOG = {metadata};"
        "</script>\n</body>"
    )


__all__ = ["CatalogAtoms", "atoms_script", "catalog_atoms", "item_specs", "spec_view", "split_shared_atoms", "view_store"]
