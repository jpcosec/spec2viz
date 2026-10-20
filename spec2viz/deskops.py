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


# Relaciones que el indice de aristas de sldb fabrica solo a partir de la estructura
# (secciones, tags, campos, modelos). No las declaro nadie: en el bundle no dicen nada.
_STRUCTURAL_RELATIONS = frozenset(
    {
        "has_section", "tagged_as", "has_document", "has_field", "has_model", "names",
        "semantic_parent", "semantic_equivalent", "applies_to_source", "applies_to_target",
    }
)
_DOC_NODE_PREFIX = "sldb://document/"


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
    _store_docs_cache: dict[str, list[dict]] = field(default_factory=dict)
    _view_store_cache: dict[str, Path | None] = field(default_factory=dict)
    _edges_cache: dict[tuple[str, str], list[dict]] = field(default_factory=dict)
    _edges_unavailable: set[str] = field(default_factory=set)

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
            import sldb.api  # noqa: F401 - solo la superficie publica
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
                store_path = self._find_local_store_with_boundary(candidate, boundary)
            else:
                store_path = self._find_local_store(candidate)
            if store_path is not None:
                break

        if store_path is not None and boundary is not None and not self._is_relative_to(store_path.parent, boundary):
            store_path = None

        self._view_store_cache[view_key] = store_path
        return store_path

    def _resolve_item_src_path(self, item: CatalogItem) -> Path | None:
        if not item.src:
            return None
        from spec2viz.orchestrator import resolve_item_path

        src_value = item.src.split("#", 1)[0]
        return resolve_item_path(src_value, Path(item.source_base_dir), "src").resolve()

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

    def _find_local_store_with_boundary(self, start: Path, boundary: Path) -> Path | None:
        current = start.resolve()
        boundary = boundary.resolve()
        for directory in [current, *current.parents]:
            if not self._is_relative_to(directory, boundary):
                break
            candidate = directory / ".sldb"
            if self._store_exists(candidate):
                return candidate.resolve()
            if directory == boundary:
                break
        return None

    def _find_local_store(self, start: Path) -> Path | None:
        current = start.resolve()
        for directory in [current, *current.parents]:
            candidate = directory / ".sldb"
            if self._store_exists(candidate):
                return candidate.resolve()
        return None

    @staticmethod
    def _store_exists(path: Path) -> bool:
        """Un `.sldb` es store si sldb puede leer su indice (API publica; sin tocar internos)."""
        if not path.is_dir():
            return False
        try:
            from sldb.api import store_links

            store_links(path)
            return True
        except Exception:
            return False

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

    def _load_store_documents(self, store_path: Path) -> list[dict]:
        """Documentos del store y de sus stores enlazados, via la API publica de sldb.

        Cada entrada trae `ref` (`Model:name`, o `alias:Model:name` si viene de un store
        enlazado), `store`, `model`, `name`, `title`, `path` absoluto y `payload`.
        """
        cache_key = str(store_path.resolve())
        if cache_key in self._store_docs_cache:
            return self._store_docs_cache[cache_key]
        try:
            from sldb.api import load_runtime_documents, open_store
        except Exception as exc:  # pragma: no cover - exercised through fallback path
            raise RuntimeError(f"SLDB import failed: {exc}") from exc

        roots: dict[str, Path] = {}
        docs: list[dict] = []
        for doc in load_runtime_documents(store_path.resolve(), self.pythonpath, include_linked=True):
            doc_store = str(doc.store_path)
            if doc_store not in roots:
                roots[doc_store] = Path(open_store(Path(doc_store)).project_root)
            store_name = str(getattr(doc, "store_name", "") or "local")
            ref = f"{doc.model_name}:{doc.name}" if store_name == "local" else f"{store_name}:{doc.model_name}:{doc.name}"
            payload = dict(doc.payload or {})
            docs.append(
                {
                    "ref": ref,
                    "store": doc_store,
                    "store_name": store_name,
                    "model": str(doc.model_name),
                    "name": str(doc.name),
                    "title": str(payload.get("title") or doc.name),
                    "path": str(roots[doc_store] / doc.path),
                    "payload": payload,
                }
            )
        self._store_docs_cache[cache_key] = docs
        return docs

    def _load_store_payload_uncached(self, store_path: Path) -> dict[str, dict]:
        payload: dict[str, dict] = {}
        for doc in self._load_store_documents(store_path):
            if doc["model"] != "AtomDoc":
                continue
            self._merge_atom(payload, doc["payload"], Path(doc["path"]), Path(doc["store"]))
        return payload

    def resolve_ref(self, store_path: Path, ref: str) -> dict | None:
        """El documento `Model:name` (o `alias:Model:name`) del store de la vista, o None."""
        try:
            docs = self._load_store_documents(store_path)
        except Exception as exc:
            self._warn(str(store_path), f"Failed to load documents through SLDB: {exc}")
            self._store_docs_cache[str(store_path.resolve())] = []
            return None
        return next((doc for doc in docs if doc["ref"] == ref), None)

    def edges_of(self, store_path: Path, ref: str) -> list[dict]:
        """Las aristas del grafo sldb que tocan el documento `ref`, en ambos sentidos.

        Solo las que alguien declaro (RelationDoc, `__references__`, `__containment__`...);
        las estructurales que el indice fabrica solo (secciones, tags, campos) no aportan
        nada en el bundle. Cada entrada: `relation`, `direction` (`out`/`in`), `node` (id
        del otro extremo), `ref` (`Model:name` si es documento, vacio si no), `title`.
        Si el store no tiene indice de aristas se avisa una vez y se devuelve vacio.
        """
        store_key = str(store_path.resolve())
        cache_key = (store_key, ref)
        if cache_key in self._edges_cache:
            return self._edges_cache[cache_key]
        edges: list[dict] = []
        if store_key not in self._edges_unavailable:
            try:
                from sldb.api import edges_from, edges_to

                titles = {doc["ref"]: doc["title"] for doc in self._load_store_documents(store_path)}
                for direction, records in (("out", edges_from(store_path, ref)), ("in", edges_to(store_path, ref))):
                    for record in records:
                        if record.relation in _STRUCTURAL_RELATIONS:
                            continue
                        other = str(record.target if direction == "out" else record.source)
                        other_ref = other[len(_DOC_NODE_PREFIX):] if other.startswith(_DOC_NODE_PREFIX) else ""
                        edges.append(
                            {
                                "relation": str(record.relation),
                                "direction": direction,
                                "node": other,
                                "ref": other_ref,
                                "title": titles.get(other_ref, other_ref or other),
                            }
                        )
            except Exception as exc:
                self._edges_unavailable.add(store_key)
                self._warn(str(store_path), f"Edge index unavailable through SLDB, relations left out: {exc}")
        self._edges_cache[cache_key] = edges
        return edges

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
                        "tags": tags,
                    }
            except Exception as exc:
                print(f"Failed to parse atom {md_file}: {exc}")
    return json.dumps(atoms_db)


