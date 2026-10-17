"""Sincroniza un spec de diagrama con un store sldb: nodos, aristas, el spec y su notacion.

Solo usa la superficie publica de sldb (`sldb.api`). Lo que escribe:

- `SpecDoc:<spec id>` con la ruta y el hash del YAML, que referencia a sus nodos y a su
  notacion.
- `SpecNodeDoc:<spec id>.<elemento>` por cada elemento del spec (nodo, estado, paso,
  clase, participante), con sus `refs:`, `atoms:`, `contains:` y el resto del elemento en
  `data` (atributos, metodos, guardas), que es de donde leen los compartimentos.
- Un `RelationDoc` por cada arista del spec, con la relacion del spec como tipo; si el
  tipo no es builtin, el `RelationTypeDoc` que falta se crea en `sldb/relation_types/`.
- La notacion del spec (`NotationDoc`, `GlyphDoc`, `LinkDoc`), en `sldb/notations/<name>/`,
  si el tipo de diagrama tiene una por defecto o se pide una.

Los documentos de una sincronizacion anterior que ya no estan en el spec (o en la
notacion) se borran. Al final se reconstruye el indice de aristas y se valida.
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
from spec2viz.notation import DEFAULT_NOTATIONS, NotationSpec, glyph_ref, link_ref, load_notation, notation_ref

MODEL_REFS = {
    "SpecDoc": "spec2viz.sldb_models:SpecDoc",
    "SpecNodeDoc": "spec2viz.sldb_models:SpecNodeDoc",
    "NotationDoc": "spec2viz.sldb_models:NotationDoc",
    "GlyphDoc": "spec2viz.sldb_models:GlyphDoc",
    "LinkDoc": "spec2viz.sldb_models:LinkDoc",
}

_MANAGED_MODELS = ("SpecDoc", "SpecNodeDoc", "RelationDoc", "RelationTypeDoc", "NotationDoc", "GlyphDoc", "LinkDoc")

# coleccion de aristas por tipo de diagrama: (coleccion, campo con la relacion o None,
# relacion por defecto). Con campo None todas las aristas llevan la relacion por defecto.
# activity y component_view_matrix no tienen coleccion de aristas: salen de los elementos.
_EDGE_COLLECTIONS: dict[str, tuple[str, str | None, str]] = {
    "component": ("edges", "relation", "uses"),
    "deployment": ("connections", "protocol", "connects"),
    "state": ("transitions", None, "transitions_to"),
    "sequence": ("messages", "kind", "sends"),
    "class": ("relations", "relation", "association"),
    "reflection": ("edges", "relation", "relates_to"),
}

# el `kind` de un mensaje de secuencia como relacion (los renderers tratan todo lo que no es
# async/return como sincrono; aqui los sinonimos que aparecen en los specs)
_MESSAGE_RELATIONS = {
    "sync": "sends", "call": "sends", "": "sends",
    "async": "sends_async", "signal": "sends_async",
    "return": "returns", "reply": "returns", "response": "returns",
}

# colecciones de elementos por tipo de diagrama (las de deskops mas reflection)
_ELEMENT_COLLECTIONS_SYNC: dict[str, tuple[str, ...]] = {**_ELEMENT_COLLECTIONS, "reflection": ("nodes",)}

# campo que mejor describe una arista, para las notas del RelationDoc
_EDGE_LABEL_FIELDS = ("label", "on", "message", "protocol")

# campos del elemento que ya tienen sitio propio en SpecNodeDoc; el resto va a `data`
_ELEMENT_OWN_FIELDS = frozenset({"id", "label", "name", "kind", "type", "contains", "atoms", "refs", "description", "docstring"})

RELATION_TYPES_DIR = Path("sldb") / "relation_types"
NOTATIONS_DIR = Path("sldb") / "notations"


@dataclass
class SyncReport:
    spec_id: str
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    relation_types_added: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    edge_errors: list[str] = field(default_factory=list)
    notation: str = ""

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


def _plain(value: Any) -> Any:
    """Un valor del spec como dato YAML plano (sin tuplas)."""
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


def _element(eid: Any, el: Any, collection: str, extra_flags: dict[str, Any] | None = None) -> dict:
    el = el if isinstance(el, dict) else {}
    extra = {str(k): _plain(v) for k, v in el.items() if k not in _ELEMENT_OWN_FIELDS and v is not None}
    extra.update(extra_flags or {})
    return {
        "id": str(eid),
        "label": str(el.get("label") or el.get("name") or eid),
        "kind": str(el.get("kind") or el.get("type") or ""),
        "collection": collection,
        "contains": [str(c) for c in (el.get("contains") or [])],
        "atoms": [str(a) for a in (el.get("atoms") or [])],
        "refs": [str(r) for r in (el.get("refs") or [])],
        "description": str(el.get("description") or el.get("docstring") or ""),
        "data": extra,
    }


def stage_id(view_id: str, stage: str) -> str:
    """Id de elemento de una etapa de una vista de matriz: `<vista>__<etapa>`."""
    return f"{view_id}__{stage}"


def _matrix_elements(data: dict) -> list[dict]:
    """Componentes (anidados por `children` -> contains) y etapas por vista (`collection: stages`)."""
    out: list[dict] = []
    for view in data.get("views") or []:
        if not isinstance(view, dict) or not view.get("id"):
            continue
        for order, stage in enumerate(view.get("stages") or [], start=1):
            if isinstance(stage, dict) and stage.get("id"):
                out.append(_element(stage_id(str(view["id"]), str(stage["id"])), {"label": stage.get("label") or stage["id"]}, "stages",
                                    {"view": str(view["id"]), "view_label": str(view.get("label") or view["id"]), "order": order}))

    def walk(components: Any) -> None:
        for comp in components or []:
            if not isinstance(comp, dict) or not comp.get("name"):
                continue
            children = [c for c in comp.get("children") or [] if isinstance(c, dict) and c.get("name")]
            el = _element(comp["name"], {k: v for k, v in comp.items() if k != "children"}, "components")
            el["contains"] = [str(c["name"]) for c in children]
            out.append(el)
            walk(children)

    walk(data.get("components"))
    return out


def spec_elements(spec: dict) -> list[dict]:
    """Los elementos del spec: id, label, kind, collection, contains, atoms, refs, description y data.

    `data` es el resto del elemento; ademas `initial`/`final` marcan el estado o paso inicial y
    final (state, activity) y las etapas de una matriz llevan `view` y `order`.
    """
    data = spec.get("data") or {}
    diagram_type = str(spec.get("type"))
    if diagram_type == "component_view_matrix":
        return _matrix_elements(data)
    flags: dict[str, dict[str, Any]] = {}
    if diagram_type == "state" and data.get("initial"):
        flags[str(data["initial"])] = {"initial": True}
    if diagram_type == "activity":
        if data.get("start"):
            flags[str(data["start"])] = {"initial": True}
        if data.get("end"):
            flags.setdefault(str(data["end"]), {})["final"] = True
    out: list[dict] = []
    for collection in _ELEMENT_COLLECTIONS_SYNC.get(diagram_type, ()):
        raw = data.get(collection) or {}
        pairs = raw.items() if isinstance(raw, dict) else [(e.get("id"), e) for e in raw if isinstance(e, dict)]
        for eid, el in pairs:
            if eid:
                out.append(_element(eid, el, collection, flags.get(str(eid))))
    return out


def _edge_label(raw: dict) -> str:
    label = next((str(raw[f]) for f in _EDGE_LABEL_FIELDS if raw.get(f)), "")
    if raw.get("guard"):
        label = f"{label} [{raw['guard']}]".strip()
    return label


def _activity_edges(data: dict) -> list[dict]:
    """`next` -> relacion `next`; cada rama de `branches` -> relacion `branch` con su etiqueta."""
    out: list[dict] = []
    for sid, step in (data.get("steps") or {}).items():
        if not isinstance(step, dict):
            continue
        if step.get("next"):
            out.append({"from": str(sid), "to": str(step["next"]), "relation": "next", "label": "", "condition": ""})
        for label, target in (step.get("branches") or {}).items():
            out.append({"from": str(sid), "to": str(target), "relation": "branch", "label": str(label), "condition": ""})
    return out


def _matrix_edges(data: dict) -> list[dict]:
    """Un `occupies` por componente y etapa de cada vista; la vista va en la etiqueta."""
    out: list[dict] = []

    def walk(components: Any) -> None:
        for comp in components or []:
            if not isinstance(comp, dict) or not comp.get("name"):
                continue
            for view_id, stages in (comp.get("stages") or {}).items():
                for stage in stages or []:
                    out.append({"from": str(comp["name"]), "to": stage_id(str(view_id), str(stage)), "relation": "occupies", "label": str(view_id), "condition": ""})
            walk(comp.get("children"))

    walk(data.get("components"))
    return out


def spec_edges(spec: dict) -> list[dict]:
    """Las aristas del spec en orden: from, to, relation (token), label (con la guarda) y condition."""
    data = spec.get("data") or {}
    diagram_type = str(spec.get("type"))
    if diagram_type == "activity":
        return _activity_edges(data)
    if diagram_type == "component_view_matrix":
        return _matrix_edges(data)
    entry = _EDGE_COLLECTIONS.get(diagram_type)
    if entry is None:
        return []
    collection, relation_field, default = entry
    out: list[dict] = []
    for raw in data.get(collection) or []:
        if not isinstance(raw, dict) or not raw.get("from") or not raw.get("to"):
            continue
        value = raw.get(relation_field) if relation_field else None
        if diagram_type == "sequence":
            relation = _MESSAGE_RELATIONS.get(str(value or "").strip().lower(), relation_token(value, default))
        else:
            relation = relation_token(value, default)
        condition = str(raw.get("condition") or "") if diagram_type == "sequence" else ""
        out.append({"from": str(raw["from"]), "to": str(raw["to"]), "relation": relation, "label": _edge_label(raw), "condition": condition})
    return out


def edge_name(spec_id: str, index: int, count: int, edge: dict) -> str:
    """`<spec>.<nn>-<from>__<rel>__<to>`: el prefijo ordena las aristas y evita duplicados."""
    width = max(2, len(str(count)))
    return f"{spec_id}.{index:0{width}d}-{edge['from']}__{edge['relation']}__{edge['to']}"


def find_store(start: Path) -> Path | None:
    """El `.sldb` mas cercano hacia arriba desde `start`, si sldb lo reconoce como store."""
    from spec2viz.deskops import SldbAtomResolver

    return SldbAtomResolver()._find_local_store(start)


class _StoreWriter:
    """Lo comun a sincronizar specs y notaciones: preparar el store, upsert, tipos de relacion."""

    def __init__(self, store_path: Path, pythonpath: str | None = None, actor: str = "spec2viz"):
        self.store_path = Path(store_path).resolve()
        self.pythonpath = pythonpath
        self.actor = actor
        self._prepared = False
        self._root: Path | None = None

    def prepare(self) -> None:
        """Registra los modelos de spec2viz y las relaciones builtin; idempotente."""
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

    @property
    def root(self) -> Path:
        if self._root is None:
            import sldb.api as api

            self._root = Path(api.open_store(self.store_path).project_root).resolve()
        return self._root

    def existing_documents(self) -> dict[tuple[str, str], Any]:
        import sldb.api as api

        return {
            (str(doc.model_name), str(doc.name)): doc
            for doc in api.load_runtime_documents(self.store_path, self.pythonpath, include_linked=False)
            if str(doc.model_name) in _MANAGED_MODELS
        }

    def upsert(self, existing: dict, report: SyncReport, model: str, name: str, path: Path, payload: dict) -> None:
        import sldb.api as api

        if (model, name) in existing:
            api.save_document_payload(self.store_path, model, name, payload, self.pythonpath, actor=self.actor)
            report.updated.append(f"{model}:{name}")
        else:
            api.create_document(self.store_path, model, path, payload, name=name, pythonpath=self.pythonpath, actor=self.actor)
            report.created.append(f"{model}:{name}")

    def ensure_relation_type(self, existing: dict, report: SyncReport, relation: str, description: str) -> None:
        """Crea el `RelationTypeDoc` de `relation` si el store no lo tiene."""
        import sldb.api as api

        type_name = f"reltype-{relation}"
        if ("RelationTypeDoc", type_name) in existing or api.doc_exists(self.store_path, f"RelationTypeDoc/{type_name}"):
            return
        payload = {
            "title": relation,
            "name": relation,
            "direction": "directed",
            "cardinality": "many_to_many",
            "axis": "",
            "source_types": [],
            "target_types": [],
            "condition": "",
            "description": description,
        }
        api.create_document(
            self.store_path, "RelationTypeDoc", self.root / RELATION_TYPES_DIR / f"{relation}.md", payload,
            name=type_name, pythonpath=self.pythonpath, actor=self.actor,
        )
        report.relation_types_added.append(relation)
        existing[("RelationTypeDoc", type_name)] = None

    def delete(self, existing: dict, report: SyncReport, model: str, name: str) -> None:
        import sldb.api as api

        api.delete_document(self.store_path, str(existing[(model, name)].path), self.pythonpath, actor=self.actor)
        report.deleted.append(f"{model}:{name}")

    def finish(self, report: SyncReport) -> SyncReport:
        import sldb.api as api

        api.rebuild_edges(self.store_path, self.pythonpath)
        report.edge_errors = list(api.check_edges(self.store_path).errors)
        return report


class NotationSync(_StoreWriter):
    """Escribe una notacion (NotationDoc, GlyphDoc, LinkDoc) en un store."""

    def sync(self, name_or_path: str | Path, *, finish: bool = True) -> SyncReport:
        import sldb.api as api

        notation = load_notation(name_or_path)
        report = SyncReport(spec_id=notation.name, notation=notation_ref(notation.name))
        self.prepare()
        existing = self.existing_documents()
        out = self.root / NOTATIONS_DIR / notation.name

        # aplicabilidad: los modelos que nombra tienen que estar registrados en el store
        for model in notation.models:
            try:
                api.load_registered_model(self.store_path, model, self.pythonpath)
            except Exception:
                report.unresolved.append(f"notation {notation.name}: model '{model}' is not registered in the store")

        # las relaciones que nombra son vocabulario del store
        for relation in notation.relations:
            self.ensure_relation_type(existing, report, relation, f"Relacion `{relation}` declarada por la notacion `{notation.name}` de spec2viz.")

        current: set[tuple[str, str]] = set()
        for glyph in notation.glyphs:
            name = f"{notation.name}.{glyph.id}"
            default_form = f'(where {glyph.model} "{glyph.where}")' if glyph.where else f"(model {glyph.model})"
            payload = {
                "id": name,
                "title": glyph.title or glyph.id,
                "notation": notation_ref(notation.name),
                "model": glyph.model,
                "where": glyph.where,
                "shape": glyph.shape,
                "label": glyph.label,
                "label_style": glyph.label_style,
                "keyword": glyph.keyword,
                "compartments": list(glyph.compartments),
                "function": glyph.function,
                "form": glyph.form or default_form,
                "description": glyph.description,
            }
            self.upsert(existing, report, "GlyphDoc", name, out / "glyphs" / f"{glyph.id}.md", payload)
            current.add(("GlyphDoc", name))

        for link in notation.links:
            name = f"{notation.name}.{link.id}"
            default_form = f"(model {link.model})" if link.model else f"(relation {link.relation})"
            payload = {
                "id": name,
                "title": link.title or link.id,
                "notation": notation_ref(notation.name),
                "relation": link.relation,
                "relation_type": f"RelationTypeDoc:reltype-{link.relation}",
                "model": link.model,
                "draw": link.draw,
                "line": link.line,
                "source_end": link.source_end,
                "target_end": link.target_end,
                "label": link.label,
                "ends": {k: e.model_dump() for k, e in link.ends.items()},
                "form": link.form or default_form,
                "description": link.description,
            }
            self.upsert(existing, report, "LinkDoc", name, out / "links" / f"{link.id}.md", payload)
            current.add(("LinkDoc", name))

        payload = {
            "id": notation.name,
            "title": notation.title or notation.name,
            "name": notation.name,
            "diagram_type": notation.diagram_type,
            "level": notation.level,
            "projection": notation.projection,
            "layout": dict(notation.layout),
            "markers": [m.model_dump() for m in notation.markers],
            "glyphs": [glyph_ref(notation.name, g.id) for g in notation.glyphs],
            "links": [link_ref(notation.name, l.id) for l in notation.links],
            "description": notation.description,
        }
        self.upsert(existing, report, "NotationDoc", notation.name, out / "notation.md", payload)

        prefix = f"{notation.name}."
        for (model, name) in list(existing):
            if model in ("GlyphDoc", "LinkDoc") and name.startswith(prefix) and (model, name) not in current:
                self.delete(existing, report, model, name)

        return self.finish(report) if finish else report


class SpecSync(_StoreWriter):
    """Escribe un spec en un store. Una instancia por store; `sync` por spec."""

    def __init__(self, store_path: Path, pythonpath: str | None = None, out_dir: Path | None = None, actor: str = "spec2viz"):
        super().__init__(store_path, pythonpath, actor)
        self.out_dir = out_dir

    def sync(self, spec_path: Path, notation: str | Path | None = None, catalog: dict[str, str] | None = None) -> SyncReport:
        """Sincroniza el spec. `notation`: nombre builtin o ruta; None = la del tipo de
        diagrama (si tiene); `"none"` = sin notacion. `catalog`: `category`, `nav`, `summary`
        del catalogo (vistas.yml) que graph_ui usa para listar el spec."""
        import sldb.api as api
        from spec2viz.loader import load as load_spec

        spec_path = Path(spec_path).resolve()
        load_spec(spec_path)  # valida contra los modelos de spec2viz antes de tocar el store
        text = spec_path.read_text(encoding="utf-8")
        spec = yaml.safe_load(text) or {}
        spec_id = str(spec["id"])
        diagram_type = str(spec.get("type") or "")
        report = SyncReport(spec_id=spec_id)

        chosen = DEFAULT_NOTATIONS.get(diagram_type) if notation is None else notation
        notation_spec: NotationSpec | None = None
        if chosen and str(chosen) != "none":
            notation_spec = load_notation(chosen)
            if notation_spec.diagram_type != diagram_type:
                raise ValueError(
                    f"notation '{notation_spec.name}' draws `{notation_spec.diagram_type}` specs, and `{spec_id}` is a `{diagram_type}` spec"
                )

        self.prepare()
        if notation_spec is not None:
            sub = NotationSync(self.store_path, self.pythonpath, self.actor).sync(chosen, finish=False)
            for attr in ("created", "updated", "deleted", "relation_types_added", "unresolved"):
                getattr(report, attr).extend(getattr(sub, attr))
            report.notation = sub.notation

        root = self.root
        out = (self.out_dir or spec_path.parent / "sldb" / spec_id).resolve()
        existing = self.existing_documents()

        elements = spec_elements(spec)
        edges = spec_edges(spec)

        # tipos de relacion que el spec usa y el store no conoce
        for relation in sorted({e["relation"] for e in edges}):
            self.ensure_relation_type(existing, report, relation, f"Relacion `{relation}` declarada por las aristas del spec `{spec_id}` de spec2viz.")

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
                "collection": el["collection"],
                "refs": el["refs"],
                "atom_refs": [f"AtomDoc:{a}" for a in el["atoms"]],
                "contains": [node_ref(spec_id, c) for c in el["contains"]],
                "data": el["data"],
                "description": el["description"],
            }
            self.upsert(existing, report, "SpecNodeDoc", name, out / "nodes" / f"{name}.md", payload)
            current.add(("SpecNodeDoc", name))

        # el spec
        try:
            rel_spec_path = str(spec_path.relative_to(root))
        except ValueError:
            rel_spec_path = str(spec_path)
        spec_payload = {
            "id": spec_id,
            "title": str(spec.get("title") or spec_id),
            "diagram_type": diagram_type,
            "version": str(spec.get("version") or ""),
            "spec_path": rel_spec_path,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "notation": report.notation,
            "category": str((catalog or {}).get("category") or ""),
            "nav": str((catalog or {}).get("nav") or ""),
            "summary": str((catalog or {}).get("summary") or ""),
            "nodes": [node_ref(spec_id, el["id"]) for el in elements],
            "description": str((spec.get("metadata") or {}).get("description") or ""),
        }
        self.upsert(existing, report, "SpecDoc", spec_id, out / f"{spec_id}.md", spec_payload)

        # aristas
        for index, edge in enumerate(edges, start=1):
            name = edge_name(spec_id, index, len(edges), edge)
            payload = {
                "title": f"{edge['from']} {edge['relation']} {edge['to']}",
                "source_id": node_ref(spec_id, edge["from"]),
                "target_id": node_ref(spec_id, edge["to"]),
                "relation_type": edge["relation"],
                "condition": edge.get("condition", ""),
                "notes": edge["label"],
            }
            self.upsert(existing, report, "RelationDoc", name, out / "edges" / f"{name}.md", payload)
            current.add(("RelationDoc", name))

        # lo que quedo de una sincronizacion anterior y ya no esta en el spec
        prefix = f"{spec_id}."
        for (model, name) in list(existing):
            if model in ("SpecNodeDoc", "RelationDoc") and name.startswith(prefix) and (model, name) not in current:
                self.delete(existing, report, model, name)

        # refs y atoms que no existen: aristas de schema, el indice no las reporta
        for el in elements:
            for ref in [*el["refs"], *(f"AtomDoc:{a}" for a in el["atoms"])]:
                if not api.doc_exists(self.store_path, to_slash_ref(ref)):
                    report.unresolved.append(f"{spec_id}.{el['id']}: '{ref}' no existe en el store")

        return self.finish(report)


def catalog_entries(config: Path) -> list[dict[str, Any]]:
    """Las entradas de un `vistas.yml`: por cada spec listado, su ruta y sus metadatos de catalogo."""
    config = Path(config).resolve()
    raw = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
    base = config.parent
    out: list[dict[str, Any]] = []
    for vista in raw.get("vistas") or []:
        if not isinstance(vista, dict):
            continue
        for spec in vista.get("specs") or []:
            path = Path(str(spec))
            if not path.is_absolute():
                path = (base / path).resolve() if (base / path).exists() else (base.parent.parent / path).resolve()
            out.append({
                "spec": path,
                "vista": str(vista.get("id") or ""),
                "catalog": {
                    "category": str(vista.get("category") or ""),
                    "nav": str(vista.get("nav") or ""),
                    "summary": str(vista.get("desc") or vista.get("title") or ""),
                },
            })
    return out


def sync_catalog(sync: "SpecSync", config: Path) -> list[SyncReport]:
    """Sincroniza cada spec de un `vistas.yml` con su notacion y sus metadatos de catalogo."""
    return [sync.sync(entry["spec"], catalog=entry["catalog"]) for entry in catalog_entries(config)]


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
    if report.notation:
        line += f", notation {report.notation}"
    line += ")"
    for problem in report.problems:
        line += f"\n  ! {problem}"
    return line


def format_notation_report(report: SyncReport) -> str:
    """Una linea por notacion, con lo que paso."""
    glyphs = sum(1 for d in [*report.created, *report.updated] if d.startswith("GlyphDoc:"))
    links = sum(1 for d in [*report.created, *report.updated] if d.startswith("LinkDoc:"))
    line = (
        f"Synced notation {report.spec_id}: {glyphs} glyphs, {links} links "
        f"({len(report.created)} created, {len(report.updated)} updated, {len(report.deleted)} deleted"
    )
    if report.relation_types_added:
        line += f", relation types added: {', '.join(report.relation_types_added)}"
    line += ")"
    for problem in report.problems:
        line += f"\n  ! {problem}"
    return line


__all__ = [
    "SpecSync", "NotationSync", "SyncReport", "find_store", "format_report", "format_notation_report",
    "spec_edges", "spec_elements", "edge_name", "stage_id", "relation_token", "node_ref", "to_slash_ref",
    "catalog_entries", "sync_catalog",
]


if __name__ == "__main__":  # pragma: no cover
    print("Use `spec2viz diagram sync`.", file=sys.stderr)
