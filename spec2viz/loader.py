from __future__ import annotations
from pathlib import Path
from typing import Annotated, Union

import yaml
from pydantic import Field, TypeAdapter, ValidationError as PydanticValidationError

from spec2viz.exceptions import ParseError
from spec2viz.models.base import BaseDiagram, DiagramType
from spec2viz.models.sequence    import SequenceDiagram
from spec2viz.models.state       import StateDiagram
from spec2viz.models.component   import ComponentDiagram
from spec2viz.models.activity    import ActivityDiagram
from spec2viz.models.deployment  import DeploymentDiagram
from spec2viz.models.matrix      import MatrixDiagram
from spec2viz.models.reflection  import ReflectionDiagram
from spec2viz.models.class_diagram import ClassDiagram

AnyDiagram = Annotated[
    Union[
        ClassDiagram,
        SequenceDiagram, StateDiagram, ComponentDiagram,
        ActivityDiagram, DeploymentDiagram, MatrixDiagram,
        ReflectionDiagram,
    ],
    Field(discriminator="type"),
]

_adapter: TypeAdapter[AnyDiagram] = TypeAdapter(AnyDiagram)
_valid_types = {t.value for t in DiagramType}


def load(path: str | Path) -> BaseDiagram:
    path = Path(path)
    if not path.exists():
        raise ParseError(f"File not found: {path}")
    try:
        raw = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        raise ParseError(f"YAML parse error in {path}: {exc}") from exc

    diagram_type = raw.get("type", "")
    if diagram_type not in _valid_types:
        raise ParseError(f"Unsupported diagram type: {diagram_type}")

    try:
        return _adapter.validate_python(raw)
    except PydanticValidationError as exc:
        desconocidas = unknown_keys(exc)
        if desconocidas:
            listado = "; ".join(f"unknown key '{k}'" for k in desconocidas)
            raise ParseError(f"Invalid diagram schema in {path} (type {diagram_type}): {listado}. "
                             "Every key must be part of the schema of its type "
                             "(`spec2viz diagram schema` exports them).") from exc
        raise ParseError(f"Invalid diagram schema in {path}: {exc}") from exc


def unknown_keys(exc: PydanticValidationError) -> list[str]:
    """The dotted path of every key the schema does not declare (``extra_forbidden``), without the
    tag of the diagram union: ``data.edges``, ``data.nodes.ec2.estado``, ``data.connections.0.via``."""
    out = []
    for err in exc.errors():
        if err.get("type") != "extra_forbidden":
            continue
        loc = [str(p) for p in err.get("loc", ())]
        if loc and loc[0] in _valid_types:   # the discriminated union puts the type first
            loc = loc[1:]
        out.append(".".join(loc))
    return out
