"""Compilation dispatch by diagram type (migrated from `spec2viz.compilers`): one compiler per
spec model of sldb (D3), each producing the intermediate representation of `specir.visual.ir`."""
from __future__ import annotations
from specir.visual.spec_models import BaseDiagram
from specir.visual.spec_models import SequenceDiagram
from specir.visual.spec_models import StateDiagram
from specir.visual.spec_models import ComponentDiagram
from specir.visual.spec_models import ActivityDiagram
from specir.visual.spec_models import DeploymentDiagram
from specir.visual.spec_models import MatrixDiagram
from specir.visual.compilers.sequence   import SequenceCompiler
from specir.visual.compilers.state      import StateCompiler
from specir.visual.compilers.component  import ComponentCompiler
from specir.visual.compilers.activity   import ActivityCompiler
from specir.visual.compilers.deployment import DeploymentCompiler
from specir.visual.compilers.matrix     import MatrixCompiler
from specir.visual.compilers.reflection import ReflectionCompiler
from specir.visual.spec_models import ReflectionDiagram
from specir.visual.exceptions import CompileError
from specir.visual.spec_models import ClassDiagram
from specir.visual.compilers.class_diagram import ClassCompiler


def compile_ir(diagram: BaseDiagram):
    match diagram:
        case ClassDiagram():      return ClassCompiler().compile(diagram)
        case SequenceDiagram():   return SequenceCompiler().compile(diagram)
        case StateDiagram():      return StateCompiler().compile(diagram)
        case ComponentDiagram():  return ComponentCompiler().compile(diagram)
        case ActivityDiagram():   return ActivityCompiler().compile(diagram)
        case DeploymentDiagram(): return DeploymentCompiler().compile(diagram)
        case MatrixDiagram():     return MatrixCompiler().compile(diagram)
        case ReflectionDiagram(): return ReflectionCompiler().compile(diagram)
        case _: raise CompileError(f"No compiler for diagram type: {diagram.type}")
