from __future__ import annotations
from yaml_charts.models.component import ComponentDiagram
from yaml_charts.ir import ComponentIR, ComponentNode, ComponentEdge


class ComponentCompiler:
    def compile(self, diagram: ComponentDiagram) -> ComponentIR:
        nodes = [
            ComponentNode(id=nid, label=node.label or nid, kind=node.kind, contains=list(node.contains))
            for nid, node in diagram.data.nodes.items()
        ]
        edges = [
            ComponentEdge(from_=e.from_, to=e.to, relation=e.relation, label=e.label)
            for e in diagram.data.edges
        ]
        return ComponentIR(title=diagram.title, nodes=nodes, edges=edges)
