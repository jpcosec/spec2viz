from __future__ import annotations

from pathlib import Path
from statistics import mean

import json
import re
import sys
from dataclasses import dataclass, field

import yaml

from spec2viz.orchestrator import (
    CatalogItem,
    load_catalog,
    render_catalog_metadata,
    render_filter_bar,
    render_nav,
    render_sections,
)


@dataclass
class AtomBuildWarning:
    scope: str
    message: str


@dataclass
class CoverageBuildWarning:
    scope: str
    message: str


@dataclass
class SldbAtomResolver:
    pythonpath: str | None = None
    warnings: list[AtomBuildWarning] = field(default_factory=list)
    _store_payload_cache: dict[str, dict[str, dict]] = field(default_factory=dict)
    _view_store_cache: dict[str, Path | None] = field(default_factory=dict)

    def build_atoms_by_view(self, items: list[CatalogItem]) -> dict[str, dict[str, dict]]:
        atoms_by_view: dict[str, dict[str, dict]] = {}
        for item in items:
            view_key = self._view_key(item)
            store_path = self._discover_store_for_item(item)
            if store_path is None:
                atoms_by_view[view_key] = {}
                continue
            atoms_by_view[view_key] = self._load_store_payload(store_path)
        return atoms_by_view

    def _view_key(self, item: CatalogItem) -> str:
        return item.anchor_id

    def _discover_store_for_item(self, item: CatalogItem) -> Path | None:
        view_key = self._view_key(item)
        if view_key in self._view_store_cache:
            return self._view_store_cache[view_key]

        try:
            from sldb.store.layout import store_exists
            from sldb.store.resolver import find_local_store
        except Exception as exc:  # pragma: no cover - exercised through fallback path
            self._warn("sldb", f"SLDB unavailable while resolving stores: {exc}")
            self._view_store_cache[view_key] = None
            return None

        candidates: list[Path] = []
        src_path = self._resolve_item_src_path(item)
        if src_path is not None:
            candidates.append(src_path.parent)
        candidates.append(Path(item.source_base_dir))

        boundary = self._project_boundary(item, src_path)
        store_path = None
        for candidate in candidates:
            if boundary is not None:
                store_path = self._find_local_store_with_boundary(candidate, boundary, store_exists)
            else:
                store_path = find_local_store(candidate)
            if store_path is not None:
                break

        if store_path is not None and boundary is not None and not self._is_relative_to(store_path.parent, boundary):
            store_path = None

        self._view_store_cache[view_key] = store_path
        return store_path

    def _resolve_item_src_path(self, item: CatalogItem) -> Path | None:
        if not item.src:
            return None
        src_value = item.src.split("#", 1)[0]
        return (Path(item.source_base_dir) / src_value).resolve()

    def _project_boundary(self, item: CatalogItem, src_path: Path | None) -> Path | None:
        if not item.project:
            return None
        probe = src_path.parent if src_path is not None else Path(item.source_base_dir)
        repo_root = self._find_repo_root(probe.resolve())
        if repo_root is None:
            return None
        boundary = (repo_root / item.project).resolve()
        return boundary if boundary.exists() else None

    def _find_repo_root(self, start: Path) -> Path | None:
        current = start.resolve()
        for directory in [current, *current.parents]:
            if (directory / "README.md").exists() and ((directory / "projects").exists() or (directory / "software").exists()):
                return directory
        return None

    def _find_local_store_with_boundary(self, start: Path, boundary: Path, store_exists) -> Path | None:
        current = start.resolve()
        boundary = boundary.resolve()
        for directory in [current, *current.parents]:
            if not self._is_relative_to(directory, boundary):
                break
            candidate = directory / ".sldb"
            if store_exists(candidate):
                return candidate.resolve()
            if directory == boundary:
                break
        return None

    def _is_relative_to(self, path: Path, other: Path) -> bool:
        try:
            path.resolve().relative_to(other.resolve())
            return True
        except ValueError:
            return False

    def _load_store_payload(self, store_path: Path) -> dict[str, dict]:
        cache_key = str(store_path.resolve())
        if cache_key in self._store_payload_cache:
            return self._store_payload_cache[cache_key]

        try:
            payload = self._load_store_payload_uncached(store_path.resolve())
        except Exception as exc:  # pragma: no cover - defensive guard
            self._warn(str(store_path), f"Failed to load atoms through SLDB: {exc}")
            payload = {}

        self._store_payload_cache[cache_key] = payload
        return payload

    def _load_store_payload_uncached(self, store_path: Path) -> dict[str, dict]:
        try:
            from sldb.cli.model_utils import resolve_model_ref
            from sldb.runtime.validation import extract_model_data
            from sldb.store.io import load_documents_index, load_models_index, load_store_index
            from sldb.store.layout import project_root, store_exists
        except Exception as exc:  # pragma: no cover - exercised through fallback path
            raise RuntimeError(f"SLDB import failed: {exc}") from exc

        payload: dict[str, dict] = {}
        visited: set[str] = set()

        def visit(current_store: Path):
            current_key = str(current_store.resolve())
            if current_key in visited:
                return
            visited.add(current_key)

            root = project_root(current_store)
            store_index = load_store_index(current_store)
            atom_entry = next((entry for entry in store_index.models if entry.name == "AtomDoc"), None)
            if atom_entry is not None:
                model_type = resolve_model_ref(atom_entry.model_ref, self.pythonpath)
                model_index = load_models_index(root / atom_entry.models_index)
                documents_index = load_documents_index(root / model_index.documents_index)
                for document in documents_index.documents:
                    doc_path = root / document.path
                    if not doc_path.exists():
                        self._warn(current_key, f"Missing tracked atom doc: {doc_path}")
                        continue
                    try:
                        atom = extract_model_data(model_type, doc_path.read_text(encoding="utf-8"))
                    except Exception as exc:
                        self._warn(current_key, f"Skipped invalid atom doc {doc_path}: {exc}")
                        continue
                    self._merge_atom(payload, atom, doc_path, current_store)

            for linked in store_index.stores:
                linked_store = Path(linked.path)
                linked_store = linked_store if linked_store.is_absolute() else (root / linked_store)
                linked_store = linked_store.resolve()
                if not store_exists(linked_store):
                    self._warn(current_key, f"Linked store missing: {linked.name} -> {linked_store}")
                    continue
                visit(linked_store)

        visit(store_path)
        return payload

    def _merge_atom(self, payload: dict[str, dict], atom: dict, doc_path: Path, store_path: Path) -> None:
        title = str(atom.get("title") or "").strip()
        question = str(atom.get("five_wh_one_plus") or "").strip().lower()
        body = str(atom.get("answer") or "").strip()
        if not title or not question or not body:
            return

        title_norm = _normalize_key(title)
        if not title_norm:
            return

        tags = atom.get("tags") or []
        entry = payload.setdefault(
            title_norm,
            {"title": title, "atoms": {}, "aliases": _alias_candidates(title, tags)},
        )
        entry["aliases"] = _alias_candidates(title, tags)
        entry["atoms"][question] = {
            "id": atom.get("id") or doc_path.stem,
            "body": body,
            "path": str(doc_path),
            "store": str(store_path),
            "tags": tags,
            "provenance": atom.get("provenance"),
        }

    def _warn(self, scope: str, message: str) -> None:
        warning = AtomBuildWarning(scope=scope, message=message)
        self.warnings.append(warning)
        print(f"[spec2viz][atoms] {scope}: {message}", file=sys.stderr)


