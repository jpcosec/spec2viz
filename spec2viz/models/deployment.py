from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import BaseDiagram, DiagramType


class DeploymentNodeModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str | None = Field(
        default=None, description="Optional display name for the deployment node."
    )
    kind: str = Field(
        default="server",
        description="Semantic infrastructure kind, such as server or browser.",
    )
    contains: list[str] = Field(
        default_factory=list,
        description="Artifact or node identifiers hosted within this deployment node.",
    )


class ArtifactModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str | None = Field(
        default=None, description="Optional display name for the deployed artifact."
    )
    kind: str = Field(
        default="component", description="Semantic artifact kind used in rendering."
    )


class ConnectionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    from_: str = Field(
        alias="from", description="Source node identifier for the connection."
    )
    to: str = Field(description="Destination node identifier for the connection.")
    protocol: str | None = Field(
        default=None,
        description="Optional protocol or transport label for the connection.",
    )


class DeploymentData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    nodes: dict[str, DeploymentNodeModel] = Field(
        description="Deployment nodes keyed by identifier."
    )
    artifacts: dict[str, ArtifactModel] = Field(
        default_factory=dict, description="Deployable artifacts keyed by identifier."
    )
    connections: list[ConnectionModel] = Field(
        default_factory=list,
        description="Network or runtime connections between deployment nodes.",
    )


class DeploymentDiagram(BaseDiagram):
    type: Literal[DiagramType.deployment] = Field(
        default=DiagramType.deployment,
        description="Discriminator for deployment diagram specs.",
    )
    data: DeploymentData = Field(
        description="Deployment-specific nodes, artifacts, and connections."
    )


__all__ = [
    "DeploymentNodeModel",
    "ArtifactModel",
    "ConnectionModel",
    "DeploymentData",
    "DeploymentDiagram",
]
