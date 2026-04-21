from __future__ import annotations
from pathlib import Path
from typing import Annotated, Union

import yaml
from pydantic import Field, TypeAdapter, ValidationError as PydanticValidationError

from yaml_charts.exceptions import ParseError
from yaml_charts.models.base import BaseDiagram, DiagramType
from yaml_charts.models.sequence   import SequenceDiagram
from yaml_charts.models.state      import StateDiagram
from yaml_charts.models.component  import ComponentDiagram
from yaml_charts.models.activity   import ActivityDiagram
from yaml_charts.models.deployment import DeploymentDiagram
from yaml_charts.models.matrix     import MatrixDiagram

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
