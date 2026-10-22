from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import DocRef, BaseDiagram, DiagramType


StepTone = Literal["success", "warning", "danger", "info", "neutral", "rule1", "rule2", "rule3", "rule4", "rule5"]


class StepModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str = Field(description="Display label rendered for the activity step.")
    kind: str = Field(
        default="action",
        description="Semantic step type: action (default), decision (branches) or merge (joins branches back into one flow; drawn as a diamond like decision).",
    )
    tone: StepTone | None = Field(
        default=None,
        description=(
            "Optional color tone for the BPMN renderer: success, warning, danger, info, neutral, or rule1..rule5 "
            "to tint each decision group. A gateway's outgoing flows take its border color."
        ),
    )
    partition: str | None = Field(
        default=None,
        description="Optional swimlane (UML activity partition) the step belongs to, such as Dev, Approver or AWS; renderers draw one lane per partition.",
    )
    notes: str | None = Field(
        default=None,
        description="Optional UML note attached to the step, drawn as a note with a folded corner joined to it.",
    )
    next: str | None = Field(
        default=None, description="Identifier of the next step in the default path."
    )
    branches: dict[str, str] = Field(
        default_factory=dict,
        description="Conditional branch labels mapped to destination step identifiers.",
    )
    atoms: list[str] = Field(
        default_factory=list,
        description="Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
    )
    refs: list[DocRef] = Field(
        default_factory=list,
        description="Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
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


__all__ = ["StepModel", "StepTone", "ActivityData", "ActivityDiagram"]
