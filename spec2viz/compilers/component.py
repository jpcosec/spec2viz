from __future__ import annotations
from spec2viz.models.component import ComponentDiagram
from spec2viz.ir import ComponentIR, ComponentNode, ComponentEdge


class ComponentCompiler:
    def compile(self, diagram: ComponentDiagram) -> ComponentIR:
        nodes = [
            ComponentNode(
                id=nid,
                label=node.label or nid,
                kind=node.kind,
                contains=list(node.contains),
            )
            for nid, node in diagram.data.nodes.items()
        ]
        edges = [
            ComponentEdge(from_=e.from_, to=e.to, relation=e.relation, label=e.label)
            for e in diagram.data.edges
        ]
        style_kinds = {}
        if diagram.style is not None:
            style_kinds = dict(diagram.style.kinds)
        return ComponentIR(
            title=diagram.title,
            nodes=nodes,
            edges=edges,
            style_kinds=style_kinds,
        )
