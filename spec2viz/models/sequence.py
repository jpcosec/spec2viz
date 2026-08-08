from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import BaseDiagram, DiagramType


class ParticipantModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(description="Unique participant identifier referenced by messages.")
    kind: str = Field(
        default="component",
        description="Semantic participant kind used for styling or grouping.",
    )


class MessageModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    from_: str = Field(
        alias="from", description="Participant id that sends the message."
    )
    to: str = Field(description="Participant id that receives the message.")
    message: str = Field(description="Label displayed on the message arrow.")
    kind: str = Field(
        default="sync", description="Message interaction type, such as sync or async."
    )
    condition: str | None = Field(
        default=None,
        description="Optional condition that qualifies when the message is sent.",
    )
    group: str | None = Field(
        default=None, description="Optional group label for visually related messages."
    )


class SequenceData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    participants: list[ParticipantModel] = Field(
        description="Ordered participants that appear across the sequence diagram."
    )
    messages: list[MessageModel] = Field(
        description="Ordered interactions exchanged between participants."
    )


class SequenceDiagram(BaseDiagram):
    type: Literal[DiagramType.sequence] = Field(
        default=DiagramType.sequence,
        description="Discriminator for sequence diagram specs.",
    )
    data: SequenceData = Field(
        description="Sequence-specific participants and messages."
    )


__all__ = ["ParticipantModel", "MessageModel", "SequenceData", "SequenceDiagram"]
