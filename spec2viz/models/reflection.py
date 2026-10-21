from __future__ import annotations
from typing import Literal, Dict, List, Any
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import BaseDiagram, DiagramType, Metadata


class SemanticMetadata(Metadata):
    """Metadata supporting the 6D model for cross-ecosystem alignment."""

    who: str | None = Field(
        default=None, description="Who: Context actor or responsible entity."
    )
    what: str | None = Field(
        default=None, description="What: The object of the semantic relation."
    )
    where: str | None = Field(
        default=None, description="Where: Topology or persistence context."
    )
    when: str | None = Field(
        default=None, description="When: Temporal or phase context."
    )
    how: str | None = Field(
        default=None, description="How: Mechanical or technical context."
    )
    why: str | None = Field(
        default=None, description="Why: Rationale or business rule."
    )


class ReflectionNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: str = Field(
        default="core", description="Semantic kind of the node (e.g., repository, module)."
    )
    label: str | None = Field(
        default=None, description="Optional display label for the node."
    )
    metadata: SemanticMetadata | None = Field(
        default=None, description="Optional 6D metadata for the node."
    )


class ReflectionEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    from_: str = Field(alias="from", description="Source node identifier.")
    to: str = Field(description="Target node identifier.")
    relation: str = Field(
        default="relates", description="Semantic relationship type (e.g., depends_on, inherits)."
    )
    label: str | None = Field(
        default=None, description="Optional label shown alongside the relationship."
    )
    metadata: SemanticMetadata | None = Field(
        default=None, description="Optional 6D metadata for the edge."
    )


class ReflectionIR(BaseModel):
    """Semantic Intermediate Representation for reflection and enforcement."""

    model_config = ConfigDict(extra="forbid")

    nodes: Dict[str, ReflectionNode] = Field(
        description="Reflection nodes keyed by their stable identifier."
    )
    edges: List[ReflectionEdge] = Field(
        default_factory=list, description="Relationships between the reflection nodes."
    )


class EnforcementFact(BaseModel):
    """A single atomic fact extracted for enforcement purposes."""

    source: str = Field(description="Subject identifier of the fact.")
    target: str = Field(description="Object identifier of the fact.")
    relation: str = Field(description="The semantic relation between source and target.")
    context: Dict[str, Any] = Field(
        default_factory=dict, description="Condensed 6D context or additional attributes."
    )


class EnforcementArtifact(BaseModel):
    """Condensed version of the IR for consumption by linters, auditors, and gates."""

    model_config = ConfigDict(extra="forbid")

    fingerprint: str = Field(
        description="Hash or version identifier to ensure artifact integrity."
    )
    facts: List[EnforcementFact] = Field(
        description="List of atomic facts that form the enforcement surface."
    )


class ReflectionDiagram(BaseDiagram):
    """Diagram type specifically for architectural reflection and enforcement."""

    type: Literal[DiagramType.reflection] = Field(
        default=DiagramType.reflection,
        description="Discriminator for reflection diagram specs.",
    )
    data: ReflectionIR = Field(
        description="The core semantic IR containing nodes and edges."
    )
    enforcement: EnforcementArtifact | None = Field(
        default=None,
        description="Optional condensed artifact for inward architectural enforcement.",
    )


__all__ = [
    "SemanticMetadata",
    "ReflectionNode",
    "ReflectionEdge",
    "ReflectionIR",
    "EnforcementFact",
    "EnforcementArtifact",
    "ReflectionDiagram",
]
