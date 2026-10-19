from __future__ import annotations
from spec2viz.exceptions import EndpointKindError, StructureError, UnknownReferenceError, ValidationError
from spec2viz.models.base import BaseDiagram
from spec2viz.models.sequence   import SequenceDiagram
from spec2viz.models.state      import StateDiagram
from spec2viz.models.component  import ComponentDiagram
from spec2viz.models.activity   import ActivityDiagram
from spec2viz.models.deployment import DeploymentDiagram
from spec2viz.models.matrix     import MatrixDiagram, MatrixComponentModel
from spec2viz.models.class_diagram import ClassDiagram


def validate(diagram: BaseDiagram) -> None:
    _validate_style(diagram)
    match diagram:
        case ClassDiagram():      _validate_class(diagram)
        case ComponentDiagram():  _validate_component(diagram)
        case SequenceDiagram():   _validate_sequence(diagram)
        case StateDiagram():      _validate_state(diagram)
        case ActivityDiagram():   _validate_activity(diagram)
        case DeploymentDiagram(): _validate_deployment(diagram)
        case MatrixDiagram():     _validate_matrix(diagram)


def _validate_style(d: BaseDiagram) -> None:
    """`style.kinds` neutral (fill, stroke, icon): colores token de la paleta default o `#rrggbb`
    (`InvalidColorError`), iconos del set declarado (`UnknownIconError`). Las claves de un
    renderer (como `plantuml`) no se validan aqui."""
    if d.style is None or not d.style.kinds:
        return
    from spec2viz.exceptions import UnknownIconError
    from spec2viz.palette import resolve_color
    from spec2viz.styling import _builtin_default

    default = _builtin_default()
    for kind, entry in d.style.kinds.items():
        if not isinstance(entry, dict):
            continue
        for prop in ("fill", "stroke"):
            if entry.get(prop):
                resolve_color(str(entry[prop]), default["colors"], f"{d.id} style.kinds.{kind}.{prop}")
        if entry.get("icon") and str(entry["icon"]) not in default["icon_set"]["icons"]:
            raise UnknownIconError(f"{d.id} style.kinds.{kind}.icon {entry['icon']!r} is not in the {default['icon_set']['name']} icon set")


def _validate_class(d: ClassDiagram) -> None:
    classes = d.data.classes
    parents: dict[str, list[str]] = {ident: [] for ident in classes}
    for ident, definition in classes.items():
        names = [a.name for a in definition.attributes]
        if len(names) != len(set(names)):
            raise ValidationError(f"Duplicate attribute in class '{ident}' in {d.id}")
        signatures = set()
        for method in definition.methods:
            parameters = [p.name for p in method.parameters]
            if len(parameters) != len(set(parameters)):
                raise ValidationError(f"Duplicate parameter in '{ident}.{method.name}' in {d.id}")
            signature = (method.name, tuple(p.type for p in method.parameters))
            if signature in signatures:
                raise ValidationError(f"Duplicate method signature in '{ident}.{method.name}' in {d.id}")
            signatures.add(signature)
            if method.static and method.abstract:
                raise ValidationError(f"Method '{ident}.{method.name}' cannot be both static and abstract in {d.id}")
    for relation in d.data.relations:
        if relation.from_ not in classes or relation.to not in classes:
            raise ValidationError(f"Class relation references unknown class: {relation.from_} -> {relation.to} in {d.id}")
        if relation.relation in {"inheritance", "realization"}:
            if relation.from_ == relation.to:
                raise ValidationError(f"Class cannot inherit from or realize itself in {d.id}")
            if relation.from_multiplicity or relation.to_multiplicity:
                raise ValidationError(f"Inheritance and realization do not have multiplicities in {d.id}")
            parents[relation.from_].append(relation.to)
        if relation.relation == "realization" and classes[relation.to].kind not in {"interface", "protocol"}:
            raise ValidationError(f"Realization target '{relation.to}' must be an interface or protocol in {d.id}")
        for multiplicity in (relation.from_multiplicity, relation.to_multiplicity):
            if multiplicity and ".." in multiplicity:
                low, high = multiplicity.split("..")
                if high != "*" and int(low) > int(high):
                    raise ValidationError(f"Inverted multiplicity '{multiplicity}' in {d.id}")
    active, done = set(), set()

    def visit(ident):
        if ident in active:
            raise ValidationError(f"Inheritance/realization cycle at '{ident}' in {d.id}")
        if ident in done:
            return
        active.add(ident)
        for parent in parents[ident]:
            visit(parent)
        active.remove(ident)
        done.add(ident)

    for ident in classes:
        visit(ident)


def _validate_component(d: ComponentDiagram) -> None:
    node_ids = set(d.data.nodes)
    for edge in d.data.edges:
        if edge.from_ not in node_ids:
            raise ValidationError(f"Edge 'from' references unknown node '{edge.from_}' in {d.id}")
        if edge.to not in node_ids:
            raise ValidationError(f"Edge 'to' references unknown node '{edge.to}' in {d.id}")


