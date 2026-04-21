from __future__ import annotations
from pathlib import Path
from typing import Annotated, Union

import yaml
from pydantic import Field, TypeAdapter, ValidationError as PydanticValidationError

from spec2viz.exceptions import ParseError
from spec2viz.models.base import BaseDiagram, DiagramType
from spec2viz.models.sequence   import SequenceDiagram
from spec2viz.models.state      import StateDiagram
from spec2viz.models.component  import ComponentDiagram
from spec2viz.models.activity   import ActivityDiagram
from spec2viz.models.deployment import DeploymentDiagram
from spec2viz.models.matrix     import MatrixDiagram

AnyDiagram = Annotated[
    Union[
        SequenceDiagram, StateDiagram, ComponentDiagram,
        ActivityDiagram, DeploymentDiagram, MatrixDiagram,
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
        raise ParseError(f"Invalid diagram schema in {path}: {exc}") from exc