def _normalize_key(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^\w\s]+", " ", value)
    return re.sub(r"\s+", " ", value)


def _alias_candidates(title: str, tags: list[str]) -> list[str]:
    aliases: list[str] = []
    normalized_title = _normalize_key(title)
    if normalized_title:
        aliases.append(normalized_title)
        words = [word for word in normalized_title.split() if len(word) >= 3]
        aliases.extend(words)
        aliases.extend([f"{a} {b}" for a, b in zip(words, words[1:])])

    for tag in tags or []:
        if ":" not in tag:
            continue
        _namespace, value = tag.split(":", 1)
        normalized_value = _normalize_key(value.replace("-", " ").replace("_", " "))
        if normalized_value:
            aliases.append(normalized_value)
            aliases.extend([word for word in normalized_value.split() if len(word) >= 3])

    seen: set[str] = set()
    result: list[str] = []
    for alias in aliases:
        if alias and alias not in seen:
            seen.add(alias)
            result.append(alias)
    return result


def parse_atoms(atoms_dir: Path) -> str:
    if not atoms_dir or not atoms_dir.exists():
        return "{}"

    atoms_db = {}
    for md_file in atoms_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                body = parts[2].strip()
                title = fm.get("title")
                question = fm.get("five_wh_one_plus")
                if title and question:
                    title_norm = _normalize_key(title)
                    tags = fm.get("tags") or []
                    if title_norm not in atoms_db:
                        atoms_db[title_norm] = {
                            "title": title.strip(),
                            "aliases": _alias_candidates(title, tags),
                            "atoms": {},
                        }
                    atoms_db[title_norm]["atoms"][question.strip().lower()] = {
                        "id": fm.get("id", md_file.stem),
                        "body": body,
                    }
            except Exception as exc:
                print(f"Failed to parse atom {md_file}: {exc}")
    return json.dumps(atoms_db)


