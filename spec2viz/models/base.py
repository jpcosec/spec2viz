"""Base Pydantic models and DiagramType enum shared by all diagram types."""

from __future__ import annotations
from enum import Enum
from typing import Annotated, Any
from pydantic import BaseModel, ConfigDict, Field, model_validator

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


#: Prefix of the project annotations a spec may add under ``metadata`` (OpenAPI-style ``x-`` extensions).
EXTENSION_PREFIX = "x-"


class Metadata(BaseModel):
    """Authorship and description, plus the project's own annotations as ``x-*`` keys.

    ``metadata`` is the only place a project may add keys of its own, and only with the ``x-`` prefix
    (``x-fuentes``, ``x-estado``): they are kept as written under ``extensions``. Any other unknown key is
    an error with its path, like everywhere else in a spec (a typo there is caught, not silently kept)."""

    model_config = ConfigDict(extra="forbid")

    author: str | None = Field(
        default=None,
        description="Name of the person or team responsible for the diagram spec.",
    )
    description: str | None = Field(
        default=None,
        description="Free-form summary that explains the intent of the diagram.",
    )
    extensions: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Project annotations: every `metadata` key that starts with `x-`, kept as written (renderers ignore "
            "them). Any other unknown key under `metadata` is an error."
        ),
    )

    @model_validator(mode="before")
    @classmethod
    def _extensions(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        value = dict(value)
        found = {k: value.pop(k) for k in list(value) if isinstance(k, str) and k.startswith(EXTENSION_PREFIX)}
        if found:
            value["extensions"] = {**(value.get("extensions") or {}), **found}
        return value


class Style(BaseModel):
    model_config = ConfigDict(extra="forbid")

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

    model_config = ConfigDict(extra="forbid")

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