def _validate_sequence(d: SequenceDiagram) -> None:
    ids = {p.id for p in d.data.participants}
    for msg in d.data.messages:
        if msg.from_ not in ids:
            raise ValidationError(f"Message 'from' references unknown participant '{msg.from_}' in {d.id}")
        if msg.to not in ids:
            raise ValidationError(f"Message 'to' references unknown participant '{msg.to}' in {d.id}")


def _validate_state(d: StateDiagram) -> None:
    ids = {s.id for s in d.data.states}
    if d.data.initial not in ids:
        raise ValidationError(f"Initial state '{d.data.initial}' not in states in {d.id}")
    for t in d.data.transitions:
        if t.from_ not in ids:
            raise ValidationError(f"Transition 'from' references unknown state '{t.from_}' in {d.id}")
        if t.to not in ids:
            raise ValidationError(f"Transition 'to' references unknown state '{t.to}' in {d.id}")


def _validate_activity(d: ActivityDiagram) -> None:
    valid = set(d.data.steps) | {d.data.end}
    if d.data.start not in d.data.steps:
        raise UnknownReferenceError(f"Start step '{d.data.start}' not found in {d.id}")
    for sid, step in d.data.steps.items():
        if step.next and step.next not in valid:
            raise UnknownReferenceError(f"Step '{sid}' next '{step.next}' unknown in {d.id}")
        for branch, target in step.branches.items():
            if target not in valid:
                raise UnknownReferenceError(f"Step '{sid}' branch '{branch}' target '{target}' unknown in {d.id}")
        if step.kind == "merge" and step.branches:
            raise StructureError(f"Step '{sid}' is a merge: it joins flows into one `next` and takes no branches in {d.id}")
        if step.partition is not None and not step.partition.strip():
            raise StructureError(f"Step '{sid}' has an empty partition in {d.id}")


# extremos que admite cada tipo de conexion de despliegue (origen, destino); communication entre
# artefactos se mantiene por compatibilidad, UML la define entre nodos
_DEPLOYMENT_ENDS = {
    "communication": {("node", "node"), ("artifact", "artifact")},
    "deploy": {("artifact", "node")},
    "manifest": {("artifact", "node"), ("artifact", "artifact")},
}


def _validate_deployment(d: DeploymentDiagram) -> None:
    nodes, artifacts = d.data.nodes, d.data.artifacts
    for both in sorted(set(nodes) & set(artifacts)):
        raise StructureError(f"Id '{both}' is both a node and an artifact in {d.id}")
    kind_of = {**{a: "artifact" for a in artifacts}, **{n: "node" for n in nodes}}
    parent: dict[str, str] = {}
    for nid, node in nodes.items():
        for ref in node.contains:
            if ref not in kind_of:
                raise UnknownReferenceError(f"Node '{nid}' contains unknown node or artifact '{ref}' in {d.id}")
            if kind_of[ref] == "node":
                if ref == nid:
                    raise StructureError(f"Node '{nid}' contains itself in {d.id}")
                if ref in parent:
                    raise StructureError(f"Node '{ref}' is contained by both '{parent[ref]}' and '{nid}' in {d.id}")
                parent[ref] = nid
    for nid in nodes:
        seen, current = [nid], parent.get(nid)
        while current is not None:
            if current in seen:
                cycle = " > ".join([*reversed(seen[seen.index(current):]), current])
                raise StructureError(f"Node containment has a cycle ({cycle}) in {d.id}")
            seen.append(current)
            current = parent.get(current)
    for conn in d.data.connections:
        for end, ref in (("from", conn.from_), ("to", conn.to)):
            if ref not in kind_of:
                raise UnknownReferenceError(f"Connection '{end}' references unknown node or artifact '{ref}' in {d.id}")
        ends = (kind_of[conn.from_], kind_of[conn.to])
        if ends not in _DEPLOYMENT_ENDS[conn.kind]:
            allowed = ", ".join(f"{a} -> {b}" for a, b in sorted(_DEPLOYMENT_ENDS[conn.kind]))
            raise EndpointKindError(
                f"Connection '{conn.from_}' -> '{conn.to}' ({conn.kind}) goes {ends[0]} -> {ends[1]}; "
                f"a {conn.kind} connection goes {allowed} in {d.id}"
            )


def _validate_matrix(d: MatrixDiagram) -> None:
    for view in d.data.views:
        valid_stages = {s.id for s in view.stages}
        _check_components(d.id, view.id, valid_stages, d.data.components)


def _check_components(diagram_id, view_id, valid_stages, components):
    for comp in components:
        for sid in comp.stages.get(view_id, []):
            if sid not in valid_stages:
                raise ValidationError(
                    f"Component '{comp.name}' references unknown stage '{sid}' "
                    f"in view '{view_id}' in {diagram_id}"
                )
        _check_components(diagram_id, view_id, valid_stages, comp.children)