def build_atoms_by_view(items: list[CatalogItem], atoms_dir: Path | None = None) -> tuple[dict[str, dict[str, dict]], list[AtomBuildWarning]]:
    resolver = SldbAtomResolver()
    atoms_by_view = resolver.build_atoms_by_view(items)

    if atoms_dir:
        fallback = json.loads(parse_atoms(atoms_dir))
        for item in items:
            view_key = item.anchor_id
            if atoms_by_view.get(view_key):
                continue
            atoms_by_view[view_key] = fallback

    return atoms_by_view, resolver.warnings


def build_coverage_by_view(
    items: list[CatalogItem], kgdb_snapshot_path: Path | None = None
) -> tuple[dict[str, dict], list[CoverageBuildWarning]]:
    warnings: list[CoverageBuildWarning] = []
    snapshot_path = kgdb_snapshot_path or _discover_snapshot_path(items)
    if snapshot_path is None or not snapshot_path.exists():
        warnings.append(CoverageBuildWarning(scope="kgdb", message="KGDB snapshot not found; coverage projection is empty."))
        return {item.anchor_id: _empty_coverage_payload(item) for item in items}, warnings

    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except Exception as exc:
        warnings.append(CoverageBuildWarning(scope=str(snapshot_path), message=f"Failed to read KGDB snapshot: {exc}"))
        return {item.anchor_id: _empty_coverage_payload(item) for item in items}, warnings

    nodes = {node.get("identity", {}).get("node_id"): node for node in snapshot.get("nodes", []) if node.get("identity", {}).get("node_id")}
    views_by_source_ref = {}
    for node_id, node in nodes.items():
        if not node_id or node.get("identity", {}).get("node_type") != "view":
            continue
        source_ref = str(node.get("semantics", {}).get("source_ref") or "").strip()
        if source_ref:
            views_by_source_ref[source_ref] = node

    payload: dict[str, dict] = {}
    project_root = _project_root_from_snapshot(snapshot_path)
    for item in items:
        view_key = item.anchor_id
        source_ref = _item_source_ref(item, project_root)
        view_node = views_by_source_ref.get(source_ref)
        if view_node is None:
            payload[view_key] = _empty_coverage_payload(item)
            continue
        payload[view_key] = _project_view_payload(item, view_node, nodes)

    return payload, warnings


def _discover_snapshot_path(items: list[CatalogItem]) -> Path | None:
    candidates: list[Path] = []
    for item in items:
        base = Path(item.source_base_dir).resolve()
        candidates.extend([base, *base.parents])
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        snapshot = candidate / ".sldb" / "runtime" / "knowledge_graph.kg.json"
        if snapshot.exists():
            return snapshot
    return None


def _project_root_from_snapshot(snapshot_path: Path) -> Path:
    return snapshot_path.resolve().parents[2]


def _item_source_ref(item: CatalogItem, project_root: Path) -> str:
    if not item.src:
        return ""
    src_value = item.src
    src_path_text, fragment = src_value.split("#", 1) if "#" in src_value else (src_value, None)
    resolved = (Path(item.source_base_dir) / src_path_text).resolve()
    try:
        relative = resolved.relative_to(project_root).as_posix()
    except ValueError:
        relative = resolved.as_posix()
    return f"{relative}#{fragment}" if fragment else relative


