"""El unico interprete del contrato de notacion (`docs/notation-contract.md`).

`resolve_view(store, "SpecDoc:<id>")` lee del store el spec, sus nodos, sus aristas y su
notacion, y devuelve que glifo, marcas, rotulo y compartimentos le tocan a cada nodo y que
link le toca a cada relacion. Una superficie (graph_ui) sirve ese resultado y dibuja; no
reimplementa `where`, ni las plantillas, ni la prioridad de los glifos.

Reglas que aplica, numeradas como en el contrato:

- §2 la notacion es `SpecDoc.notation`; su `diagram_type` tiene que coincidir con el del spec.
- §3 entran los `SpecNodeDoc` de `SpecDoc.nodes` y los `RelationDoc` con ambos extremos en
  esa lista.
- §4 un glifo casa si `model` es el del documento y `where` (gramatica de `sldb find --where`)
  se cumple sobre el payload aplanado: el payload con las claves de `data` copiadas encima.
  Gana el primero en el orden de `NotationDoc.glyphs`. `compartments` son rutas con punto
  sobre el payload crudo (`data.attributes`). Un `{campo}` ausente en un rotulo queda vacio.
- §5 un `RelationDoc` casa con el link cuya `relation` es su `relation_type`, o con el link
  comodin `*` si lo hay; una relacion sin link no entra. `SpecNodeDoc.contains` (la fuente
  canonica, de la que el indice deriva las aristas `contains`) casa con el link `contains`.
  Los links salen en el orden del spec (`order`), que el nombre del `RelationDoc` conserva.
- §6 una marca casa como un glifo y se lista en el nodo.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from spec2viz.notation import ANY_RELATION

_PLACEHOLDER = re.compile(r"\{([A-Za-z0-9_.]+)\}")
_DOC_FIELDS = ("id", "title", "kind", "refs", "atom_refs", "contains", "description", "spec", "element")


class ViewError(ValueError):
    """El store no tiene lo que el contrato necesita (spec, notacion, glifos)."""


def flatten(payload: dict[str, Any]) -> dict[str, Any]:
    """El payload con las claves de `data` copiadas al nivel superior; `data` no pisa nada."""
    data = payload.get("data") or {}
    out = dict(payload)
    for key, value in (data.items() if isinstance(data, dict) else []):
        out.setdefault(key, value)
    return out


def lookup(payload: dict[str, Any], path: str) -> Any:
    """`a.b.c` sobre dicts anidados; None si falta algun tramo."""
    value: Any = payload
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def render_template(template: str, payload: dict[str, Any]) -> str:
    """`{campo}` -> el valor del payload aplanado (`{a.b}` con punto sobre el crudo); ausente -> vacio."""
    flat = flatten(payload)

    def sub(match: re.Match) -> str:
        key = match.group(1)
        value = flat.get(key) if "." not in key else lookup(payload, key)
        if value is None or isinstance(value, (dict, list)):
            return ""
        return str(value)

    return re.sub(r"[ \t]{2,}", " ", _PLACEHOLDER.sub(sub, template)).strip()


def matches(expression: str, payload: dict[str, Any]) -> bool:
    if not expression:
        return True
    from sldb.api import where_matches

    return where_matches(expression, flatten(payload))


def _docs(store: Path, pythonpath: str | None) -> dict[str, dict[str, Any]]:
    import sldb.api as api

    return {
        f"{doc.model_name}:{doc.name}": {"model": str(doc.model_name), "payload": dict(doc.payload or {})}
        for doc in api.load_runtime_documents(Path(store), pythonpath, include_linked=False)
    }


def _node_view(ref: str, payload: dict[str, Any], glyphs: list[dict], markers: list[dict]) -> dict[str, Any]:
    glyph = next((g for g in glyphs if g["payload"]["model"] == "SpecNodeDoc" and matches(g["payload"].get("where", ""), payload)), None)
    if glyph is None:
        raise ViewError(f"no glyph of the notation matches {ref} (the last glyph of a model must have no `where`)")
    gp = glyph["payload"]
    compartments = []
    for path in gp.get("compartments") or []:
        value = lookup(payload, path)
        if value in (None, [], {}, ""):
            continue
        compartments.append({"path": path, "items": value if isinstance(value, list) else [value]})
    return {
        "doc": ref,
        "element": payload.get("element", ""),
        "title": payload.get("title", ""),
        "kind": payload.get("kind", ""),
        "collection": payload.get("collection", ""),
        "data": dict(payload.get("data") or {}),
        "glyph": glyph["ref"],
        "shape": gp.get("shape", ""),
        "function": gp.get("function", ""),
        "label": render_template(gp.get("label") or "{title}", payload),
        "label_style": gp.get("label_style", ""),
        "keyword": gp.get("keyword", ""),
        "compartments": compartments,
        "markers": [{"id": m["id"], "shape": m["shape"]} for m in markers if m.get("model", "SpecNodeDoc") == "SpecNodeDoc" and matches(m.get("where", ""), payload)],
        "refs": list(payload.get("refs") or []) + list(payload.get("atom_refs") or []),
    }


_ORDER = re.compile(r"\.(\d+)-")


def link_order(relation_doc: str | None) -> int:
    """La posicion de la arista en el spec, del nombre `<spec>.<nn>-...`; 0 si no la lleva."""
    match = _ORDER.search(relation_doc or "")
    return int(match.group(1)) if match else 0


def _link_view(source: str, target: str, link: dict, relation_payload: dict[str, Any] | None, relation_doc: str | None) -> dict[str, Any]:
    lp = link["payload"]
    rp = relation_payload or {}
    attributes = dict(rp.get("attributes") or {})
    # las plantillas de un link leen el RelationDoc con sus `attributes` encima (como `data` en un nodo)
    templated = {**rp, "data": attributes}
    relation = lp["relation"] if lp["relation"] != ANY_RELATION else str(rp.get("relation_type") or "")
    return {
        "source": source,
        "target": target,
        "relation": relation,
        "link": link["ref"],
        "doc": relation_doc,
        "order": link_order(relation_doc),
        "condition": str(rp.get("condition") or ""),
        "data": attributes,
        "source_label": render_template(lp.get("source_label") or "", templated),
        "target_label": render_template(lp.get("target_label") or "", templated),
        "draw": lp.get("draw", "line"),
        "line": lp.get("line", "solid"),
        "source_end": lp.get("source_end", "none"),
        "target_end": lp.get("target_end", "open-arrow"),
        "label": render_template(lp.get("label") or "", templated),
    }


# operadores de fragmento UML; un `group` que empieza por uno de ellos lo declara como `kind`
FRAGMENT_KINDS = ("alt", "loop", "opt", "par", "break", "critical", "neg", "ref", "seq", "strict")


def fragment_kind(group: str) -> tuple[str, str]:
    """`(kind, label)` de un `group`: `"loop for each spec"` -> `("loop", "for each spec")`;
    sin operador delante, `("group", <el grupo entero>)`."""
    head, _, rest = group.strip().partition(" ")
    if head.lower() in FRAGMENT_KINDS:
        return head.lower(), rest.strip()
    return "group", group.strip()


def fragments_of(links: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Un fragmento por racha de links consecutivos (por `order`) con el mismo `data.group`."""
    out: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_group = ""
    for link in sorted((l for l in links if l.get("order")), key=lambda l: l["order"]):
        group = str(link.get("data", {}).get("group") or "")
        if group and current is not None and current_group == group:
            current["orders"].append(link["order"])
            continue
        current_group = group
        kind, label = fragment_kind(group)
        current = {"label": label, "kind": kind, "group": group, "orders": [link["order"]]} if group else None
        if current is not None:
            out.append(current)
    return out


