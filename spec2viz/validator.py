from __future__ import annotations
from spec2viz.exceptions import ValidationError
from spec2viz.models.base import BaseDiagram
from spec2viz.models.sequence   import SequenceDiagram
from spec2viz.models.state      import StateDiagram
from spec2viz.models.component  import ComponentDiagram
from spec2viz.models.activity   import ActivityDiagram
from spec2viz.models.deployment import DeploymentDiagram
from spec2viz.models.matrix     import MatrixDiagram, MatrixComponentModel
from spec2viz.models.class_diagram import ClassDiagram


def validate(diagram: BaseDiagram) -> None:
    match diagram:
        case ClassDiagram():      _validate_class(diagram)
        case ComponentDiagram():  _validate_component(diagram)
        case SequenceDiagram():   _validate_sequence(diagram)
        case StateDiagram():      _validate_state(diagram)
        case ActivityDiagram():   _validate_activity(diagram)
        case DeploymentDiagram(): _validate_deployment(diagram)
        case MatrixDiagram():     _validate_matrix(diagram)


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
        raise ValidationError(f"Start step '{d.data.start}' not found in {d.id}")
    for sid, step in d.data.steps.items():
        if step.next and step.next not in valid:
            raise ValidationError(f"Step '{sid}' next '{step.next}' unknown in {d.id}")
        for branch, target in step.branches.items():
            if target not in valid:
                raise ValidationError(f"Step '{sid}' branch '{branch}' target '{target}' unknown in {d.id}")


def _validate_deployment(d: DeploymentDiagram) -> None:
    art_ids = set(d.data.artifacts)
    for node in d.data.nodes.values():
        for ref in node.contains:
            if ref not in art_ids:
                raise ValidationError(f"Node contains unknown artifact '{ref}' in {d.id}")
    for conn in d.data.connections:
        if conn.from_ not in art_ids:
            raise ValidationError(f"Connection 'from' references unknown artifact '{conn.from_}' in {d.id}")
        if conn.to not in art_ids:
            raise ValidationError(f"Connection 'to' references unknown artifact '{conn.to}' in {d.id}")


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