def _empty_coverage_payload(item: CatalogItem) -> dict:
    return {
        "view_id": item.anchor_id,
        "view_node_id": None,
        "diagram_type": item.diagram_type or "",
        "title": item.title,
        "source_ref": "",
        "scope": item.project or "",
        "summary": {
            "total_elements": 0,
            "elements_fully_covered": 0,
            "avg_coverage_ratio": 0.0,
            "expected_facet_count": 0,
            "covered_facet_count": 0,
            "missing_facet_count": 0,
        },
        "elements": [],
    }


def _project_view_payload(item: CatalogItem, view_node: dict, nodes: dict[str, dict]) -> dict:
    semantics = view_node.get("semantics", {})
    elements: list[dict] = []
    for edge in sorted(view_node.get("edges", []), key=lambda edge: edge.get("target_id", "")):
        if edge.get("relation_type") != "contains":
            continue
        element_node = nodes.get(edge.get("target_id"))
        if not element_node:
            continue
        element_payload = _project_element_payload(element_node, nodes)
        elements.append(element_payload)

    fully_covered = sum(1 for element in elements if element["expected_facets"] and not element["missing_facets"])
    coverage_ratios = [element["coverage_ratio"] for element in elements]
    expected_count = sum(len(element["expected_facets"]) for element in elements)
    covered_count = sum(len({entry["facet"] for entry in element["covered_facets"]}) for element in elements)
    missing_count = sum(len(element["missing_facets"]) for element in elements)
    return {
        "view_id": item.anchor_id,
        "view_node_id": view_node.get("identity", {}).get("node_id"),
        "diagram_type": semantics.get("diagram_type") or item.diagram_type or "",
        "title": semantics.get("title") or item.title,
        "source_ref": semantics.get("source_ref") or item.src or "",
        "scope": semantics.get("scope") or item.project or "",
        "summary": {
            "total_elements": len(elements),
            "elements_fully_covered": fully_covered,
            "avg_coverage_ratio": round(mean(coverage_ratios), 4) if coverage_ratios else 0.0,
            "expected_facet_count": expected_count,
            "covered_facet_count": covered_count,
            "missing_facet_count": missing_count,
        },
        "elements": sorted(elements, key=lambda element: element["element_id"]),
    }


def _project_element_payload(element_node: dict, nodes: dict[str, dict]) -> dict:
    semantics = element_node.get("semantics", {})
    expected_facets: list[dict] = []
    covered_facets: list[dict] = []
    for edge in element_node.get("edges", []):
        relation_type = edge.get("relation_type")
        metadata = edge.get("metadata", {})
        if relation_type == "expects_facet":
            facet_node = nodes.get(edge.get("target_id"))
            facet_name = metadata.get("facet") or facet_node.get("semantics", {}).get("facet") if facet_node else None
            if not facet_name:
                continue
            expected_facets.append(
                {
                    "facet": facet_name,
                    "facet_node_id": edge.get("target_id"),
                    "source_field": metadata.get("source_field") or _source_field_for(semantics, facet_name),
                }
            )
        if relation_type == "covers_facet":
            facet_name = metadata.get("facet")
            atom_id = metadata.get("atom_id")
            if not facet_name or not atom_id:
                continue
            covered_facets.append(
                {
                    "facet": facet_name,
                    "facet_node_id": f"facet:{facet_name}",
                    "atom_id": atom_id,
                    "atom_node_id": edge.get("target_id"),
                    "score": metadata.get("score", 0.0),
                    "match_basis": metadata.get("match_basis"),
                    "evidence": metadata.get("evidence"),
                }
            )

    expected_facets = sorted(expected_facets, key=lambda item: item["facet"])
    covered_facets = sorted(covered_facets, key=lambda item: (item["facet"], item["atom_id"]))
    covered_names = {item["facet"] for item in covered_facets}
    missing_facets = [item for item in expected_facets if item["facet"] not in covered_names]
    ratio = round(len({item["facet"] for item in covered_facets if item["facet"] in {entry['facet'] for entry in expected_facets}}) / len(expected_facets), 4) if expected_facets else 0.0
    return {
        "element_id": semantics.get("element_id") or "",
        "element_node_id": element_node.get("identity", {}).get("node_id"),
        "element_kind": semantics.get("element_kind") or "",
        "label": semantics.get("label"),
        "source": semantics.get("source"),
        "target": semantics.get("target"),
        "expected_facets": expected_facets,
        "covered_facets": covered_facets,
        "missing_facets": missing_facets,
        "coverage_ratio": ratio,
    }