def _tag_matches(tag: str, wanted: str) -> bool:
    """`wanted` calza con el tag completo (`ns:valor`) o con su valor sin namespace."""
    tag = str(tag).strip().lower()
    wanted = wanted.strip().lower()
    return tag == wanted or (":" in tag and tag.split(":", 1)[1] == wanted)


def filter_atoms_payload(payload: dict[str, dict], tags: list[str] | None) -> dict[str, dict]:
    """Deja solo los atomos que tengan al menos uno de `tags`; sin `tags` no filtra."""
    if not tags:
        return payload
    filtered: dict[str, dict] = {}
    for key, entry in payload.items():
        kept = {
            question: atom
            for question, atom in (entry.get("atoms") or {}).items()
            if any(_tag_matches(t, w) for t in (atom.get("tags") or []) for w in tags)
        }
        if kept:
            filtered[key] = {**entry, "atoms": kept}
    return filtered


def build_atoms_by_view(
    items: list[CatalogItem], atoms_dir: Path | None = None, atoms_tags: list[str] | None = None
) -> tuple[dict[str, dict[str, dict]], list[AtomBuildWarning]]:
    atoms_by_view, warnings = _raw_atoms_by_view(items, atoms_dir)
    if atoms_tags:
        atoms_by_view = {k: filter_atoms_payload(v, atoms_tags) for k, v in atoms_by_view.items()}
    return atoms_by_view, warnings


