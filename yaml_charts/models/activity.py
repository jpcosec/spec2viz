from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict
from yaml_charts.models.base import BaseDiagram, DiagramType


class StepModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label:    str
    kind:     str            = "action"
    next:     str | None     = None
    branches: dict[str, str] = {}


class ActivityData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start: str
    steps: dict[str, StepModel]
    end:   str


class ActivityDiagram(BaseDiagram):
    type: Literal[DiagramType.activity] = DiagramType.activity
    data: ActivityData
