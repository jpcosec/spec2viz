from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import BaseDiagram, DiagramType


class StateModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(description="Stable state identifier referenced by transitions.")
    label: str = Field(description="Display label rendered for the state.")


class TransitionModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_: str = Field(
        alias="from", description="Source state identifier for the transition."
    )
    to: str = Field(description="Destination state identifier for the transition.")
    on: str = Field(description="Event or trigger that causes the transition.")
    guard: str | None = Field(
        default=None,
        description="Optional guard condition that must be true for the transition.",
    )
    action: str | None = Field(
        default=None, description="Optional action executed during the transition."
    )


class StateData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entity: str = Field(
        description="Name of the entity whose lifecycle is being modeled."
    )
    initial: str = Field(description="Identifier of the initial state.")
    states: list[StateModel] = Field(
        description="All states that can appear in the lifecycle."
    )
    transitions: list[TransitionModel] = Field(
        description="Transitions connecting the defined states."
    )


class StateDiagram(BaseDiagram):
    type: Literal[DiagramType.state] = Field(
        default=DiagramType.state, description="Discriminator for state diagram specs."
    )
    data: StateData = Field(
        description="State-specific lifecycle nodes and transitions."
    )


__all__ = ["StateModel", "TransitionModel", "StateData", "StateDiagram"]
