from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from yaml_charts.models.base import BaseDiagram, DiagramType


class NodeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label:    str       | None = None
    kind:     str       = "core"
    contains: list[str] = []


class EdgeModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_:    str       = Field(alias="from")
    to:       str
    relation: str       = "uses"
    label:    str | None = None


class ComponentData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nodes: dict[str, NodeModel]
    edges: list[EdgeModel] = []


class ComponentDiagram(BaseDiagram):
    type: Literal[DiagramType.component] = DiagramType.component
    data: ComponentData


__all__ = ["NodeModel", "EdgeModel", "ComponentData", "ComponentDiagram"]