def _raw_atoms_by_view(
    items: list[CatalogItem], atoms_dir: Path | None = None, resolver: SldbAtomResolver | None = None
) -> tuple[dict[str, dict[str, dict]], list[AtomBuildWarning]]:
    resolver = resolver or SldbAtomResolver()
    atoms_by_view = resolver.build_atoms_by_view(items)

    if atoms_dir:
        fallback = json.loads(parse_atoms(atoms_dir))
        for item in items:
            view_key = item.anchor_id
            if atoms_by_view.get(view_key):
                continue
            atoms_by_view[view_key] = fallback

    return atoms_by_view, resolver.warnings


# --- vinculacion explicita nodo -> atomos (`atoms: [id, ...]` en el spec) -------------------

# coleccion del spec donde viven los elementos, por tipo de diagrama
_ELEMENT_COLLECTIONS = {
    "component": ("nodes",),
    "deployment": ("nodes", "artifacts"),
    "activity": ("steps",),
    "state": ("states",),
    "class": ("classes",),
    "sequence": ("participants",),
}


def label_key(value: str) -> str:
    """Misma normalizacion que `normKey` del template (minusculas, sin puntuacion)."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]+", " ", (value or "").strip().lower())).strip()


def _spec_elements(spec: dict) -> list[tuple[str, str, list[str], list[str]]]:
    """(id, label, atoms, refs) de cada elemento del spec que el catalogo puede mostrar."""
    data = spec.get("data") or {}
    out: list[tuple[str, str, list[str], list[str]]] = []
    for collection in _ELEMENT_COLLECTIONS.get(str(spec.get("type")), ()):
        raw = data.get(collection) or {}
        pairs = raw.items() if isinstance(raw, dict) else [(e.get("id"), e) for e in raw if isinstance(e, dict)]
        for eid, el in pairs:
            if not eid:
                continue
            el = el if isinstance(el, dict) else {}
            atoms = [str(a) for a in (el.get("atoms") or [])]
            refs = [str(r) for r in (el.get("refs") or [])]
            out.append((str(eid), str(el.get("label") or eid), atoms, refs))
    return out


def _item_specs(item: CatalogItem) -> list[dict]:
    """Los specs YAML de una vista que se pudieron leer, como dicts."""
    from spec2viz.orchestrator import CatalogLoader

    loader = CatalogLoader()
    specs: list[dict] = []
    for spec_ref in item.specs:
        spec_path = loader._resolve_spec_path(spec_ref, Path(item.source_base_dir))
        if spec_path is None:
            continue
        try:
            spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if isinstance(spec, dict):
            specs.append(spec)
    return specs


def collect_explicit_atoms(item: CatalogItem) -> tuple[dict[str, list[str]], int, int]:
    """Mapa `clave de etiqueta -> [atom-id]` de los specs de la vista, total de elementos y cuantos traen `atoms`.

    Se indexa por etiqueta e id normalizados porque el template solo ve el texto del nodo
    renderizado (en Mermaid no hay forma robusta de poner `data-atoms` en el SVG).
    """
    explicit: dict[str, list[str]] = {}
    total = 0
    with_atoms = 0
    for spec in _item_specs(item):
        for eid, label, atoms, _refs in _spec_elements(spec):
            total += 1
            if not atoms:
                continue
            with_atoms += 1
            for key in {label_key(label), label_key(eid)}:
                bucket = explicit.setdefault(key, [])
                bucket.extend(a for a in atoms if a not in bucket)
    return explicit, total, with_atoms


def _atom_index(payload: dict[str, dict]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for entry in payload.values():
        for question, atom in (entry.get("atoms") or {}).items():
            if atom.get("id"):
                index[str(atom["id"])] = {
                    "id": atom["id"],
                    "title": entry.get("title", ""),
                    "question": question,
                    "body": atom.get("body", ""),
                }
    return index


_WIKILINK = re.compile(r"\[\[([^\[\]]+?)\]\]")


class UnknownAtomError(ValueError):
    """Un spec referencia un atomo que no existe entre los cargados (`--strict-atoms`)."""


def build_explicit_atoms(
    items: list[CatalogItem],
    raw_atoms_by_view: dict[str, dict[str, dict]],
    strict: bool = False,
) -> tuple[dict[str, dict[str, dict]], set[str], list[AtomBuildWarning], dict[str, dict]]:
    """Resuelve los `atoms:` de los specs.

    Devuelve (`view -> clave -> {title, list}`, vistas totalmente explicitas, warnings,
    `id -> atomo` de los enlazados con `[[id]]` desde los explicitos, un nivel).
    """
    linked: dict[str, dict] = {}
    result: dict[str, dict[str, dict]] = {}
    complete: set[str] = set()
    warnings: list[AtomBuildWarning] = []
    for item in items:
        explicit, total, with_atoms = collect_explicit_atoms(item)
        if not explicit:
            continue
        index = _atom_index(raw_atoms_by_view.get(item.anchor_id) or {})
        resolved: dict[str, dict] = {}
        for key, ids in explicit.items():
            found = []
            for atom_id in ids:
                if atom_id in index:
                    found.append(index[atom_id])
                else:
                    msg = f"{item.id}: atomo '{atom_id}' (nodo '{key}') no existe entre los atomos cargados"
                    warnings.append(AtomBuildWarning(scope=item.anchor_id, message=msg))
                    print(f"[spec2viz][atoms] {msg}", file=sys.stderr)
            if found:
                resolved[key] = {"title": key, "explicit": True, "list": found}
                for atom in found:
                    for target in _WIKILINK.findall(atom.get("body") or ""):
                        target = target.strip()
                        if target in index:
                            linked[target] = index[target]
        if resolved:
            result[item.anchor_id] = resolved
        if total and with_atoms == total and len(resolved) == len(explicit):
            complete.add(item.anchor_id)
    if strict and warnings:
        raise UnknownAtomError("; ".join(w.message for w in warnings))
    return result, complete, warnings, linked


def collect_explicit_refs(item: CatalogItem) -> dict[str, list[str]]:
    """Mapa `clave de etiqueta -> [ref]` de los `refs:` de los elementos de la vista."""
    explicit: dict[str, list[str]] = {}
    for spec in _item_specs(item):
        for eid, label, _atoms, refs in _spec_elements(spec):
            if not refs:
                continue
            for key in {label_key(label), label_key(eid)}:
                bucket = explicit.setdefault(key, [])
                bucket.extend(r for r in refs if r not in bucket)
    return explicit


_SUMMARY_FIELDS = ("summary", "answer", "content", "purpose", "docstring", "goal", "description")


def _ref_payload(doc: dict) -> dict:
    payload = doc.get("payload") or {}
    summary = next((str(payload[f]).strip() for f in _SUMMARY_FIELDS if payload.get(f)), "")
    return {key: doc.get(key, "") for key in ("ref", "model", "name", "title", "path", "store")} | {"summary": summary[:300]}


def build_explicit_refs(
    items: list[CatalogItem], resolver: SldbAtomResolver | None = None, strict: bool = False
) -> tuple[dict[str, dict[str, list[dict]]], list[AtomBuildWarning]]:
    """Resuelve los `refs: [Model:name]` de los specs contra el store sldb de cada vista.

    Devuelve `view -> clave de etiqueta -> [{ref, model, name, title, path, store, summary}]`
    y los warnings; con `strict` una ref que no existe aborta el build.
    """
    resolver = resolver or SldbAtomResolver()
    result: dict[str, dict[str, list[dict]]] = {}
    warnings: list[AtomBuildWarning] = []
    for item in items:
        explicit = collect_explicit_refs(item)
        if not explicit:
            continue
        store_path = resolver._discover_store_for_item(item)
        resolved: dict[str, list[dict]] = {}
        for key, refs in explicit.items():
            found = []
            for ref in refs:
                doc = resolver.resolve_ref(store_path, ref) if store_path is not None else None
                if doc is None:
                    where = "sin store sldb para la vista" if store_path is None else "no existe en el store sldb de la vista"
                    msg = f"{item.id}: ref '{ref}' (nodo '{key}') {where}"
                    warnings.append(AtomBuildWarning(scope=item.anchor_id, message=msg))
                    print(f"[spec2viz][refs] {msg}", file=sys.stderr)
                    continue
                found.append(_ref_payload(doc) | {"edges": resolver.edges_of(store_path, ref)})
            if found:
                resolved[key] = found
        if resolved:
            result[item.anchor_id] = resolved
    if strict and warnings:
        raise UnknownAtomError("; ".join(w.message for w in warnings))
    return result, warnings


def attach_atom_edges(
    items: list[CatalogItem],
    explicit_atoms: dict[str, dict[str, dict]],
    linked_atoms: dict[str, dict],
    resolver: SldbAtomResolver,
    atoms_by_view: dict[str, dict[str, dict]] | None = None,
) -> None:
    """Cuelga `edges` (las aristas sldb de `AtomDoc:<id>`) de cada atomo explicito, enlazado o difuso."""
    atoms_by_view = atoms_by_view or {}
    for item in items:
        store_path = resolver._discover_store_for_item(item)
        if store_path is None:
            continue
        explicit = [a for entry in (explicit_atoms.get(item.anchor_id) or {}).values() for a in entry.get("list") or []]
        fuzzy = [a for entry in (atoms_by_view.get(item.anchor_id) or {}).values() for a in (entry.get("atoms") or {}).values()]
        for atom in [*explicit, *linked_atoms.values(), *fuzzy]:
            if atom.get("id") and "edges" not in atom:
                atom["edges"] = resolver.edges_of(store_path, f"AtomDoc:{atom['id']}")


def split_shared_atoms(atoms_by_view: dict[str, dict[str, dict]]) -> tuple[dict[str, dict], dict[str, dict[str, dict]]]:
    """Saca a un `ATOMS_DB` comun el payload repetido en varias vistas.

    El template cae a `ATOMS_DB` cuando la vista no esta en `ATOMS_BY_VIEW`, asi que el
    payload mas repetido (no vacio) se emite una sola vez en vez de una por vista.
    """
    counts: dict[str, int] = {}
    for payload in atoms_by_view.values():
        if payload:
            key = json.dumps(payload, sort_keys=True)
            counts[key] = counts.get(key, 0) + 1
    if not counts:
        return {}, atoms_by_view
    shared_key, shared_count = max(counts.items(), key=lambda kv: kv[1])
    if shared_count < 2:
        return {}, atoms_by_view
    shared = json.loads(shared_key)
    rest = {
        view: payload
        for view, payload in atoms_by_view.items()
        if not (payload and json.dumps(payload, sort_keys=True) == shared_key)
    }
    return shared, rest


def build_coverage_by_view(
    items: list[CatalogItem], snapshot_path: Path | None = None, kgdb_snapshot_path: Path | None = None
) -> tuple[dict[str, dict], list[CoverageBuildWarning]]:
    """Cobertura por vista a partir de un snapshot de grafo con nodos `view` (el
    `knowledge_graph.kg.json` de la epoca de kgdb; `kgdb_snapshot_path` se acepta como alias).
    Sin snapshot la proyeccion queda vacia y se avisa; nada mas depende de el."""
    warnings: list[CoverageBuildWarning] = []
    snapshot_path = snapshot_path or kgdb_snapshot_path or _discover_snapshot_path(items)
    if snapshot_path is None or not snapshot_path.exists():
        warnings.append(CoverageBuildWarning(scope="snapshot", message="Graph snapshot not found; coverage projection is empty."))
        return {item.anchor_id: _empty_coverage_payload(item) for item in items}, warnings

    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except Exception as exc:
        warnings.append(CoverageBuildWarning(scope=str(snapshot_path), message=f"Failed to read graph snapshot: {exc}"))
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


def render_deskops(
    config_path: Path,
    base_dir: Path | None = None,
    atoms_dir: Path | None = None,
    atoms_tags: list[str] | None = None,
    strict_atoms: bool = False,
) -> str:
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

    resolver = SldbAtomResolver()
    raw_atoms_by_view, warnings = _raw_atoms_by_view(catalog.items, atoms_dir, resolver)
    explicit_atoms, complete_views, explicit_warnings, linked_atoms = build_explicit_atoms(
        catalog.items, raw_atoms_by_view, strict=strict_atoms
    )
    explicit_refs, ref_warnings = build_explicit_refs(catalog.items, resolver, strict=strict_atoms)
    attach_atom_edges(catalog.items, explicit_atoms, linked_atoms, resolver, raw_atoms_by_view)
    warnings = [*warnings, *explicit_warnings, *ref_warnings]
    atoms_by_view = {
        view: filter_atoms_payload(payload, atoms_tags) if atoms_tags else payload
        for view, payload in raw_atoms_by_view.items()
    }
    # vista con todos sus nodos explicitos: no hace falta coincidencia difusa, no se embebe nada mas
    for view in complete_views:
        atoms_by_view[view] = {}
    shared_atoms, atoms_by_view = split_shared_atoms(atoms_by_view)
    coverage_by_view, coverage_warnings = build_coverage_by_view(catalog.items)
    atoms_by_view_json = json.dumps(atoms_by_view)
    shared_atoms_json = json.dumps(shared_atoms)
    explicit_atoms_json = json.dumps(explicit_atoms)
    linked_atoms_json = json.dumps(linked_atoms)
    explicit_refs_json = json.dumps(explicit_refs)
    coverage_by_view_json = json.dumps(coverage_by_view)
    warnings_json = json.dumps([warning.__dict__ for warning in warnings])
    coverage_warnings_json = json.dumps([warning.__dict__ for warning in coverage_warnings])
    catalog_metadata = render_catalog_metadata(catalog, catalog.items)

    if "{{ATOMS_DB}}" in html:
        html = html.replace("{{ATOMS_DB}}", "{}")

    injection = (
        "\n<script>"
        f"window.ATOMS_DB = {shared_atoms_json}; "
        f"window.ATOMS_BY_VIEW = {atoms_by_view_json}; "
        f"window.ATOMS_EXPLICIT = {explicit_atoms_json}; "
        f"window.ATOMS_LINKED = {linked_atoms_json}; "
        f"window.REFS_EXPLICIT = {explicit_refs_json}; "
        f"window.COVERAGE_BY_VIEW = {coverage_by_view_json}; "
        f"window.SPEC2VIZ_ATOM_WARNINGS = {warnings_json}; "
        f"window.SPEC2VIZ_COVERAGE_WARNINGS = {coverage_warnings_json}; "
        f"window.SPEC2VIZ_CATALOG = {catalog_metadata};"
        "</script>\n</body>"
    )
    html = html.replace("</body>", injection)

    return html


def build_deskops(
    config_path: Path,
    out_path: Path,
    base_dir: Path | None = None,
    atoms_dir: Path | None = None,
    atoms_tags: list[str] | None = None,
    strict_atoms: bool = False,
):
    html = render_deskops(config_path, base_dir, atoms_dir, atoms_tags, strict_atoms)
    out_path.write_text(html, encoding="utf-8")
