"""Mermaid desde una vista resuelta (`notation_view.resolve_view` / `resolve_documents`).

Es la proyeccion estatica de lo mismo que graph_ui dibuja en vivo: la notacion ya eligio glifo,
forma, keyword, rotulo y compartimentos de cada nodo, el estilo ya esta resuelto con su
precedencia (glifo > style.kinds del spec > paleta) y cada link trae su trazo, terminales, rotulo
y color. Aqui solo se traduce a un `flowchart` de mermaid con layout ELK; nada se recalcula.

Cubre las vistas de layout `graph` (component, deployment, activity, clase, estado, reflection).
Las de `lanes` (secuencia) y `grid` (matriz) no son un grafo: `view_to_mermaid` lanza
`ValueError` y el catalogo usa su fuente renderizada.

Aproximaciones de forma (mermaid no tiene todas las de la notacion): `package` es `notch-rect`
(mermaid no tiene la carpeta con pestana), `note` es `doc`, `node-box`/`artifact`/`class-box` son
rectangulos, `stick-figure` es un estadio. Los iconos (Lucide) son para superficies que los
dibujan; mermaid no los muestra.
"""

from __future__ import annotations

import html
from typing import Any

from spec2viz.renderers.mermaid import FLOWCHART_CONFIG

# forma de la notacion -> nodo de mermaid; `{l}` es el rotulo ya escapado
_SHAPES = {
    "box": '["{l}"]', "node-box": '["{l}"]', "class-box": '["{l}"]', "boundary-box": '["{l}"]',
    "artifact": '["{l}"]', "row-header": '["{l}"]', "column-header": '["{l}"]',
    "rounded-box": '("{l}")', "rounded-container": '("{l}")',
    "diamond": '{{"{l}"}}',
    "cylinder": '[("{l}")]',
    "stick-figure": '(["{l}"])',
    "queue": '@{{ shape: h-cyl, label: "{l}" }}',
    "cloud": '@{{ shape: cloud, label: "{l}" }}',
    "package": '@{{ shape: notch-rect, label: "{l}" }}',
    "note": '@{{ shape: doc, label: "{l}" }}',
}
# formas sin rotulo (pseudonodos)
_BARE = {"filled-circle": "@{ shape: sm-circ }", "bullseye": "@{ shape: fr-circ }"}
_DIRECTIONS = {"TB": "TD", "TD": "TD", "BT": "BT", "LR": "LR", "RL": "RL"}


def _esc(text: Any) -> str:
    """Rotulo de mermaid con htmlLabels: HTML escapado, comillas como entidad de mermaid."""
    return html.escape(str(text), quote=False).replace('"', "#quot;")


def _item(value: Any) -> str:
    """Un elemento de compartimento: atributo `name: type`, metodo `name(params): returns` o texto."""
    if isinstance(value, dict):
        name = value.get("name", "")
        if "parameters" in value or "returns" in value:
            params = ", ".join(f"{p.get('name', '')}: {p.get('type', '')}" if isinstance(p, dict) else str(p) for p in value.get("parameters") or [])
            returns = value.get("returns")
            return f"{name}({params})" + (f": {returns}" if returns else "")
        return f"{name}: {value['type']}" if value.get("type") else str(name)
    return str(value)


def _label(node: dict[str, Any]) -> str:
    """keyword, rotulo y compartimentos del nodo, ya resueltos por la notacion."""
    lines = [_esc(node["keyword"])] if node.get("keyword") else []
    label = _esc(node.get("label", ""))
    if node.get("label_style") == "italic":
        label = f"<i>{label}</i>"
    elif node.get("label_style") == "bold":
        label = f"<b>{label}</b>"
    lines.append(label)
    for compartment in node.get("compartments") or []:
        items = [_esc(_item(v)) for v in compartment.get("items") or []]
        if items:
            lines.append("<hr/>" + "<br/>".join(items))
    return "<br/>".join(l for l in lines if l) or " "


def view_to_mermaid(view: dict[str, Any], theme: str = "dark", ink: str | None = None) -> str:
    """Un `flowchart` de mermaid (ELK) desde una vista resuelta de layout `graph`.

    `theme` elige el lado de cada color `{light, dark}`; `ink` es el color del texto sobre un
    relleno (por defecto el de la paleta default para ese tema).
    """
    layout = view.get("layout") or {}
    if layout.get("kind", "graph") != "graph":
        raise ValueError(f"layout {layout.get('kind')!r} is not a graph; view_to_mermaid draws graph layouts only")
    if ink is None:
        from spec2viz.styling import _builtin_default

        ink = _builtin_default()["ink"][theme]

    nodes = list(view.get("nodes") or [])
    ids = {node["doc"]: f"n{i}" for i, node in enumerate(nodes)}
    by_doc = {node["doc"]: node for node in nodes}
    nest = [l for l in view.get("links") or [] if l.get("draw") == "nest" and l["source"] in ids and l["target"] in ids]
    parent = {}
    for link in nest:
        parent.setdefault(link["target"], link["source"])
    children: dict[str, list[str]] = {}
    for child, owner in parent.items():
        children.setdefault(owner, []).append(child)

    lines = [*FLOWCHART_CONFIG.split("\n"), f"flowchart {_DIRECTIONS.get(str(layout.get('direction') or 'TB'), 'TD')}"]

    def emit(doc: str, indent: str) -> None:
        node = by_doc[doc]
        if doc in children:
            lines.append(f'{indent}subgraph {ids[doc]} ["{_label({**node, "compartments": []})}"]')
            for child in children[doc]:
                emit(child, indent + "    ")
            lines.append(f"{indent}end")
            return
        shape = node.get("shape", "")
        if shape in _BARE:
            lines.append(f"{indent}{ids[doc]}{_BARE[shape]}")
        else:
            lines.append(f"{indent}{ids[doc]}{_SHAPES.get(shape, _SHAPES['box']).format(l=_label(node))}")

    for node in nodes:
        if node["doc"] not in parent:
            emit(node["doc"], "    ")

    # marcas (el pseudoestado inicial de un statechart): un punto que apunta a su elemento
    for node in nodes:
        for index, marker in enumerate(node.get("markers") or []):
            mid = f"{ids[node['doc']]}m{index}"
            lines.append(f"    {mid}{_BARE.get(marker.get('shape', ''), '@{ shape: sm-circ }')}")
            lines.append(f"    {mid} --> {ids[node['doc']]}")

    link_styles: list[str] = []
    edge_index = sum(len(n.get("markers") or []) for n in nodes)
    for link in view.get("links") or []:
        if link.get("draw") == "nest" or link["source"] not in ids or link["target"] not in ids:
            continue
        dashed = link.get("line") in ("dashed", "dotted")
        headless = link.get("target_end", "open-arrow") == "none"
        arrow = ("-.-" if headless else "-.->") if dashed else ("---" if headless else "-->")
        text = " ".join(t for t in (link.get("source_label"), link.get("label"), link.get("target_label")) if t)
        label = f'|"{_esc(text)}"|' if text else ""
        lines.append(f"    {ids[link['source']]} {arrow}{label} {ids[link['target']]}")
        if link.get("color"):
            link_styles.append(f"    linkStyle {edge_index} stroke:{link['color'][theme]}")
        edge_index += 1
    lines.extend(link_styles)

    for node in nodes:
        style = node.get("style") or {}
        parts = [f"{prop}:{style[prop][theme]}" for prop in ("fill", "stroke") if prop in style]
        if parts:
            lines.append(f"    style {ids[node['doc']]} {','.join(parts)},color:{ink}")
    return "\n".join(lines)


__all__ = ["view_to_mermaid"]
