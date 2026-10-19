from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import DocRef, BaseDiagram, DiagramType


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
        description="Artifact or node identifiers hosted within this deployment node. Nodes nest (VPC > subnet > cluster > service): a node has at most one parent and containment has no cycles.",
    )
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
    )


class ArtifactModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str | None = Field(
        default=None, description="Optional display name for the deployed artifact."
    )
    kind: str = Field(
        default="component", description="Semantic artifact kind used in rendering."
    )
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
    )


class ConnectionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    from_: str = Field(
        alias="from", description="Source node identifier for the connection."
    )
    to: str = Field(description="Destination node or artifact identifier for the connection.")
    kind: Literal["communication", "deploy", "manifest"] = Field(
        default="communication",
        description=(
            "communication (default): a communication path between two nodes, or between two artifacts as before; "
            "deploy: «deploy» from an artifact to the node it is deployed on; "
            "manifest: «manifest» from an artifact to the node or artifact it manifests."
        ),
    )
    protocol: str | None = Field(
        default=None,
        description="Optional protocol or transport label for the connection.",
    )
    label: str | None = Field(
        default=None,
        description="Optional label for the connection; shown with the protocol when both are set.",
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
        description="Communication paths between nodes (or artifacts) and «deploy»/«manifest» relations from artifacts.",
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
