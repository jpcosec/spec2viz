"""Compila un grafo sldb (edge index) en un spec de diagrama `component`.

Dos fuentes producen la misma forma intermedia `(nodes, edges)`:

- `load_node_link(path)`: el JSON node-link que escribe `sldb graph snapshot save`.
- `load_store_index(store)`: el edge index de un store, leido via `sldb.api` (import
  perezoso: la ruta JSON funciona sin sldb instalado).

`component_spec_from_graph` filtra por tipo de nodo, modelo y relacion, traduce los
ids `sldb://...` a identificadores seguros y devuelve un dict listo para `yaml.dump`
que valida como `ComponentDiagram`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

# Nodos del grafo: id -> tipo de nodo tal como lo entrega la fuente.
GraphNodes = dict[str, str]
# Aristas del grafo: (source, target, relation).
GraphEdges = list[tuple[str, str, str]]

SLDB_SCHEME = "sldb://"

# Tipos de nodo que se conservan si el usuario no indica `--node-type`.
DEFAULT_NODE_TYPES: tuple[str, ...] = ("document", "model")

# Relaciones estructurales que solo agregan ruido en un diagrama de componentes.
DEFAULT_EXCLUDED_RELATIONS: tuple[str, ...] = (
    "has_section",
    "tagged_as",
    "has_document",
    "has_field",
    "has_model",
    "names",
    "semantic_parent",
    "semantic_equivalent",
    "applies_to_source",
    "applies_to_target",
)

# Relacion que se vuelve anidamiento (`contains`) en vez de arista.
CONTAINS_RELATION = "contains"

# Palabras que mermaid interpreta como sintaxis si aparecen como id de nodo.
_RESERVED_IDS = frozenset({"end", "graph", "subgraph", "style", "class", "click", "classDef", "linkStyle", "direction"})


# ── Loaders ──────────────────────────────────────────────────────────────────


def _node_identity(node: dict) -> tuple[str | None, str | None]:
    """Extrae (id, tipo) de un nodo node-link; acepta `id`/`type` o `schema.identity`."""
    identity = (node.get("schema") or {}).get("identity") or {}
    node_id = node.get("id") or identity.get("node_id")
    node_type = node.get("type") or identity.get("node_type")
    return node_id, node_type


def load_node_link(path: str | Path) -> tuple[GraphNodes, GraphEdges]:
    """Lee un JSON node-link (`sldb graph snapshot save --output x.json`)."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    nodes: GraphNodes = {}
    for node in raw.get("nodes") or []:
        node_id, node_type = _node_identity(node)
        if node_id:
            nodes[str(node_id)] = str(node_type or "")
    edges: GraphEdges = [
        (str(link["source"]), str(link["target"]), str(link.get("relation") or ""))
        for link in raw.get("links") or []
        if link.get("source") and link.get("target")
    ]
    return nodes, edges


def load_store_index(store_path: str | Path) -> tuple[GraphNodes, GraphEdges]:
    """Lee el edge index de un store via la API publica de sldb (import perezoso)."""
    from sldb.api import load_edge_index  # solo la superficie publica

    index = load_edge_index(store_path)
    nodes: GraphNodes = {str(nid): str(rec.node_type or "") for nid, rec in index.nodes.items()}
    edges: GraphEdges = [(str(e.source), str(e.target), str(e.relation or "")) for e in index.edges]
    return nodes, edges


# ── Normalizacion de ids ─────────────────────────────────────────────────────


def _normalize_type(node_type: str) -> str:
    """`sldb_document` -> `document`; los demas tipos quedan igual."""
    return node_type[5:] if node_type.startswith("sldb_") else node_type


def node_kind(node_id: str, node_type: str) -> str:
    """Tipo canonico del nodo: el segmento tras `sldb://` (document, model, ...).

    Cae al `node_type` de la fuente (sin el prefijo `sldb_`) cuando el id no sigue
    el esquema; el store index tipa los documentos con el nombre del modelo, por eso
    el id manda.
    """
    if node_id.startswith(SLDB_SCHEME):
        head = node_id[len(SLDB_SCHEME):].split("/", 1)[0]
        if head:
            return head
    return _normalize_type(node_type)


def _id_tail(node_id: str) -> str:
    """Parte del id despues de `sldb://<kind>/` (o el id completo si no aplica)."""
    if node_id.startswith(SLDB_SCHEME):
        rest = node_id[len(SLDB_SCHEME):]
        return rest.split("/", 1)[1] if "/" in rest else rest
    return node_id


def document_ref(node_id: str, node_type: str = "") -> tuple[str | None, str | None]:
    """(modelo, nombre) de un nodo documento `sldb://document/[store:]Model:name`.

    Devuelve `(None, None)` si el nodo no es un documento. El modelo cae al
    `node_type` cuando el id no trae la parte `Model:` (store index tipa asi).
    """
    if node_kind(node_id, node_type) != "document":
        return None, None
    tail = _id_tail(node_id)
    parts = tail.split(":")
    if len(parts) >= 3:
        return parts[-2], parts[-1]
    if len(parts) == 2:
        return parts[0], parts[1]
    model = _normalize_type(node_type) if node_type and node_type != "document" else None
    return model, tail


def sanitize_id(node_id: str) -> str:
    """Identificador seguro `[A-Za-z0-9_]` a partir de un id `sldb://...`."""
    text = node_id[len(SLDB_SCHEME):] if node_id.startswith(SLDB_SCHEME) else node_id
    text = re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_")
    if not text:
        text = "node"
    if text[0].isdigit() or text in _RESERVED_IDS:
        text = f"n_{text}"
    return text