def resolve_view(store: Path, spec_ref: str, pythonpath: str | None = None) -> dict[str, Any]:
    """La vista de un spec segun su notacion, lista para dibujar.

    Devuelve `{spec, notation, layout, level, nodes, links, skipped}`; `skipped` lista las
    relaciones del spec que la notacion no dibuja. `ViewError` si el spec no existe, no tiene
    notacion, o la notacion no casa con el tipo de diagrama.
    """
    if not spec_ref.startswith("SpecDoc:"):
        spec_ref = f"SpecDoc:{spec_ref}"
    docs = _docs(store, pythonpath)
    spec = docs.get(spec_ref)
    if spec is None:
        raise ViewError(f"{spec_ref} is not in the store")
    sp = spec["payload"]
    notation_ref = sp.get("notation") or ""
    if not notation_ref:
        raise ViewError(f"{spec_ref} has no notation; sync it with `spec2viz diagram sync --notation <name>`")
    notation = docs.get(notation_ref)
    if notation is None:
        raise ViewError(f"{spec_ref} points at {notation_ref}, which is not in the store")
    np_ = notation["payload"]
    if np_.get("diagram_type") != sp.get("diagram_type"):
        raise ViewError(f"{notation_ref} draws `{np_.get('diagram_type')}` specs and {spec_ref} is a `{sp.get('diagram_type')}` spec")

    glyphs = [{"ref": r, "payload": docs[r]["payload"]} for r in np_.get("glyphs") or [] if r in docs]
    links = [{"ref": r, "payload": docs[r]["payload"]} for r in np_.get("links") or [] if r in docs]
    if not glyphs:
        raise ViewError(f"{notation_ref} lists no glyph that is in the store")
    by_relation = {l["payload"]["relation"]: l for l in links if l["payload"]["relation"] != ANY_RELATION}
    wildcard = next((l for l in links if l["payload"]["relation"] == ANY_RELATION), None)
    markers = list(np_.get("markers") or [])

    node_refs = [r for r in sp.get("nodes") or [] if r in docs]
    nodes = [_node_view(r, docs[r]["payload"], glyphs, markers) for r in node_refs]
    in_view = set(node_refs)

    out_links: list[dict[str, Any]] = []
    skipped: list[str] = []
    contains_link = by_relation.get("contains")
    for ref in node_refs:
        for child in docs[ref]["payload"].get("contains") or []:
            if child in in_view:
                if contains_link is None:
                    skipped.append(f"{ref} contains {child}")
                else:
                    out_links.append(_link_view(ref, child, contains_link, None, None))
    relation_links: list[dict[str, Any]] = []
    for ref, doc in docs.items():
        if doc["model"] != "RelationDoc":
            continue
        rp = doc["payload"]
        source, target = rp.get("source_id"), rp.get("target_id")
        if source not in in_view or target not in in_view:
            continue
        link = by_relation.get(rp.get("relation_type")) or wildcard
        if link is None:
            skipped.append(f"{ref}: relation '{rp.get('relation_type')}' has no link in {notation_ref}")
            continue
        relation_links.append(_link_view(source, target, link, rp, ref))
    out_links.extend(sorted(relation_links, key=lambda l: (l["order"], l["doc"] or "")))

    return {
        "spec": spec_ref,
        "title": sp.get("title", ""),
        "diagram_type": sp.get("diagram_type", ""),
        "notation": notation_ref,
        "level": np_.get("level", "types"),
        "layout": dict(np_.get("layout") or {"kind": "graph"}),
        "nodes": nodes,
        "links": out_links,
        "fragments": fragments_of(out_links),
        "skipped": skipped,
    }


__all__ = ["resolve_view", "ViewError", "flatten", "lookup", "render_template", "matches", "link_order", "fragments_of", "fragment_kind", "FRAGMENT_KINDS"]
