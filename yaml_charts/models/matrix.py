from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict
from yaml_charts.models.base import BaseDiagram, DiagramType


class MatrixStageModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id:    str
    label: str


class MatrixViewModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id:     str
    label:  str
    stages: list[MatrixStageModel]


class MatrixComponentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name:     str
    kind:     str                        = "core"
    label:    str | None                 = None
    stages:   dict[str, list[str]]       = {}
    children: list[MatrixComponentModel] = []


MatrixComponentModel.model_rebuild()


class MatrixData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    views:      list[MatrixViewModel]
    components: list[MatrixComponentModel]


class MatrixDiagram(BaseDiagram):
    type: Literal[DiagramType.component_view_matrix] = DiagramType.component_view_matrix
    data: MatrixData


__all__ = ["MatrixStageModel", "MatrixViewModel", "MatrixComponentModel", "MatrixData", "MatrixDiagram"]
