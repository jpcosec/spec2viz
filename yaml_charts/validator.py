from __future__ import annotations
from yaml_charts.exceptions import ValidationError
from yaml_charts.models.base import BaseDiagram
from yaml_charts.models.sequence   import SequenceDiagram
from yaml_charts.models.state      import StateDiagram
from yaml_charts.models.component  import ComponentDiagram
from yaml_charts.models.activity   import ActivityDiagram
from yaml_charts.models.deployment import DeploymentDiagram
from yaml_charts.models.matrix     import MatrixDiagram, MatrixComponentModel


def validate(diagram: BaseDiagram) -> None:
    match diagram:
        case ComponentDiagram():  _validate_component(diagram)
        case SequenceDiagram():   _validate_sequence(diagram)
        case StateDiagram():      _validate_state(diagram)
        case ActivityDiagram():   _validate_activity(diagram)
        case DeploymentDiagram(): _validate_deployment(diagram)
        case MatrixDiagram():     _validate_matrix(diagram)


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
