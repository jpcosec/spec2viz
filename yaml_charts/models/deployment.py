from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from yaml_charts.models.base import BaseDiagram, DiagramType


class DeploymentNodeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label:    str       | None = None
    kind:     str       = "server"
    contains: list[str] = []


class ArtifactModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str | None = None
    kind:  str        = "component"


class ConnectionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_:    str       = Field(alias="from")
    to:       str
    protocol: str | None = None


class DeploymentData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nodes:       dict[str, DeploymentNodeModel]
    artifacts:   dict[str, ArtifactModel]      = {}
    connections: list[ConnectionModel]          = []


class DeploymentDiagram(BaseDiagram):
    type: Literal[DiagramType.deployment] = DiagramType.deployment
    data: DeploymentData


__all__ = ["DeploymentNodeModel", "ArtifactModel", "ConnectionModel", "DeploymentData", "DeploymentDiagram"]
