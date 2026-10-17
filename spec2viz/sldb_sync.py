"""Sincroniza un spec de diagrama con un store sldb: nodos, aristas y el spec como documentos.

Solo usa la superficie publica de sldb (`sldb.api`). Lo que escribe:

- `SpecDoc:<spec id>` con la ruta y el hash del YAML, que referencia a sus nodos.
- `SpecNodeDoc:<spec id>.<elemento>` por cada elemento del spec (nodo, estado, paso,
  clase, participante), con sus `refs:`, `atoms:` y `contains:`.
- Un `RelationDoc` por cada arista del spec, con la relacion del spec como tipo; si el
  tipo no es builtin, el `RelationTypeDoc` que falta se crea en `sldb/relation_types/`.

Los documentos de una sincronizacion anterior que ya no estan en el spec se borran.
Al final se reconstruye el indice de aristas y se valida.
"""

from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from spec2viz.deskops import _ELEMENT_COLLECTIONS

MODEL_REFS = {
    "SpecDoc": "spec2viz.sldb_models:SpecDoc",
    "SpecNodeDoc": "spec2viz.sldb_models:SpecNodeDoc",
}

# coleccion de aristas por tipo de diagrama: (coleccion, campo con la relacion o None,
# relacion por defecto). Con campo None todas las aristas llevan la relacion por defecto.
_EDGE_COLLECTIONS: dict[str, tuple[str, str | None, str]] = {
    "component": ("edges", "relation", "uses"),
    "deployment": ("connections", "protocol", "connects"),
    "state": ("transitions", None, "transitions_to"),
    "sequence": ("messages", None, "sends"),
    "class": ("relations", "relation", "association"),
}

# campo que mejor describe una arista, para las notas del RelationDoc
_EDGE_LABEL_FIELDS = ("label", "on", "message", "protocol")

RELATION_TYPES_DIR = Path("sldb") / "relation_types"


@dataclass
class SyncReport:
    spec_id: str
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    relation_types_added: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    edge_errors: list[str] = field(default_factory=list)

    @property
    def problems(self) -> list[str]:
        return [*self.unresolved, *self.edge_errors]


def relation_token(value: Any, default: str) -> str:
    """La relacion del spec como token de vocabulario sldb (`loads(path)` -> `loads_path`)."""
    token = re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")
    return token or default


def node_ref(spec_id: str, element_id: str) -> str:
    return f"SpecNodeDoc:{spec_id}.{element_id}"


def to_slash_ref(ref: str) -> str:
    """`Model:name` (o `alias:Model:name`) en la forma `Model/name` que `doc_exists` entiende."""
    head, _, name = ref.rpartition(":")
    return f"{head}/{name}"


def spec_elements(spec: dict) -> list[dict]:
    """Los elementos del spec: id, label, kind, contains, atoms, refs, description."""
    data = spec.get("data") or {}
    out: list[dict] = []
    for collection in _ELEMENT_COLLECTIONS.get(str(spec.get("type")), ()):
        raw = data.get(collection) or {}
        pairs = raw.items() if isinstance(raw, dict) else [(e.get("id"), e) for e in raw if isinstance(e, dict)]
        for eid, el in pairs:
            if not eid:
                continue
            el = el if isinstance(el, dict) else {}
            out.append(
                {
                    "id": str(eid),
                    "label": str(el.get("label") or el.get("name") or eid),
                    "kind": str(el.get("kind") or el.get("type") or ""),
                    "contains": [str(c) for c in (el.get("contains") or [])],
                    "atoms": [str(a) for a in (el.get("atoms") or [])],
                    "refs": [str(r) for r in (el.get("refs") or [])],
                    "description": str(el.get("description") or el.get("docstring") or ""),
                }
            )
    return out


