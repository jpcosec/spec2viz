"""Base Pydantic models and DiagramType enum shared by all diagram types."""

from __future__ import annotations
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

# `Model:name` export id of an sldb document, optionally prefixed by the alias of a
# linked store (`store:Model:name`). The same format sldb resolves in declared
# references; an id without the model part is not a reference.
DOC_REF_PATTERN = r"^(?:[A-Za-z0-9][A-Za-z0-9._-]*:)?[A-Za-z_][A-Za-z0-9_]*:[^\s:]+$"
DocRef = Annotated[str, Field(pattern=DOC_REF_PATTERN)]



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
        description=(
            "Style per semantic kind. Neutral keys `fill`, `stroke` (a token of the default palette such as "
            "`database-fill`, a `#rrggbb` hex used in both themes, or a `{light, dark}` pair of hex or tokens) and "
            "`icon` (a name of the palette's Lucide icon set) apply to every "
            "renderer and to graph_ui, below the notation's glyph and above the default palette. A renderer-specific "
            "block (such as `plantuml: {background, border, font}`) is read only by that renderer."
        ),
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
