"""UML syntax backends for the shared, structured ClassIR."""
import re

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


def _package_styles(ir: ClassIR) -> list[tuple[str, dict, list[str]]]:
    """(kind, estilo resuelto, clases) por kind de paquete con `style.kinds` neutral: cada clase
    toma el estilo de su paquete mas interno que lo tenga (la misma `resolve_style`)."""
    from spec2viz.styling import resolve_style

    styled = {k: {p: v[p] for p in ("fill", "stroke") if v.get(p)} for k, v in ir.style_kinds.items() if isinstance(v, dict)}
    kind_of = {p.id: p.kind for p in ir.packages}
    members: dict[str, list[str]] = {}
    for node in ir.classes:
        owner = ir.package_of(node.id)
        if owner is None:
            continue
        for pid in reversed(ir.package_path(owner)):
            if styled.get(kind_of[pid]):
                members.setdefault(kind_of[pid], []).append(node.id)
                break
    return [(k, resolve_style(None, k, {k: styled[k]}, None), ids) for k, ids in members.items()]


def _mermaid_namespace(label: str) -> str:
    """Nombre de namespace de mermaid: letras, digitos y `_`."""
    return re.sub(r"[^0-9A-Za-z_]+", "_", label).strip("_") or "package"


def _mermaid_class_lines(node, indent: str) -> list[str]:
    lines = [f'{indent}class {node.id}["{_mermaid_label(node.label)}"]', f'{indent}class {node.id} {{']
    if node.kind != "class":
        annotation = "enumeration" if node.kind == "enum" else node.kind
        lines.append(f'{indent}    <<{annotation}>>')
    for attribute in node.attributes:
        modifier = "$" if attribute.static else ""
        lines.append(f'{indent}    {VISIBILITY[attribute.visibility]}{_mermaid_type(attribute.type)} {attribute.name}{modifier}')
    for method in node.methods:
        params = ", ".join(f'{p.name}: {_mermaid_type(p.type)}' for p in method.parameters)
        modifier = "$" if method.static else "*" if method.abstract else ""
        lines.append(f'{indent}    {VISIBILITY[method.visibility]}{method.name}({params}){modifier} {_mermaid_type(method.returns)}')
    lines.append(f'{indent}}}')
    return lines


def render_mermaid_class(ir: ClassIR) -> str:
    lines = ["classDiagram", f"    direction {ir.direction}"]
    by_package: dict[str | None, list] = {}
    for node in ir.classes:
        by_package.setdefault(ir.package_of(node.id), []).append(node)
    for node in by_package.get(None, []):
        lines.extend(_mermaid_class_lines(node, "    "))
    # mermaid no anida `namespace`: cada paquete con clases propias es un namespace con el nombre
    # de su ruta (`Dominio.Facturacion`); PlantUML y graph_ui anidan de verdad
    labels = {p.id: p.label for p in ir.packages}
    for package in ir.packages:
        if package.id not in by_package:
            continue
        name = ".".join(_mermaid_namespace(labels[pid]) for pid in ir.package_path(package.id))
        lines.append(f"    namespace {name} {{")
        for node in by_package[package.id]:
            lines.extend(_mermaid_class_lines(node, "        "))
        lines.append("    }")
    lines.extend('    ' + _relation(edge, MERMAID_RELATION, _mermaid_label) for edge in ir.relations)
    for index, (kind, style, ids) in enumerate(_package_styles(ir)):
        parts = [f"{prop}:{style[prop]['light']}" for prop in ("fill", "stroke") if prop in style]
        lines.append(f"    classDef pkg{index} {','.join(parts)}")
        lines.append(f'    cssClass "{",".join(ids)}" pkg{index}')
    return '\n'.join(lines)


def _plantuml_class_lines(node, indent: str) -> list[str]:
    keyword = {"interface": "interface", "protocol": "interface", "abstract": "abstract class", "enum": "enum"}.get(node.kind, "class")
    stereotype = f' <<{node.kind}>>' if node.kind in {"record", "protocol"} else ""
    lines = [f'{indent}{keyword} "{node.label}" as {node.id}{stereotype} {{']
    for attribute in node.attributes:
        modifier = "{static} " if attribute.static else ""
        lines.append(f'{indent}    {modifier}{VISIBILITY[attribute.visibility]}{attribute.name}: {attribute.type}')
    for method in node.methods:
        modifier = "{static} " if method.static else "{abstract} " if method.abstract else ""
        params = ", ".join(f'{p.name}: {p.type}' for p in method.parameters)
        lines.append(f'{indent}    {modifier}{VISIBILITY[method.visibility]}{method.name}({params}): {method.returns}')
    lines.append(f'{indent}}}')
    return lines


def render_plantuml_class(ir: ClassIR) -> str:
    from spec2viz.styling import resolve_style

    lines = ["@startuml", "skinparam classAttributeIconSize 0"]
    if ir.direction == "LR":
        lines.append("left to right direction")
    by_id = {node.id: node for node in ir.classes}
    packages = {p.id: p for p in ir.packages}
    nested = {ref for p in ir.packages for ref in p.contains}
    styled = {k: {q: v[q] for q in ("fill", "stroke") if v.get(q)} for k, v in ir.style_kinds.items() if isinstance(v, dict)}

    def emit_package(package, indent: str) -> None:
        # paquete UML anidado; el relleno (tema claro) de su kind si `style.kinds` lo da
        style = resolve_style(None, package.kind, {package.kind: styled[package.kind]}, None) if styled.get(package.kind) else {}
        color = f" {style['fill']['light']}" if "fill" in style else ""
        lines.append(f'{indent}package "{package.label}" as {package.id}{color} {{')
        for ref in package.contains:
            if ref in packages:
                emit_package(packages[ref], indent + "    ")
            elif ref in by_id:
                lines.extend(_plantuml_class_lines(by_id[ref], indent + "    "))
        lines.append(f"{indent}}}")

    for package in ir.packages:
        if package.id not in nested:
            emit_package(package, "")
    for node in ir.classes:
        if ir.package_of(node.id) is None:
            lines.extend(_plantuml_class_lines(node, ""))
    lines.extend(_relation(edge, PLANTUML_RELATION) for edge in ir.relations)
    lines.append("@enduml")
    return '\n'.join(lines)
