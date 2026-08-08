from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import BaseDiagram, DiagramType


class StepModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str = Field(description="Display label rendered for the activity step.")
    kind: str = Field(
        default="action", description="Semantic step type, such as action or decision."
    )
    next: str | None = Field(
        default=None, description="Identifier of the next step in the default path."
    )
    branches: dict[str, str] = Field(
        default_factory=dict,
        description="Conditional branch labels mapped to destination step identifiers.",
    )


class ActivityData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    start: str = Field(description="Identifier of the first step in the activity flow.")
    steps: dict[str, StepModel] = Field(
        description="All activity steps keyed by identifier."
    )
    end: str = Field(
        description="Identifier of the terminal step in the activity flow."
    )


class ActivityDiagram(BaseDiagram):
    type: Literal[DiagramType.activity] = Field(
        default=DiagramType.activity,
        description="Discriminator for activity diagram specs.",
    )
    data: ActivityData = Field(description="Activity-specific steps and control flow.")


__all__ = ["StepModel", "ActivityData", "ActivityDiagram"]
