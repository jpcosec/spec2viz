"""Base Pydantic models and DiagramType enum shared by all diagram types."""
from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, ConfigDict


class DiagramType(str, Enum):
    component             = "component"
    sequence              = "sequence"
    state                 = "state"
    activity              = "activity"
    deployment            = "deployment"
    component_view_matrix = "component_view_matrix"


class Metadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    author:      str | None = None
    description: str | None = None


class Style(BaseModel):
    model_config = ConfigDict(extra="forbid")

    theme: str             = "default"
    kinds: dict[str, dict] = {}


class BaseDiagram(BaseModel):
    """Base class for all diagram types. Subclasses must add a `data` field."""
    model_config = ConfigDict(extra="forbid")

    id:       str
    title:    str
    type:     DiagramType
    version:  str
    metadata: Metadata | None = None
    style:    Style    | None = None


__all__ = ["DiagramType", "Metadata", "Style", "BaseDiagram"]