def spec_edges(spec: dict) -> list[dict]:
    """Las aristas del spec: from, to, relation (token) y label."""
    entry = _EDGE_COLLECTIONS.get(str(spec.get("type")))
    if entry is None:
        return []
    collection, relation_field, default = entry
    out: list[dict] = []
    for raw in (spec.get("data") or {}).get(collection) or []:
        if not isinstance(raw, dict) or not raw.get("from") or not raw.get("to"):
            continue
        relation = relation_token(raw.get(relation_field) if relation_field else None, default)
        label = next((str(raw[f]) for f in _EDGE_LABEL_FIELDS if raw.get(f)), "")
        out.append({"from": str(raw["from"]), "to": str(raw["to"]), "relation": relation, "label": label})
    return out


def find_store(start: Path) -> Path | None:
    """El `.sldb` mas cercano hacia arriba desde `start`, si sldb lo reconoce como store."""
    from spec2viz.deskops import SldbAtomResolver

    return SldbAtomResolver()._find_local_store(start)


class SpecSync:
    """Escribe un spec en un store. Una instancia por store; `sync` por spec."""

    def __init__(self, store_path: Path, pythonpath: str | None = None, out_dir: Path | None = None, actor: str = "spec2viz"):
        self.store_path = Path(store_path).resolve()
        self.pythonpath = pythonpath
        self.out_dir = out_dir
        self.actor = actor
        self._prepared = False

    # --- preparacion del store -------------------------------------------------------

    def prepare(self) -> None:
        """Registra SpecDoc/SpecNodeDoc y las relaciones builtin; idempotente."""
        if self._prepared:
            return
        import sldb.api as api

        for name, ref in MODEL_REFS.items():
            try:
                api.load_registered_model(self.store_path, name, self.pythonpath)
            except Exception:
                api.add_model(self.store_path, ref, self.pythonpath, actor=self.actor)
        api.init_relations(self.store_path, self.pythonpath)
        self._prepared = True

    # --- sincronizacion -----------------------------------------------------------------

    def sync(self, spec_path: Path) -> SyncReport:
        import sldb.api as api
        from spec2viz.loader import load as load_spec

        spec_path = Path(spec_path).resolve()
        load_spec(spec_path)  # valida contra los modelos de spec2viz antes de tocar el store
        text = spec_path.read_text(encoding="utf-8")
        spec = yaml.safe_load(text) or {}
        spec_id = str(spec["id"])
        report = SyncReport(spec_id=spec_id)

        self.prepare()
        root = Path(api.open_store(self.store_path).project_root).resolve()
        out = (self.out_dir or spec_path.parent / "sldb" / spec_id).resolve()
        existing = self._existing_documents()

        def upsert(model: str, name: str, path: Path, payload: dict) -> None:
            if (model, name) in existing:
                api.save_document_payload(self.store_path, model, name, payload, self.pythonpath, actor=self.actor)
                report.updated.append(f"{model}:{name}")
            else:
                api.create_document(self.store_path, model, path, payload, name=name, pythonpath=self.pythonpath, actor=self.actor)
                report.created.append(f"{model}:{name}")

        elements = spec_elements(spec)
        edges = spec_edges(spec)

        # tipos de relacion que el spec usa y el store no conoce
        for relation in sorted({e["relation"] for e in edges}):
            type_name = f"reltype-{relation}"
            if ("RelationTypeDoc", type_name) in existing or api.doc_exists(self.store_path, f"RelationTypeDoc/{type_name}"):
                continue
            payload = {
                "title": relation,
                "name": relation,
                "direction": "directed",
                "cardinality": "many_to_many",
                "axis": "",
                "source_types": [],
                "target_types": [],
                "condition": "",
                "description": f"Relacion `{relation}` declarada por las aristas del spec `{spec_id}` de spec2viz.",
            }
            api.create_document(
                self.store_path, "RelationTypeDoc", root / RELATION_TYPES_DIR / f"{relation}.md", payload,
                name=type_name, pythonpath=self.pythonpath, actor=self.actor,
            )
            report.relation_types_added.append(relation)
            existing[("RelationTypeDoc", type_name)] = None

        # nodos
        current: set[tuple[str, str]] = set()
        for el in elements:
            name = f"{spec_id}.{el['id']}"
            payload = {
                "id": name,
                "title": el["label"],
                "spec": f"SpecDoc:{spec_id}",
                "element": el["id"],
                "kind": el["kind"],
                "refs": el["refs"],
                "atom_refs": [f"AtomDoc:{a}" for a in el["atoms"]],
                "contains": [node_ref(spec_id, c) for c in el["contains"]],
                "description": el["description"],
            }
            upsert("SpecNodeDoc", name, out / "nodes" / f"{name}.md", payload)
            current.add(("SpecNodeDoc", name))

        # el spec
        try:
            rel_spec_path = str(spec_path.relative_to(root))
        except ValueError:
            rel_spec_path = str(spec_path)
        spec_payload = {
            "id": spec_id,
            "title": str(spec.get("title") or spec_id),
            "diagram_type": str(spec.get("type") or ""),
            "version": str(spec.get("version") or ""),
            "spec_path": rel_spec_path,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "nodes": [node_ref(spec_id, el["id"]) for el in elements],
            "description": str((spec.get("metadata") or {}).get("description") or ""),
        }
        upsert("SpecDoc", spec_id, out / f"{spec_id}.md", spec_payload)

        # aristas
        seen: dict[str, int] = {}
        for edge in edges:
            base = f"{spec_id}.{edge['from']}__{edge['relation']}__{edge['to']}"
            seen[base] = seen.get(base, 0) + 1
            name = base if seen[base] == 1 else f"{base}__{seen[base]}"
            payload = {
                "title": f"{edge['from']} {edge['relation']} {edge['to']}",
                "source_id": node_ref(spec_id, edge["from"]),
                "target_id": node_ref(spec_id, edge["to"]),
                "relation_type": edge["relation"],
                "condition": "",
                "notes": edge["label"],
            }
            upsert("RelationDoc", name, out / "edges" / f"{name}.md", payload)
            current.add(("RelationDoc", name))

        # lo que quedo de una sincronizacion anterior y ya no esta en el spec
        prefix = f"{spec_id}."
        for (model, name), doc in existing.items():
            if model not in ("SpecNodeDoc", "RelationDoc") or not name.startswith(prefix) or (model, name) in current:
                continue
            api.delete_document(self.store_path, str(doc.path), self.pythonpath, actor=self.actor)
            report.deleted.append(f"{model}:{name}")

        # refs y atoms que no existen: aristas de schema, el indice no las reporta
        for el in elements:
            for ref in [*el["refs"], *(f"AtomDoc:{a}" for a in el["atoms"])]:
                if not api.doc_exists(self.store_path, to_slash_ref(ref)):
                    report.unresolved.append(f"{spec_id}.{el['id']}: '{ref}' no existe en el store")

        api.rebuild_edges(self.store_path, self.pythonpath)
        report.edge_errors = list(api.check_edges(self.store_path).errors)
        return report

    def _existing_documents(self) -> dict[tuple[str, str], Any]:
        import sldb.api as api

        return {
            (str(doc.model_name), str(doc.name)): doc
            for doc in api.load_runtime_documents(self.store_path, self.pythonpath, include_linked=False)
            if str(doc.model_name) in ("SpecDoc", "SpecNodeDoc", "RelationDoc", "RelationTypeDoc")
        }


def format_report(report: SyncReport) -> str:
    """Una linea por spec, con lo que paso."""
    nodes = sum(1 for d in [*report.created, *report.updated] if d.startswith("SpecNodeDoc:"))
    edges = sum(1 for d in [*report.created, *report.updated] if d.startswith("RelationDoc:"))
    line = (
        f"Synced {report.spec_id}: {nodes} nodes, {edges} edges "
        f"({len(report.created)} created, {len(report.updated)} updated, {len(report.deleted)} deleted"
    )
    if report.relation_types_added:
        line += f", relation types added: {', '.join(report.relation_types_added)}"
    line += ")"
    for problem in report.problems:
        line += f"\n  ! {problem}"
    return line


__all__ = ["SpecSync", "SyncReport", "find_store", "format_report", "spec_edges", "spec_elements", "relation_token", "node_ref"]


if __name__ == "__main__":  # pragma: no cover
    print("Use `spec2viz diagram sync`.", file=sys.stderr)
