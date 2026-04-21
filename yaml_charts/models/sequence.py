from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from yaml_charts.models.base import BaseDiagram, DiagramType


class ParticipantModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id:   str
    kind: str = "component"


class MessageModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_:     str       = Field(alias="from")
    to:        str
    message:   str
    kind:      str       = "sync"
    condition: str | None = None
    group:     str | None = None


class SequenceData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    participants: list[ParticipantModel]
    messages:     list[MessageModel]


class SequenceDiagram(BaseDiagram):
    type: Literal[DiagramType.sequence] = DiagramType.sequence
    data: SequenceData


__all__ = ["ParticipantModel", "MessageModel", "SequenceData", "SequenceDiagram"]
