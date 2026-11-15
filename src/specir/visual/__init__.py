"""specIR's visual layer: the intermediate representation, its compilers and the projections of
the graph to it (IR11). IR13d extends this module with the full public API of the layer.

The spec models of the eight diagram types are sldb's (D3) and are only re-exported here for the
visual layer's callers; nothing of them is defined in specIR. `load_spec` and `validate_spec` are
used from `sldb.api.notations` directly, without a wrapper."""

from specir.visual.compilers import compile_ir
from specir.visual.compilers.activity import ActivityCompiler
from specir.visual.compilers.class_diagram import ClassCompiler
from specir.visual.compilers.component import ComponentCompiler
from specir.visual.compilers.deployment import DeploymentCompiler
from specir.visual.compilers.matrix import MatrixCompiler
from specir.visual.compilers.reflection import ReflectionCompiler
from specir.visual.compilers.sequence import SequenceCompiler
from specir.visual.compilers.state import StateCompiler
from specir.visual.exceptions import CompileError, Spec2VizError
from specir.visual.ir import *  # noqa: F401,F403 (the IR dataclasses, see specir.visual.ir.__all__)
from specir.visual.ir import __all__ as _IR
from specir.visual.normalize import differences, equivalent, normalize
from specir.visual.projections import ANY_STATE, component_from_view, from_spec_doc, state_from_view, view_graph
from specir.visual.spec_models import (
    SPEC_MODELS,
    ActivityDiagram,
    BaseDiagram,
    ClassDiagram,
    ComponentDiagram,
    DeploymentDiagram,
    EnforcementArtifact,
    EnforcementFact,
    MatrixDiagram,
    ReflectionDiagram,
    SequenceDiagram,
    StateDiagram,
)

__all__ = [
    *_IR,
    "ActivityCompiler", "ClassCompiler", "ComponentCompiler", "DeploymentCompiler", "MatrixCompiler",
    "ReflectionCompiler", "SequenceCompiler", "StateCompiler", "compile_ir",
    "CompileError", "Spec2VizError",
    "differences", "equivalent", "normalize",
    "ANY_STATE", "component_from_view", "from_spec_doc", "state_from_view", "view_graph",
    "SPEC_MODELS", "ActivityDiagram", "BaseDiagram", "ClassDiagram", "ComponentDiagram", "DeploymentDiagram",
    "EnforcementArtifact", "EnforcementFact", "MatrixDiagram", "ReflectionDiagram", "SequenceDiagram",
    "StateDiagram",
]
