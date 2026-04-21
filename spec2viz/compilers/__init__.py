from __future__ import annotations
from spec2viz.models.base import BaseDiagram
from spec2viz.models.sequence   import SequenceDiagram
from spec2viz.models.state      import StateDiagram
from spec2viz.models.component  import ComponentDiagram
from spec2viz.models.activity   import ActivityDiagram
from spec2viz.models.deployment import DeploymentDiagram
from spec2viz.models.matrix     import MatrixDiagram
from spec2viz.compilers.sequence   import SequenceCompiler
from spec2viz.compilers.state      import StateCompiler
from spec2viz.compilers.component  import ComponentCompiler
from spec2viz.compilers.activity   import ActivityCompiler
from spec2viz.compilers.deployment import DeploymentCompiler
from spec2viz.compilers.matrix     import MatrixCompiler
from spec2viz.exceptions import CompileError


def compile_ir(diagram: BaseDiagram):
    match diagram:
        case SequenceDiagram():   return SequenceCompiler().compile(diagram)
        case StateDiagram():      return StateCompiler().compile(diagram)
        case ComponentDiagram():  return ComponentCompiler().compile(diagram)
        case ActivityDiagram():   return ActivityCompiler().compile(diagram)
        case DeploymentDiagram(): return DeploymentCompiler().compile(diagram)
        case MatrixDiagram():     return MatrixCompiler().compile(diagram)
        case _: raise CompileError(f"No compiler for diagram type: {diagram.type}")
