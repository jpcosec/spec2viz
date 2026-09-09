"""UML syntax backends for the shared, structured ClassIR."""
from spec2viz.ir import ClassIR

VISIBILITY = {"public": "+", "private": "-", "protected": "#", "package": "~"}
MERMAID_RELATION = {
    "inheritance": "--|>", "realization": "..|>", "composition": "*--",
    "aggregation": "o--", "association": "-->", "dependency": "..>",
}
PLANTUML_RELATION = {**MERMAID_RELATION, "inheritance": "--|>", "realization": "..|>"}


def _mermaid_type(value: str) -> str:
    return value.replace("<", "~").replace(">", "~")


def _mermaid_label(value: str) -> str:
    return value.replace("&", "#amp;").replace("<", "#lt;").replace(">", "#gt;")


def _relation(edge, arrows, escape=lambda value: value):
    source = edge.from_
    target = edge.to
    if edge.from_multiplicity:
        source += f' "{edge.from_multiplicity}"'
    if edge.to_multiplicity:
        target = f'"{edge.to_multiplicity}" ' + target
    line = f'{source} {arrows[edge.relation]} {target}'
    if edge.label:
        line += f' : {escape(edge.label)}'
    return line


def render_mermaid_class(ir: ClassIR) -> str:
    lines = ["classDiagram", f"    direction {ir.direction}"]
    for node in ir.classes:
        lines.append(f'    class {node.id}["{_mermaid_label(node.label)}"]')
        lines.append(f'    class {node.id} {{')
        if node.kind != "class":
            annotation = "enumeration" if node.kind == "enum" else node.kind
            lines.append(f'        <<{annotation}>>')
        for attribute in node.attributes:
            modifier = "$" if attribute.static else ""
            lines.append(f'        {VISIBILITY[attribute.visibility]}{_mermaid_type(attribute.type)} {attribute.name}{modifier}')
        for method in node.methods:
            params = ", ".join(f'{p.name}: {_mermaid_type(p.type)}' for p in method.parameters)
            modifier = "$" if method.static else "*" if method.abstract else ""
            lines.append(f'        {VISIBILITY[method.visibility]}{method.name}({params}){modifier} {_mermaid_type(method.returns)}')
        lines.append('    }')
    lines.extend('    ' + _relation(edge, MERMAID_RELATION, _mermaid_label) for edge in ir.relations)
    return '\n'.join(lines)


def render_plantuml_class(ir: ClassIR) -> str:
    lines = ["@startuml", "skinparam classAttributeIconSize 0"]
    if ir.direction == "LR":
        lines.append("left to right direction")
    for node in ir.classes:
        keyword = {"interface": "interface", "protocol": "interface", "abstract": "abstract class", "enum": "enum"}.get(node.kind, "class")
        stereotype = f' <<{node.kind}>>' if node.kind in {"record", "protocol"} else ""
        lines.append(f'{keyword} "{node.label}" as {node.id}{stereotype} {{')
        for attribute in node.attributes:
            modifier = "{static} " if attribute.static else ""
            lines.append(f'    {modifier}{VISIBILITY[attribute.visibility]}{attribute.name}: {attribute.type}')
        for method in node.methods:
            modifier = "{static} " if method.static else "{abstract} " if method.abstract else ""
            params = ", ".join(f'{p.name}: {p.type}' for p in method.parameters)
            lines.append(f'    {modifier}{VISIBILITY[method.visibility]}{method.name}({params}): {method.returns}')
        lines.append('}')
    lines.extend(_relation(edge, PLANTUML_RELATION) for edge in ir.relations)
    lines.append("@enduml")
    return '\n'.join(lines)
