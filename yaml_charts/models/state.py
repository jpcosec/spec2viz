from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from yaml_charts.models.base import BaseDiagram, DiagramType


class StateModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id:    str
    label: str


class TransitionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_:  str       = Field(alias="from")
    to:     str
    on:     str
    guard:  str | None = None
    action: str | None = None


class StateData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entity:      str
    initial:     str
    states:      list[StateModel]
    transitions: list[TransitionModel]


class StateDiagram(BaseDiagram):
    type: Literal[DiagramType.state] = DiagramType.state
    data: StateData


__all__ = ["StateModel", "TransitionModel", "StateData", "StateDiagram"]
