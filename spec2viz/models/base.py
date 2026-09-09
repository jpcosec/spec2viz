"""Base Pydantic models and DiagramType enum shared by all diagram types."""

from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class DiagramType(str, Enum):
    class_ = "class"
    component = "component"
    sequence = "sequence"
    state = "state"
    activity = "activity"
    deployment = "deployment"
    component_view_matrix = "component_view_matrix"
    reflection = "reflection"


class Metadata(BaseModel):
    model_config = ConfigDict(extra="ignore")

    author: str | None = Field(
        default=None,
        description="Name of the person or team responsible for the diagram spec.",
    )
    description: str | None = Field(
        default=None,
        description="Free-form summary that explains the intent of the diagram.",
    )


class Style(BaseModel):
    model_config = ConfigDict(extra="ignore")

    theme: str = Field(
        default="default",
        description="Renderer theme name used to style the generated output.",
    )
    kinds: dict[str, dict] = Field(
        default_factory=dict,
        description="Kind-specific style overrides keyed by semantic kind name.",
    )


class BaseDiagram(BaseModel):
    """Base class for all diagram types. Subclasses must add a `data` field."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Stable identifier for the diagram specification.")
    title: str = Field(description="Human-readable title shown in rendered output.")
    type: DiagramType = Field(
        description="Semantic diagram type used to select the schema and renderer flow."
    )
    version: str = Field(
        description="Schema or document version for the specification."
    )
    metadata: Metadata | None = Field(
        default=None,
        description="Optional authorship and descriptive metadata for the spec.",
    )
    style: Style | None = Field(
        default=None, description="Optional presentation hints for renderers."
    )


__all__ = ["DiagramType", "Metadata", "Style", "BaseDiagram"]