def _unique_ids(node_ids: Iterable[str]) -> dict[str, str]:
    """Mapa id original -> id seguro, unico dentro del spec (sufijo `_2`, `_3`, ...)."""
    mapping: dict[str, str] = {}
    taken: set[str] = set()
    for node_id in node_ids:
        base = sanitize_id(node_id)
        candidate = base
        n = 1
        while candidate in taken:
            n += 1
            candidate = f"{base}_{n}"
        taken.add(candidate)
        mapping[node_id] = candidate
    return mapping


def _label_and_kind(node_id: str, node_type: str) -> tuple[str, str]:
    """Etiqueta y `kind` del nodo: documentos -> (name, Model); modelos -> (Model, model)."""
    kind = node_kind(node_id, node_type)
    if kind == "document":
        model, name = document_ref(node_id, node_type)
        return name or _id_tail(node_id), model or "document"
    if kind == "model":
        return _id_tail(node_id), "model"
    return _id_tail(node_id) or node_id, kind


# ── Compilacion ──────────────────────────────────────────────────────────────


def _describe(source: str, node_types, models, relations, exclude_relations, drop_isolated) -> str:
    parts = [f"Generado desde {source}", f"node_types={','.join(node_types)}"]
    if models:
        parts.append(f"models={','.join(models)}")
    if relations:
        parts.append(f"relations={','.join(relations)}")
    else:
        parts.append(f"exclude_relations={','.join(exclude_relations) or '-'}")
    if drop_isolated:
        parts.append("drop_isolated")
    return "; ".join(parts)


def component_spec_from_graph(
    nodes: GraphNodes,
    edges: GraphEdges,
    *,
    node_types: Iterable[str] | None = None,
    models: Iterable[str] | None = None,
    relations: Iterable[str] | None = None,
    exclude_relations: Iterable[str] | None = None,
    drop_isolated: bool = False,
    spec_id: str = "sldb-graph",
    title: str = "sldb graph",
    source: str = "graph",
) -> dict:
    """Compila `(nodes, edges)` en un dict de spec `component` listo para serializar.

    - `node_types`: tipos canonicos a conservar (`document`, `model`, ...); vacio ->
      `DEFAULT_NODE_TYPES`. Se acepta el prefijo `sldb_`.
    - `models`: solo documentos de estos modelos (los nodos no documento no se tocan).
    - `relations`: lista blanca de relaciones; si se da, anula `exclude_relations`.
    - `exclude_relations`: relaciones a omitir; `None` -> `DEFAULT_EXCLUDED_RELATIONS`.
    - `drop_isolated`: descarta nodos sin aristas ni anidamiento tras filtrar.
    - La relacion `contains` se vuelve `contains: [...]` en el nodo origen.
    """
    wanted_types = tuple(_normalize_type(t) for t in (node_types or ())) or DEFAULT_NODE_TYPES
    wanted_models = tuple(models or ())
    include = tuple(relations or ())
    exclude = DEFAULT_EXCLUDED_RELATIONS if exclude_relations is None else tuple(exclude_relations)

    # 1. Nodos que pasan los filtros de tipo y modelo.
    kept: dict[str, str] = {}
    for node_id, node_type in nodes.items():
        kind = node_kind(node_id, node_type)
        if kind not in wanted_types:
            continue
        if wanted_models and kind == "document":
            model, _ = document_ref(node_id, node_type)
            if model not in wanted_models:
                continue
        kept[node_id] = node_type

    # 2. Aristas con ambos extremos vivos y relacion admitida.
    def relation_ok(relation: str) -> bool:
        return relation in include if include else relation not in exclude

    live_edges: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for source_id, target_id, relation in edges:
        if source_id not in kept or target_id not in kept or not relation_ok(relation):
            continue
        key = (source_id, target_id, relation)
        if key in seen:
            continue
        seen.add(key)
        live_edges.append(key)

    # 3. Nodos aislados.
    if drop_isolated:
        connected = {e[0] for e in live_edges} | {e[1] for e in live_edges}
        kept = {nid: t for nid, t in kept.items() if nid in connected}

    # 4. Ids seguros y nodos del spec.
    ids = _unique_ids(kept)
    spec_nodes: dict[str, dict] = {}
    for node_id, node_type in kept.items():
        label, kind = _label_and_kind(node_id, node_type)
        spec_nodes[ids[node_id]] = {"label": label, "kind": kind}

    # 5. `contains` anida; el resto son aristas.
    spec_edges: list[dict] = []
    for source_id, target_id, relation in live_edges:
        if relation == CONTAINS_RELATION:
            contains = spec_nodes[ids[source_id]].setdefault("contains", [])
            if ids[target_id] not in contains:
                contains.append(ids[target_id])
        else:
            spec_edges.append({"from": ids[source_id], "to": ids[target_id], "relation": relation})

    return {
        "id": spec_id,
        "title": title,
        "type": "component",
        "version": "1.0",
        "metadata": {
            "description": _describe(source, wanted_types, wanted_models, include, exclude, drop_isolated),
        },
        "data": {"nodes": spec_nodes, "edges": spec_edges},
    }


__all__ = [
    "DEFAULT_NODE_TYPES",
    "DEFAULT_EXCLUDED_RELATIONS",
    "CONTAINS_RELATION",
    "load_node_link",
    "load_store_index",
    "node_kind",
    "document_ref",
    "sanitize_id",
    "component_spec_from_graph",
]
