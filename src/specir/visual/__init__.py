"""specIR's visual layer: the intermediate representation, its compilers and the projections of
the graph to it (IR11); its renderers, mermaid linter, JSON Schema export, packaged resources and the
render, lint and schema commands are in `specir.visual.renderers`, `lint_mermaid`, `schema`,
`templates/`, `render_file` and `commands` (IR12); the HTML catalog of diagrams, its atoms and its
annotations saved with `sldb serve` are in `specir.visual.catalog` (IR13b). IR13d extends this module
with the full public API of the layer.

The spec models of the eight diagram types are sldb's (D3) and are only re-exported here for the
visual layer's callers; nothing of them is defined in specIR. `load_spec` and `validate_spec` are
used from `sldb.api.notations` directly, without a wrapper. So are syncing a spec to the store
(`SpecSync`, `sync_spec`; `sldb notations sync --spec`, D1) and generating a component spec from a
graph, a snapshot or the Python AST (`component_spec_from_graph`, `component_spec_from_python`,
`write_component_spec`; `sldb notations from-graph`, D2): specIR defines none of them (IR13a). So are
the matching of atoms with diagram elements and the coverage per view (`sldb.api.matching`, D4) and
the catalog's path rule, validation and sync (`sldb.api.notations`, `sldb notations sync --catalog`,
D1).

The public API of the layer (IR13d) covers what the `spec2viz` package exported: `compile_ir`,
`render` (with `RENDERER_MAP`, `EXT_MAP` and `DEFAULT_RENDERER`), `render_to_file` and its provenance
header (`with_provenance`, `provenance_header`, `provenance_text`), `json_schema` and
`write_json_schema`, plus the mermaid linter (`lint_mermaid`, `assert_mermaid_ok`) and the catalog page
(`render_catalog`, `build_catalog`, `AnnotationsTarget`). spec2viz's `load` and `validate` are sldb's
`load_spec` and `validate_spec` (`sldb.api.notations`), used directly and not re-exported here. The
`specir` command is `specir.cli`."""

from specir.visual.catalog import AnnotationsTarget, build_catalog, render_catalog
from specir.visual.compilers import compile_ir
from specir.visual.compilers.activity import ActivityCompiler
from specir.visual.compilers.class_diagram import ClassCompiler
from specir.visual.compilers.component import ComponentCompiler
from specir.visual.compilers.deployment import DeploymentCompiler
from specir.visual.compilers.matrix import MatrixCompiler
from specir.visual.compilers.reflection import ReflectionCompiler
from specir.visual.compilers.sequence import SequenceCompiler
from specir.visual.compilers.state import StateCompiler
from specir.visual.exceptions import CompileError, RenderError, Spec2VizError
from specir.visual.ir import *  # noqa: F401,F403 (the IR dataclasses, see specir.visual.ir.__all__)
from specir.visual.ir import __all__ as _IR
from specir.visual.lint_mermaid import MermaidLintError, assert_mermaid_ok, lint_mermaid
from specir.visual.normalize import differences, equivalent, normalize
from specir.visual.projections import component_from_view, from_spec_doc, state_from_view, view_graph
from specir.visual.render_file import provenance_header, provenance_text, render_to_file, with_provenance
from specir.visual.renderers import DEFAULT_RENDERER, EXT_MAP, RENDERER_MAP, render
from specir.visual.schema import json_schema, write_json_schema
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
    "CompileError", "RenderError", "Spec2VizError",
    "differences", "equivalent", "normalize",
    "component_from_view", "from_spec_doc", "state_from_view", "view_graph",
    "SPEC_MODELS", "ActivityDiagram", "BaseDiagram", "ClassDiagram", "ComponentDiagram", "DeploymentDiagram",
    "EnforcementArtifact", "EnforcementFact", "MatrixDiagram", "ReflectionDiagram", "SequenceDiagram",
    "StateDiagram",
    # IR13d: the rest of what the spec2viz package exported, the linter and the catalog page.
    "DEFAULT_RENDERER", "EXT_MAP", "RENDERER_MAP", "render",
    "provenance_header", "provenance_text", "render_to_file", "with_provenance",
    "json_schema", "write_json_schema",
    "MermaidLintError", "assert_mermaid_ok", "lint_mermaid",
    "AnnotationsTarget", "build_catalog", "render_catalog",
]
