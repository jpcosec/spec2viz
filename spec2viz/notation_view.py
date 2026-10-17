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
- §5 un `RelationDoc` casa con el link cuya `relation` es su `relation_type`; una relacion sin
  link no entra. `SpecNodeDoc.contains` (la fuente canonica, de la que el indice deriva las
  aristas `contains`) casa con el link `contains`.
- §6 una marca casa como un glifo y se lista en el nodo.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

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
        "title": payload.get("title", ""),
        "kind": payload.get("kind", ""),
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


def _link_view(source: str, target: str, link: dict, relation_payload: dict[str, Any] | None, relation_doc: str | None) -> dict[str, Any]:
    lp = link["payload"]
    return {
        "source": source,
        "target": target,
        "relation": lp["relation"],
        "link": link["ref"],
        "doc": relation_doc,
        "draw": lp.get("draw", "line"),
        "line": lp.get("line", "solid"),
        "source_end": lp.get("source_end", "none"),
        "target_end": lp.get("target_end", "open-arrow"),
        "label": render_template(lp.get("label") or "", relation_payload or {}),
    }


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
    by_relation = {l["payload"]["relation"]: l for l in links}
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
    for ref, doc in docs.items():
        if doc["model"] != "RelationDoc":
            continue
        rp = doc["payload"]
        source, target = rp.get("source_id"), rp.get("target_id")
        if source not in in_view or target not in in_view:
            continue
        link = by_relation.get(rp.get("relation_type"))
        if link is None:
            skipped.append(f"{ref}: relation '{rp.get('relation_type')}' has no link in {notation_ref}")
            continue
        out_links.append(_link_view(source, target, link, rp, ref))

    return {
        "spec": spec_ref,
        "title": sp.get("title", ""),
        "diagram_type": sp.get("diagram_type", ""),
        "notation": notation_ref,
        "level": np_.get("level", "types"),
        "layout": dict(np_.get("layout") or {"kind": "graph"}),
        "nodes": nodes,
        "links": out_links,
        "skipped": skipped,
    }


__all__ = ["resolve_view", "ViewError", "flatten", "lookup", "render_template", "matches"]
