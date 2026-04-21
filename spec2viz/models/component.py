from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import BaseDiagram, DiagramType


class NodeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str | None = Field(
        default=None, description="Optional display name for the component node."
    )
    kind: str = Field(
        default="core", description="Semantic category for the component."
    )
    contains: list[str] = Field(
        default_factory=list,
        description="Identifiers of nested components contained by this node.",
    )


class EdgeModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_: str = Field(alias="from", description="Source component identifier.")
    to: str = Field(description="Destination component identifier.")
    relation: str = Field(
        default="uses",
        description="Semantic relationship between the connected components.",
    )
    label: str | None = Field(
        default=None, description="Optional label shown alongside the relationship."
    )


class ComponentData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nodes: dict[str, NodeModel] = Field(
        description="Component nodes keyed by identifier."
    )
    edges: list[EdgeModel] = Field(
        default_factory=list,
        description="Relationships between the declared component nodes.",
    )


class ComponentDiagram(BaseDiagram):
    type: Literal[DiagramType.component] = Field(
        default=DiagramType.component,
        description="Discriminator for component diagram specs.",
    )
    data: ComponentData = Field(
        description="Component-specific nodes and relationships."
    )


__all__ = ["NodeModel", "EdgeModel", "ComponentData", "ComponentDiagram"]
