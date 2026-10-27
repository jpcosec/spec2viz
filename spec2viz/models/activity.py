from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
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
    detail: str | None = Field(
        default=None,
        description=(
            "Optional long text shown in the viewer's side panel; the BPMN box keeps showing only `label`. "
            "Other renderers may ignore it."
        ),
    )
    group: str | None = Field(
        default=None,
        description=(
            "Optional group id the step belongs to. The BPMN renderer draws each group as a collapsed "
            "subProcess with its own drill-down plane; renderers that do not support groups ignore it."
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


class GroupModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str = Field(description="Display label of the collapsed subProcess that represents the group.")
    tone: StepTone | None = Field(
        default=None,
        description="Optional BPMN in Color tone for the collapsed subProcess, using the same palette as steps.",
    )
    detail: str | None = Field(
        default=None,
        description="Optional long text about the group, shown in the viewer's side panel when the subProcess is selected.",
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
    groups: dict[str, GroupModel] = Field(
        default_factory=dict,
        description=(
            "Optional groups keyed by id. Each group becomes a collapsed subProcess in the BPMN renderer; "
            "a step joins one with its `group` field."
        ),
    )

    @model_validator(mode="after")
    def _groups_exist(self) -> "ActivityData":
        known = set(self.groups)
        for sid, step in self.steps.items():
            if step.group is not None and step.group not in known:
                available = ", ".join(sorted(known)) or "none defined"
                raise ValueError(
                    f"Step '{sid}' references unknown group '{step.group}' (groups: {available})"
                )
        return self


class ActivityDiagram(BaseDiagram):
    type: Literal[DiagramType.activity] = Field(
        default=DiagramType.activity,
        description="Discriminator for activity diagram specs.",
    )
    data: ActivityData = Field(description="Activity-specific steps and control flow.")


__all__ = ["StepModel", "GroupModel", "StepTone", "ActivityData", "ActivityDiagram"]
