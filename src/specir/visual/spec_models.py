"""The spec models of the eight diagram types, taken from SLDB (D3), never defined here.

The models, their loading and their validation live in sldb (`sldb.models.notation.diagram_specs`,
with `load_spec` and `validate_spec` in `sldb.api.notations`). `sldb.api.notations` exports the two
functions but not the model classes yet, so this module is the only one of specIR that reaches
`sldb.models.notation.diagram_specs` (tests/test_imports.py allows it here and nowhere else). When
sldb exports the classes from `sldb.api.notations`, only these imports change."""

from __future__ import annotations

from sldb.api.notations import load_spec, validate_spec
from sldb.models.notation.diagram_specs import (
    ActivityDiagram,
    ClassDiagram,
    ComponentDiagram,
    DeploymentDiagram,
    MatrixDiagram,
    ReflectionDiagram,
    SequenceDiagram,
    StateDiagram,
)
from sldb.models.notation.diagram_specs.base import BaseDiagram
from sldb.models.notation.diagram_specs.reflection import EnforcementArtifact, EnforcementFact

#: The eight diagram spec models, in the order spec2viz's `compile_ir` dispatched them.
SPEC_MODELS = (
    ClassDiagram, SequenceDiagram, StateDiagram, ComponentDiagram,
    ActivityDiagram, DeploymentDiagram, MatrixDiagram, ReflectionDiagram,
)

__all__ = [
    "ActivityDiagram", "BaseDiagram", "ClassDiagram", "ComponentDiagram", "DeploymentDiagram",
    "EnforcementArtifact", "EnforcementFact", "MatrixDiagram", "ReflectionDiagram", "SPEC_MODELS",
    "SequenceDiagram", "StateDiagram", "load_spec", "validate_spec",
]
