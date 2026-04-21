from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from spec2viz.models.base import BaseDiagram, DiagramType


class MatrixStageModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(description="Stable stage identifier used inside matrix views.")
    label: str = Field(description="Display label rendered for the stage column.")


class MatrixViewModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(description="Stable identifier for the matrix view.")
    label: str = Field(description="Display label rendered for the view.")
    stages: list[MatrixStageModel] = Field(
        description="Ordered stages shown within the view."
    )


class MatrixComponentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(
        description="Stable component identifier used within the matrix hierarchy."
    )
    kind: str = Field(
        default="core", description="Semantic category assigned to the component."
    )
    label: str | None = Field(
        default=None, description="Optional display name for the component."
    )
    stages: dict[str, list[str]] = Field(
        default_factory=dict,
        description="View-to-stage membership mapping for the component.",
    )
    children: list[MatrixComponentModel] = Field(
        default_factory=list,
        description="Nested child components rendered beneath this component.",
    )


MatrixComponentModel.model_rebuild()


class MatrixData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    views: list[MatrixViewModel] = Field(
        description="Matrix views that define the column layout."
    )
    components: list[MatrixComponentModel] = Field(
        description="Top-level components rendered as rows in the matrix."
    )


class MatrixDiagram(BaseDiagram):
    type: Literal[DiagramType.component_view_matrix] = Field(
        default=DiagramType.component_view_matrix,
        description="Discriminator for component view matrix specs.",
    )
    data: MatrixData = Field(
        description="Matrix-specific views and component hierarchy."
    )


__all__ = [
    "MatrixStageModel",
    "MatrixViewModel",
    "MatrixComponentModel",
    "MatrixData",
    "MatrixDiagram",
]
