from __future__ import annotations
from yaml_charts.models.base import BaseDiagram
from yaml_charts.models.sequence   import SequenceDiagram
from yaml_charts.models.state      import StateDiagram
from yaml_charts.models.component  import ComponentDiagram
from yaml_charts.models.activity   import ActivityDiagram
from yaml_charts.models.deployment import DeploymentDiagram
from yaml_charts.models.matrix     import MatrixDiagram
from yaml_charts.compilers.sequence   import SequenceCompiler
from yaml_charts.compilers.state      import StateCompiler
from yaml_charts.compilers.component  import ComponentCompiler
from yaml_charts.compilers.activity   import ActivityCompiler
from yaml_charts.compilers.deployment import DeploymentCompiler
from yaml_charts.compilers.matrix     import MatrixCompiler
from yaml_charts.exceptions import CompileError


def compile_ir(diagram: BaseDiagram):
    match diagram:
        case SequenceDiagram():   return SequenceCompiler().compile(diagram)
        case StateDiagram():      return StateCompiler().compile(diagram)
        case ComponentDiagram():  return ComponentCompiler().compile(diagram)
        case ActivityDiagram():   return ActivityCompiler().compile(diagram)
        case DeploymentDiagram(): return DeploymentCompiler().compile(diagram)
        case MatrixDiagram():     return MatrixCompiler().compile(diagram)
        case _: raise CompileError(f"No compiler for diagram type: {diagram.type}")