def _source_field_for(semantics: dict, facet: str) -> str:
    diagram_type = semantics.get("diagram_type")
    element_kind = semantics.get("element_kind")
    mapping = {
        ("component", "node", "what"): "label",
        ("component", "edge", "how"): "semantics.relation",
        ("component", "edge", "why"): "semantics.relation",
        ("state", "state", "what"): "label",
        ("state", "transition", "how"): "semantics.action",
        ("state", "transition", "when"): "semantics.on",
        ("state", "transition", "why"): "semantics.guard",
    }
    return mapping.get((diagram_type, element_kind, facet), "label")


def render_deskops(config_path: Path, base_dir: Path | None = None, atoms_dir: Path | None = None) -> str:
    catalog = load_catalog(config_path)
    if base_dir is None:
        base_dir = config_path.parent

    tpl_path = base_dir / catalog.template if catalog.template else None
    if tpl_path and tpl_path.exists():
        print(f"spec2viz: using local catalog template override: {tpl_path}", file=sys.stderr)
        tpl = tpl_path.read_text(encoding="utf-8")
    else:
        builtin_tpl = Path(__file__).resolve().parent / "templates" / "default.html"
        if builtin_tpl.exists():
            tpl = builtin_tpl.read_text(encoding="utf-8")
        elif tpl_path:
            tpl = tpl_path.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError("No catalog template configured and built-in template missing.")

    nav = render_nav(catalog.items)
    filters = render_filter_bar(catalog.items)
    sections = render_sections(catalog.items, base_dir)

    html = tpl.replace("{{NAV}}", nav)
    html = html.replace("{{FILTERS}}", filters)
    html = html.replace("{{SECTIONS}}", sections)
    html = html.replace("{{PROJECT_NAME}}", catalog.project_name)
    html = html.replace("{{BRAND_NAME}}", catalog.brand_name)
    html = html.replace("{{BRAND_SUBTITLE}}", catalog.brand_subtitle)
    html = html.replace("{{CATALOG_TITLE}}", catalog.title)
    html = html.replace("{{CATALOG_METADATA}}", render_catalog_metadata(catalog, catalog.items))

    if "{{FILTERS}}" not in tpl and "{{SECTIONS}}" in tpl:
        html = html.replace(sections, filters + sections, 1)

    atoms_by_view, warnings = build_atoms_by_view(catalog.items, atoms_dir=atoms_dir)
    coverage_by_view, coverage_warnings = build_coverage_by_view(catalog.items)
    atoms_by_view_json = json.dumps(atoms_by_view)
    coverage_by_view_json = json.dumps(coverage_by_view)
    warnings_json = json.dumps([warning.__dict__ for warning in warnings])
    coverage_warnings_json = json.dumps([warning.__dict__ for warning in coverage_warnings])
    catalog_metadata = render_catalog_metadata(catalog, catalog.items)

    if "{{ATOMS_DB}}" in html:
        html = html.replace("{{ATOMS_DB}}", "{}")

    injection = (
        "\n<script>"
        f"window.ATOMS_DB = {{}}; "
        f"window.ATOMS_BY_VIEW = {atoms_by_view_json}; "
        f"window.COVERAGE_BY_VIEW = {coverage_by_view_json}; "
        f"window.SPEC2VIZ_ATOM_WARNINGS = {warnings_json}; "
        f"window.SPEC2VIZ_COVERAGE_WARNINGS = {coverage_warnings_json}; "
        f"window.SPEC2VIZ_CATALOG = {catalog_metadata};"
        "</script>\n</body>"
    )
    html = html.replace("</body>", injection)

    return html


def build_deskops(config_path: Path, out_path: Path, base_dir: Path | None = None, atoms_dir: Path | None = None):
    html = render_deskops(config_path, base_dir, atoms_dir)
    out_path.write_text(html, encoding="utf-8")
