from __future__ import annotations

import json
from pathlib import Path
from typing import Type

from pydantic import TypeAdapter

from spec2viz.loader import AnyDiagram
from spec2viz.models.activity import ActivityDiagram
from spec2viz.models.base import BaseDiagram, DiagramType
from spec2viz.models.component import ComponentDiagram
from spec2viz.models.deployment import DeploymentDiagram
from spec2viz.models.matrix import MatrixDiagram
from spec2viz.models.sequence import SequenceDiagram
from spec2viz.models.state import StateDiagram


_MODEL_BY_TYPE: dict[DiagramType, Type[BaseDiagram]] = {
    DiagramType.sequence: SequenceDiagram,
    DiagramType.state: StateDiagram,
    DiagramType.component: ComponentDiagram,
    DiagramType.activity: ActivityDiagram,
    DiagramType.deployment: DeploymentDiagram,
    DiagramType.component_view_matrix: MatrixDiagram,
}


def json_schema(diagram_type: str | DiagramType | None = None) -> dict:
    if diagram_type is None:
        return TypeAdapter(AnyDiagram).json_schema()

    resolved_type = DiagramType(diagram_type)
    return _MODEL_BY_TYPE[resolved_type].model_json_schema()


def write_json_schema(
    path: str | Path,
    diagram_type: str | DiagramType | None = None,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(json_schema(diagram_type), indent=2))
    return output_path


__all__ = ["json_schema", "write_json_schema"]
