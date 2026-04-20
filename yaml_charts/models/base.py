from __future__ import annotations
from enum import Enum
from pydantic import BaseModel


class DiagramType(str, Enum):
    component             = "component"
    sequence              = "sequence"
    state                 = "state"
    activity              = "activity"
    deployment            = "deployment"
    component_view_matrix = "component_view_matrix"


class Metadata(BaseModel):
    author:      str | None = None
    description: str | None = None


class Style(BaseModel):
    theme: str             = "default"
    kinds: dict[str, dict] = {}


class BaseDiagram(BaseModel):
    id:       str
    title:    str
    type:     DiagramType
    version:  str
    metadata: Metadata | None = None
    style:    Style    | None = None
