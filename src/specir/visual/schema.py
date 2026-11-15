"""JSON Schema export of diagram specs (per type or all) and of catalogs / diagram stores, migrated
from `spec2viz.schema`. The models are sldb's (D3); only the export is specIR's."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Type

from pydantic import TypeAdapter

from specir.visual.spec_models import (
    ActivityDiagram,
    AnyDiagram,
    BaseDiagram,
    ClassDiagram,
    ComponentDiagram,
    DeploymentDiagram,
    DiagramStoreEnvelope,
    DiagramType,
    MatrixDiagram,
    SequenceDiagram,
    StateDiagram,
)


_MODEL_BY_TYPE: dict[DiagramType, Type[BaseDiagram]] = {
    DiagramType.class_: ClassDiagram,
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

    if str(diagram_type) in {"diagram-store", "catalog", "project"}:
        return DiagramStoreEnvelope.model_json_schema()

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
