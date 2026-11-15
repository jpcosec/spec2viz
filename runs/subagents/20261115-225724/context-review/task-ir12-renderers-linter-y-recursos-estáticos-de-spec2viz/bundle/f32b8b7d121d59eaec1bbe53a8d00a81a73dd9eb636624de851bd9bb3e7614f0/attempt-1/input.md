FILE:desk/tasks/task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz.md
---
sldb:
  by: agent
  at: '2026-11-15T22:53:39Z'
  authority: generated
  via: save_document_payload
id: task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir11-compiladores-y-proyecciones-de-spec2viz
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/__init__.py
- src/specir/visual/exceptions.py
- src/specir/visual/ir.py
- src/specir/visual/projections.py
- src/specir/visual/spec_models.py
- src/specir/visual/notation_style.py
- src/specir/visual/renderers/__init__.py
- src/specir/visual/renderers/mermaid.py
- src/specir/visual/renderers/plantuml.py
- src/specir/visual/renderers/d2.py
- src/specir/visual/renderers/vega.py
- src/specir/visual/renderers/bpmn.py
- src/specir/visual/renderers/bpmn_palette.py
- src/specir/visual/renderers/bpmn_viewer.py
- src/specir/visual/renderers/tree.py
- src/specir/visual/renderers/graph_html.py
- src/specir/visual/renderers/antonia_html.py
- src/specir/visual/renderers/json_out.py
- src/specir/visual/renderers/class_diagram.py
- src/specir/visual/renderers/view_mermaid.py
- src/specir/visual/lint_mermaid.py
- src/specir/visual/schema.py
- src/specir/visual/render_file.py
- src/specir/visual/commands.py
- src/specir/visual/templates/default.html
- src/specir/visual/templates/vendor/bpmn-js/LICENSE
- src/specir/visual/templates/vendor/bpmn-js/README.md
- src/specir/visual/templates/vendor/bpmn-js/bpmn-js.css
- src/specir/visual/templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js
- src/specir/visual/templates/vendor/bpmn-js/diagram-js.css
- pyproject.toml
- docs/spec2viz/matriz-de-cobertura.md
- tests/test_imports.py
- tests/visual/render_parity.py
- tests/visual/goldens/spec2viz-2de1056-renders.json
- tests/visual/goldens/spec2viz-2de1056-lint.json
- tests/visual/goldens/spec2viz-2de1056-schema.json
- tests/visual/fixtures/spec2viz/examples/schema/spec2viz.schema.json
- tests/visual/fixtures/spec2viz/examples/schema/sequence.schema.json
- tests/visual/fixtures/spec2viz/examples/schema/class.schema.json
- tests/visual/test_renderers.py
- tests/visual/test_render_parity.py
- tests/visual/test_render_cases.py
- tests/visual/test_render_commands.py
- tests/visual/test_bpmn.py
- tests/visual/test_lint_mermaid.py
- tests/visual/test_schema.py
- tests/visual/test_resources.py
- tests/visual/test_visual_names.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
from_drawer: desk/drawer/tasks/task-ir12-renderers-linter-y-recursos-estaticos-de-spec2viz.md
---

# IR12 Renderers, linter y recursos estáticos de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Lo que los usuarios de spec2viz consumen son archivos renderizados. Para retirar spec2viz, specIR tiene que producir cada formato, no solo los que alguien usa hoy.

## Goal

_Describe the concrete result this task must produce._

specIR produce todos los formatos de salida de spec2viz a partir de la representación intermedia, con paridad verificable, y distribuye los recursos que esos formatos necesitan.

## Scope

_State what is in scope and what is out of scope._

Dentro: renderizadores Mermaid, PlantUML, D2, Vega, BPMN y su visor, árbol, HTML de grafo, antonia HTML y salida JSON; linter de Mermaid; export de JSON Schema de specs y de catálogos; recursos empaquetados: plantillas HTML, bpmn-js y los que requiera cada formato; comandos equivalentes a render, lint y schema. Cada pieza se migra tal cual o se reemplaza, según la matriz de cobertura.
Fuera: compiladores; sincronización al store, catálogos y consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulos de renderizado en el paquete specIR que consumen la representación intermedia de la tarea de compiladores; paridad medida con los golden y pruebas de renderizadores de spec2viz ejecutados contra specIR.

Precisiones (preflight): (1) La matriz es docs/spec2viz/matriz-de-cobertura.md (IR07); las filas de esta tarea son SV-A14 (RenderError), SV-A15 y SV-A16 (JSON Schema), SV-C01 a SV-C15 (renderers), SV-D01 (linter), SV-J04 y SV-J05 (bpmn-js y plantilla) y la parte de plantilla de SV-G08; una diferencia se declara en la condición de retiro de su fila, con la prueba que la cubre. La matriz no acredita filas: las cita IR13. (2) La representación intermedia es la de IR11: src/specir/visual/ir.py (dataclasses de spec2viz/ir.py tal cual) y compile_ir de src/specir/visual/compilers; los specs se cargan y validan con sldb.api.notations.load_spec/validate_spec (D3). (3) El corpus de paridad es el de IR11: los specs de spec2viz 2de1056 en tests/visual/fixtures/spec2viz/ con sus rutas; los 36 que validan, dibujados con los nueve renderers, más la página del visor BPMN de cada actividad; los resultados de spec2viz se guardan en tests/visual/goldens/spec2viz-2de1056-renders.json, sus hallazgos de lint en spec2viz-2de1056-lint.json y su JSON Schema en spec2viz-2de1056-schema.json (tests/visual/render_parity.py los regenera y es, junto a parity.py, el único que importa spec2viz). (4) Recursos: los de spec2viz/templates/ copiados byte a byte: default.html y vendor/bpmn-js (bpmn-js 18.31.1, licencia bpmn.io en LICENSE, procedencia en README.md); se declaran como package-data en pyproject.toml. (5) Comandos: src/specir/visual/commands.py migra de spec2viz/cli.py los grupos diagram (render, lint, schema y validate, que es el comando que nombra la cabecera de procedencia) y catalog (schema) con los mismos argumentos y opciones; el script specir apunta a ese grupo hasta que IR13d monte src/specir/cli.py con la taxonomía completa y los alias de primer nivel. render_to_file y la cabecera de procedencia (SV-J03) se migran aquí porque diagram render los necesita; IR13d los expone en la API pública. (6) El selector son los nueve valores de DIAGRAM_RENDERERS de spec2viz/cli.py (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json) con sus extensiones (EXT_MAP) y el renderer por defecto de cada IR (DEFAULT_RENDERER).
Carencia de sldb (pedida a su desk): sldb.api no exporta resolve_style, load_palette ni NotationError (están en sldb.notations), ni AnyDiagram, DiagramType y DiagramStoreEnvelope (en sldb.models.notation.diagram_specs). Hasta que lo haga, src/specir/visual/notation_style.py es el único módulo que importa de sldb.notations y src/specir/visual/spec_models.py, que ya era el de los modelos de D3, añade los tres modelos; tests/test_imports.py acota ambas excepciones.
Transición sin estado de origen (pendiente de IR11): ANY_STATE = "*" pasa a ser parte del contrato de la IR (src/specir/visual/ir.py); mermaid, plantuml y d2 la dibujan saliendo de un único pseudoestado punteado con rótulo «*» (id __any_state), distinto del estado inicial, y un StateIR sin estado inicial no dibuja la flecha inicial. Ningún spec de spec2viz produce esos casos, así que la paridad no cambia.

## Validation

_List the checks required before this task can close._

- Por cada renderizador, los fixtures de spec2viz producen en specIR una salida idéntica a su golden, o la diferencia está declarada en la matriz de cobertura con su prueba equivalente.
- El linter de Mermaid reporta en specIR los mismos hallazgos que en spec2viz sobre los fixtures de lint.
- El JSON Schema exportado por specIR para specs y catálogos es igual al de spec2viz, o la diferencia está declarada.
- El HTML del visor BPMN y el HTML de grafo generados abren sin recursos externos faltantes (prueba de empaquetado).
- Todos los valores del selector de renderizador de spec2viz existen en specIR.
- El paquete no importa spec2viz.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas de paridad de renderizadores, linter y schema pasan en specIR y sus filas de la matriz de cobertura tienen la condición de retiro cumplida.

FILE:desk/rituals/phase.md
---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of IR tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for IR.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when IR changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a IR task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:48Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-specir-solo-usa-la-api-pública-de-sldb
status: active
summary: Dependencias permitidas del paquete specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: specIR solo usa la API pública de SLDB

## What

_Define the context or guardrail this pill carries._

El código de specIR importa de SLDB únicamente sldb.api. No importa sldb.store, sldb.core ni otros módulos internos, y no importa pron ni spec2viz.

## Why

_Explain why this context matters for safe execution._

specIR es un repo periférico sobre SLDB; pron quedó descartado como base y spec2viz va a retirarse. Acoplarse a módulos internos de SLDB es lo que desfasó a pron.

## When

_Describe when an agent should apply this pill._

En toda tarea que escriba o modifique código bajo src/specir/ o tests/.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/ y tests/; lo comprueba tests/test_imports.py.

## How

_Describe the correct way to apply this guidance._

Si falta una operación general, se documenta la carencia y se pide en el desk de SLDB con deskops message send --to sldb; la tarea se detiene en ese punto si la carencia la bloquea.

## How Not

_Describe the shortcut or failure mode to avoid._

No reimplementar en specIR lo que es general de SLDB; no copiar código de pron ni de spec2viz como dependencia; no alcanzar módulos internos de SLDB aunque funcione.

FILE:desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:49Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo
status: active
summary: Mandato anti-mock para toda tarea de código de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: sin mocks ni datos fabricados; detenerse ante un bloqueo

## What

_Define the context or guardrail this pill carries._

El entregable no contiene mocks, stubs, constantes falsas, no-ops, datos fabricados ni atajos TODO. Las pruebas validan la salida real contra un store, fixture o golden real, no contra literales que duplican la respuesta esperada.

## Why

_Explain why this context matters for safe execution._

Un cierre verde con datos falsos oculta que la capacidad no existe; el valor de specIR es que el grafo refleje el sistema real.

## When

_Describe when an agent should apply this pill._

En toda tarea de código, durante la implementación y la validación.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/specir/, tests/ y tests/fixtures/.

## How

_Describe the correct way to apply this guidance._

Las pruebas corren contra un store SLDB de prueba real y contra fixtures que son aplicaciones o specs reales. Si una dependencia real no está disponible, el ejecutor se detiene y reporta el bloqueo.

## How Not

_Describe the shortcut or failure mode to avoid._

No simular SLDB, el SDK de MCP ni una aplicación de fixture; no escribir pruebas que solo comparan con un literal inline; no marcar como hecho algo que solo está esbozado.

FILE:desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas
status: active
summary: Cómo se acredita la cobertura de una capacidad de spec2viz.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: la paridad con spec2viz se demuestra con sus pruebas

## What

_Define the context or guardrail this pill carries._

Una capacidad de spec2viz se considera cubierta solo cuando la prueba o golden correspondiente de spec2viz pasa contra specIR, o cuando su fila de la matriz de cobertura declara un reemplazo con una prueba equivalente que pasa.

## Why

_Explain why this context matters for safe execution._

El objetivo es retirar spec2viz; declarar paridad sin prueba dejaría funcionalidades perdidas al retirarlo.

## When

_Describe when an agent should apply this pill._

En toda tarea que migre o reemplace una capacidad de spec2viz, y al evaluar el gate de retiro.

## Where

_Name the files, surfaces, or scope this pill applies to._

tests/visual/ en specIR; como referencia de solo lectura, spec2viz/tests/ y la matriz docs/spec2viz/matriz-de-cobertura.md.

## How

_Describe the correct way to apply this guidance._

Portar los fixtures y golden de spec2viz a tests/ de specIR y ejecutarlos; registrar en la matriz, por fila, la prueba que acredita la cobertura.

## How Not

_Describe the shortcut or failure mode to avoid._

No declarar una fila como cubierta porque otra herramienta la sustituya de hecho; no descartar una capacidad por falta de uso; no modificar un golden para que la prueba pase.

FILE:desk/atoms/atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:35Z'
  authority: generated
  via: create_document
id: atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
title: specIR reemplaza a spec2viz y cubre todas sus funciones
five_wh_one_plus: when
tags:
- system:specir
- system:spec2viz
- topic:migracion
---

# specIR reemplaza a spec2viz y cubre todas sus funciones

## Answer

spec2viz nació aparte porque SLDB no tenía grafos; ahora los tiene. specIR incorporará la capa visual y debe cubrir todas las funcionalidades de spec2viz; cuando las cubra, spec2viz se retira. Ninguna funcionalidad se da por descartada porque otra herramienta la sustituya de hecho: cada una se cubre migrándola tal cual, reemplazándola por otra arquitectura o experiencia con resultado equivalente, o exponiendo desde specIR lo que ya vive en SLDB. En los tres casos specIR responde por el camino de retiro. No es un consumidor permanente de spec2viz. Decisión del dueño del proyecto, 2026-11-11.

FILE:src/specir/visual/__init__.py
"""specIR's visual layer: the intermediate representation, its compilers and the projections of
the graph to it (IR11); its renderers, mermaid linter, JSON Schema export, packaged resources and the
render, lint and schema commands are in `specir.visual.renderers`, `lint_mermaid`, `schema`,
`templates/`, `render_file` and `commands` (IR12). IR13d extends this module with the full public API of the layer.

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
from specir.visual.exceptions import CompileError, RenderError, Spec2VizError
from specir.visual.ir import *  # noqa: F401,F403 (the IR dataclasses, see specir.visual.ir.__all__)
from specir.visual.ir import __all__ as _IR
from specir.visual.normalize import differences, equivalent, normalize
from specir.visual.projections import component_from_view, from_spec_doc, state_from_view, view_graph
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
]

FILE:src/specir/visual/exceptions.py
"""Errors of specIR's visual layer, migrated from `spec2viz.exceptions` with their names.

`ParseError`, `ValidationError` and its typed subclasses are sldb's (D3, `sldb.notations.exceptions`)
and are not defined here. IR11 brought the root and `CompileError`; IR12 adds `RenderError`."""


class Spec2VizError(Exception):
    """Root of the errors of the visual layer (compilation and rendering)."""


class CompileError(Spec2VizError):
    """A spec that no compiler of specIR turns into an intermediate representation."""


class RenderError(Spec2VizError):
    """An intermediate representation that a renderer cannot draw, or rendered text that breaks
    its engine (`specir.visual.lint_mermaid.MermaidLintError`)."""


__all__ = ["Spec2VizError", "CompileError", "RenderError"]

FILE:src/specir/visual/ir.py
"""Intermediate representation (IR) dataclasses — one per diagram type (migrated from `spec2viz.ir`).

Each IR is a graphics-ready, renderer-agnostic view of a diagram.
Compilers produce IRs; renderers consume them. The reflection compiler produces sldb's
`EnforcementArtifact` (D3), which is not redefined here.
"""

from __future__ import annotations
from dataclasses import dataclass, field


# Class members remain structured through compilation; renderers own syntax.
@dataclass
class ClassParameterIR:
    name: str
    type: str


@dataclass
class ClassAttributeIR:
    name: str
    type: str
    visibility: str
    static: bool


@dataclass
class ClassMethodIR:
    name: str
    parameters: list[ClassParameterIR]
    returns: str
    visibility: str
    abstract: bool
    static: bool


@dataclass
class ClassNodeIR:
    id: str
    label: str
    kind: str
    attributes: list[ClassAttributeIR]
    methods: list[ClassMethodIR]


@dataclass
class ClassRelationIR:
    from_: str
    to: str
    relation: str
    label: str | None
    from_multiplicity: str | None
    to_multiplicity: str | None


@dataclass
class ClassPackageIR:
    id: str
    label: str
    kind: str
    contains: list[str] = field(default_factory=list)


@dataclass
class ClassIR:
    title: str
    direction: str
    classes: list[ClassNodeIR]
    relations: list[ClassRelationIR]
    packages: list[ClassPackageIR] = field(default_factory=list)
    style_kinds: dict[str, dict] = field(default_factory=dict)

    def package_path(self, package_id: str) -> list[str]:
        """Los paquetes desde la raiz hasta `package_id` (incluido)."""
        parent = {child: p.id for p in self.packages for child in p.contains}
        path = [package_id]
        while path[0] in parent:
            path.insert(0, parent[path[0]])
        return path

    def package_of(self, class_id: str) -> str | None:
        return next((p.id for p in self.packages if class_id in p.contains), None)


# ── Matrix ────────────────────────────────────────────────────────────────────


@dataclass
class Stage:
    id: str
    index: int
    label: str
    view: str | None = None


@dataclass
class Row:
    id: str
    label: str
    row: int
    depth: int


@dataclass
class Span:
    component: str
    row: int
    start: int
    end: int
    kind: str


@dataclass
class MatrixIR:
    title: str
    stages: list[Stage]
    rows: list[Row]
    spans: list[Span]


# ── Sequence ──────────────────────────────────────────────────────────────────


@dataclass
class Participant:
    id: str
    kind: str = "component"


@dataclass
class Message:
    index: int = 0
    from_: str = ""
    to: str = ""
    message: str = ""
    kind: str = "sync"
    condition: str | None = None
    group: str | None = None


@dataclass
class SequenceIR:
    title: str
    participants: list[Participant]
    messages: list[Message]


# ── State ─────────────────────────────────────────────────────────────────────


@dataclass
class StateNode:
    id: str
    label: str
    contains: list[str] | None = None


#: The `from_` of a transition whose source state is not named (specIR's state projection, IR11:
#: the graph does not say which state an operation leaves). The renderers draw it as one pseudostate
#: labelled `*` that is not the initial state (IR12).
ANY_STATE = "*"


@dataclass
class Transition:
    from_: str
    to: str
    on: str
    guard: str | None = None
    action: str | None = None


@dataclass
class StateIR:
    title: str
    entity: str
    initial: str
    states: list[StateNode]
    transitions: list[Transition]


# ── Component ─────────────────────────────────────────────────────────────────


@dataclass
class ComponentNode:
    id: str
    label: str
    kind: str
    contains: list[str] = field(default_factory=list)
    href: str | None = None


@dataclass
class ComponentEdge:
    from_: str
    to: str
    relation: str
    label: str | None = None


@dataclass
class ComponentIR:
    title: str
    nodes: list[ComponentNode]
    edges: list[ComponentEdge]
    style_kinds: dict[str, dict] = field(default_factory=dict)


# ── Activity ──────────────────────────────────────────────────────────────────


@dataclass
class ActivityStep:
    id: str
    label: str
    kind: str = "action"
    next: str | None = None
    branches: dict[str, str] = field(default_factory=dict)
    partition: str | None = None
    notes: str | None = None
    tone: str | None = None
    detail: str | None = None
    group: str | None = None


@dataclass
class ActivityGroup:
    id: str
    label: str
    tone: str | None = None
    detail: str | None = None


@dataclass
class ActivityIR:
    title: str
    start: str
    steps: list[ActivityStep]
    end: str
    style_kinds: dict[str, dict] = field(default_factory=dict)
    groups: dict[str, ActivityGroup] = field(default_factory=dict)


# ── Deployment ────────────────────────────────────────────────────────────────


@dataclass
class DeploymentNode:
    id: str
    label: str
    kind: str
    contains: list[str] = field(default_factory=list)


@dataclass
class DeploymentArtifact:
    id: str
    label: str
    kind: str


@dataclass
class DeploymentConnection:
    from_: str
    to: str
    protocol: str | None = None
    kind: str = "communication"
    label: str | None = None

    @property
    def text(self) -> str:
        """Rotulo de la conexion: label y protocolo; con «deploy»/«manifest» el estereotipo delante."""
        parts = [p for p in (self.label, self.protocol) if p]
        text = " · ".join(parts)
        if self.kind in ("deploy", "manifest"):
            text = f"«{self.kind}» {text}".strip()
        return text


@dataclass
class DeploymentIR:
    title: str
    nodes: list[DeploymentNode]
    artifacts: list[DeploymentArtifact]
    connections: list[DeploymentConnection]
    style_kinds: dict[str, dict] = field(default_factory=dict)


__all__ = [
    "ClassParameterIR", "ClassAttributeIR", "ClassMethodIR", "ClassNodeIR",
    "ClassRelationIR", "ClassIR", "ClassPackageIR",
    "Stage",
    "Row",
    "Span",
    "MatrixIR",
    "Participant",
    "Message",
    "SequenceIR",
    "StateNode",
    "Transition",
    "ANY_STATE",
    "StateIR",
    "ComponentNode",
    "ComponentEdge",
    "ComponentIR",
    "ActivityStep",
    "ActivityGroup",
    "ActivityIR",
    "DeploymentNode",
    "DeploymentArtifact",
    "DeploymentConnection",
    "DeploymentIR",
]

FILE:src/specir/visual/projections.py
"""Projections of the graph to the intermediate representation (IR11).

A diagram of what already exists in the graph is a projection, not a second copy of its entities.
Everything that reads the store is SLDB's public API:

- a projection `ViewDoc` (nodes and relations, no sections) is evaluated by
  `sldb.api.notations.evaluate_projection_view`;
- a composed `ViewDoc` (with sections) is run by `sldb.api.run_view`; its section declarations
  (which relation each row key follows) come from `sldb.api.notations.list_projection_views`;
- a `SpecDoc` with its `SpecNodeDoc` is resolved by `sldb.api.notations.resolve_view`; what the
  resolved view leaves out (the label of each edge, in its `RelationDoc`, and the `contains` of
  each `SpecNodeDoc`) is read with `sldb.api.load_runtime_documents`.

What specIR adds is only the transformation of those results into the nodes and edges of one
diagram type:

- component: the evaluated graph goes through `sldb.api.notations.component_spec_from_graph`
  (D2, the same generator as `sldb notations from-graph`), the spec it returns is validated as
  sldb's `ComponentDiagram` and compiled by specIR's component compiler. Node ids are D2's safe
  ids (`document_<Model>_<name>`), labels are the documents' titles and kinds their models.
- state: the states are the `StateDoc` of the view, the entity is the `DomainEntityDoc` they name
  (`StateDoc.entity`), and every `transitions` edge (a `DomainOperationDoc` that moves the entity
  into a state) is a transition `on` the operation's title. specIR's graph does not say which
  state an operation leaves, so the transition's `from_` is `ANY_STATE`; the initial state is the
  only state no operation leads into, and empty when there is not exactly one.

Nothing here writes to the store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.api.notations import (
    component_spec_from_graph,
    evaluate_projection_view,
    list_projection_views,
    node_id,
    resolve_view,
)

from specir.visual.compilers import compile_ir
from specir.visual.exceptions import CompileError
from specir.visual.ir import ANY_STATE, ComponentEdge, ComponentIR, ComponentNode, StateIR, StateNode, Transition
from specir.visual.spec_models import ComponentDiagram, validate_spec

#: The relation D2 nests (`contains: [...]`) instead of drawing.
CONTAINS = "contains"
DOCUMENT = "sldb://document/"
#: What the IR of a SpecDoc lacks against the IR of its YAML, because the store does not keep it.
SPEC_DOC_GAPS = {"StateIR": ("entity",), "ComponentIR": ("style_kinds",)}

Graph = dict[str, Any]


def _store(store: Path | str) -> Path:
    return Path(store)


def _view_payload(store: Path, ref: str) -> dict[str, Any]:
    """The payload of the ViewDoc `ref` (`ViewDoc:<name>` or `<name>`)."""
    name = ref.split(":", 1)[-1]
    for view in list_projection_views(store):
        if view["ref"] == f"ViewDoc:{name}":
            return dict(view["payload"] or {})
    raise CompileError(f"ViewDoc:{name} is not in the store {store}")


def _composed_graph(store: Path, name: str, sections: list[dict[str, Any]], params: dict[str, str] | None) -> Graph:
    """Nodes and edges of a composed view, from `run_view` and the edges its sections declare."""
    result = api.run_view(store, name, params)
    nodes: dict[str, dict[str, Any]] = {}
    edges: set[tuple[str, str, str]] = set()
    for section in sections:
        rows = _rows(result["sections"].get(section["key"], {}))
        for row in rows:
            nodes[node_id(row["model"], row["name"])] = {
                "model": row["model"], "name": row["name"], "title": (row.get("fields") or {}).get("title") or row["name"],
            }
        for declared in section.get("edges") or []:
            key = declared.get("as") or f"{declared['direction']}:{declared['relation']}"
            for row in rows:
                here = node_id(row["model"], row["name"])
                for other in row.get(key) or []:
                    there = other if other.startswith(DOCUMENT) else f"{DOCUMENT}{other}"
                    pair = (here, there) if declared["direction"] == "out" else (there, here)
                    edges.add((*pair, declared["relation"]))
    kept = sorted((s, t, r) for s, t, r in edges if s in nodes and t in nodes)
    return {"title": result["view"], "nodes": nodes, "edges": kept}


def _rows(section: dict[str, Any]) -> list[dict[str, Any]]:
    if "groups" in section:
        return [row for group in section["groups"] for row in group["rows"]]
    return list(section.get("rows") or [])


def view_graph(store: Path | str, ref: str, params: dict[str, str] | None = None) -> Graph:
    """`{title, nodes: {node id: {model, name, title}}, edges: [(source, target, relation)]}` of the
    ViewDoc `ref`, evaluated by SLDB: `run_view` when it has sections, else
    `evaluate_projection_view`. Node ids are SLDB's `sldb://document/<Model>:<name>`."""
    store = _store(store)
    payload = _view_payload(store, ref)
    if payload.get("sections"):
        graph = _composed_graph(store, payload.get("name") or ref.split(":", 1)[-1], payload["sections"], params)
    else:
        result = evaluate_projection_view(store, f"ViewDoc:{ref.split(':', 1)[-1]}")
        graph = {
            "nodes": {n["id"]: {"model": n["model"], "name": n["name"], "title": n["title"], "payload": n.get("payload") or {}} for n in result["nodes"]},
            "edges": sorted((e["source"], e["target"], e["relation_type"]) for e in result["edges"]),
        }
    graph["title"] = payload.get("title") or payload.get("name") or ref
    return graph


def component_spec_of(graph: Graph, spec_id: str) -> dict[str, Any]:
    """The component spec of an evaluated view, by D2's `component_spec_from_graph`."""
    nodes = {nid: "document" for nid in graph["nodes"]}
    attrs = {nid: {"label": node["title"], "kind": node["model"]} for nid, node in graph["nodes"].items()}
    relations = sorted({r for _, _, r in graph["edges"]})
    return component_spec_from_graph(
        nodes, graph["edges"], relations=relations, exclude_relations=() if not relations else None,
        spec_id=spec_id, title=graph["title"], source=f"ViewDoc:{spec_id}", attrs=attrs,
    )


def component_from_view(store: Path | str, ref: str, params: dict[str, str] | None = None) -> ComponentIR:
    """The ComponentIR of a ViewDoc: its graph as D2's component spec, validated by sldb and compiled."""
    name = ref.split(":", 1)[-1]
    diagram = ComponentDiagram.model_validate(component_spec_of(view_graph(store, ref, params), name))
    validate_spec(diagram)
    return compile_ir(diagram)


def state_from_view(store: Path | str, ref: str, params: dict[str, str] | None = None) -> StateIR:
    """The StateIR of a ViewDoc that selects StateDoc, their DomainEntityDoc and the
    DomainOperationDoc that lead to them (see the module docstring)."""
    graph = view_graph(store, ref, params)
    nodes = graph["nodes"]
    states = sorted((nid for nid, n in nodes.items() if n["model"] == "StateDoc"), key=lambda nid: nodes[nid]["name"])
    if not states:
        raise CompileError(f"{ref} selects no StateDoc: it is not a state diagram")
    entities = {(nodes[s].get("payload") or {}).get("entity") or _referenced(graph, s) for s in states} - {None, ""}
    if len(entities) != 1:
        raise CompileError(f"{ref}: the states name {len(entities)} entities, a state diagram draws one: {sorted(entities)}")
    entity_id = next(iter(entities))
    entity_id = entity_id if entity_id.startswith(DOCUMENT) else f"{DOCUMENT}{entity_id}"
    entity = nodes[entity_id]["title"] if entity_id in nodes else entity_id[len(DOCUMENT):]
    transitions = [
        Transition(from_=ANY_STATE, to=nodes[t]["name"], on=nodes[s]["title"])
        for s, t, r in graph["edges"] if r == "transitions" and t in states and s in nodes
    ]
    entered = {t.to for t in transitions}
    initial = [nodes[s]["name"] for s in states if nodes[s]["name"] not in entered]
    return StateIR(
        title=graph["title"], entity=entity, initial=initial[0] if len(initial) == 1 else "",
        states=[StateNode(id=nodes[s]["name"], label=nodes[s]["title"]) for s in states],
        transitions=transitions,
    )


def _referenced(graph: Graph, state: str) -> str | None:
    """The DomainEntityDoc a state references (its `references` edge), when the payload lacks it."""
    return next((t for s, t, r in graph["edges"] if s == state and r == "references"), None)


def _spec_documents(store: Path, view: dict[str, Any]) -> tuple[dict[str, Any], dict[str, list[str]]]:
    """What `resolve_view` leaves out and the store keeps: the `notes` of each RelationDoc the view
    names (the spec's edge label) and the `contains` of each SpecNodeDoc, as element ids."""
    links = {link["doc"].split(":", 1)[-1] for link in view["links"] if link.get("doc")}
    nodes = {node["doc"].split(":", 1)[-1]: node["element"] for node in view["nodes"]}
    prefix = f"SpecNodeDoc:{view['spec'].split(':', 1)[-1]}."
    notes: dict[str, Any] = {}
    contains: dict[str, list[str]] = {}
    for document in api.load_runtime_documents(store, None, include_linked=False):
        payload = document.payload or {}
        if document.model_name == "RelationDoc" and document.name in links:
            notes[document.name] = payload.get("notes")
        elif document.model_name == "SpecNodeDoc" and document.name in nodes:
            contains[nodes[document.name]] = [ref[len(prefix):] if ref.startswith(prefix) else ref for ref in payload.get("contains") or []]
    return notes, contains


def from_spec_doc(store: Path | str, spec_ref: str) -> ComponentIR | StateIR:
    """The IR of a SpecDoc and its SpecNodeDoc, from `resolve_view` (component and state specs).

    It equals the IR compiled from the spec's YAML except in what SpecSync (sldb, D1) does not keep
    in the store: a state spec's `entity` and a spec's `style.kinds` are fields of the spec, not
    elements, and the SpecDoc has neither. So the StateIR of a SpecDoc has an empty `entity` and
    its ComponentIR an empty `style_kinds` (`SPEC_DOC_GAPS`)."""
    store = _store(store)
    view = resolve_view(store, spec_ref)
    kind = view["diagram_type"]
    if kind not in ("component", "state"):
        raise CompileError(f"{view['spec']} is a `{kind}` spec; specIR materializes component and state SpecDoc")
    elements = {n["doc"]: n["element"] for n in view["nodes"]}
    notes, contains = _spec_documents(store, view)
    links = [
        (elements[link["source"]], elements[link["target"]], link)
        for link in sorted(view["links"], key=lambda l: l["order"]) if link["relation"] != CONTAINS
    ]
    if kind == "component":
        nodes = [
            ComponentNode(id=n["element"], label=n["title"] or n["element"], kind=n["kind"],
                          contains=contains.get(n["element"], []), href=(n.get("data") or {}).get("href"))
            for n in view["nodes"]
        ]
        edges = [
            ComponentEdge(from_=source, to=target, relation=link["relation"], label=notes.get(link["doc"].split(":", 1)[-1]) or None)
            for source, target, link in links
        ]
        return ComponentIR(title=view["title"], nodes=nodes, edges=edges)
    transitions = [
        Transition(from_=source, to=target, on=(link.get("data") or {}).get("on", ""),
                   guard=(link.get("data") or {}).get("guard"), action=(link.get("data") or {}).get("action"))
        for source, target, link in links
    ]
    initial = next((n["element"] for n in view["nodes"] if (n.get("data") or {}).get("initial")), "")
    states = [StateNode(id=n["element"], label=n["title"], contains=contains.get(n["element"]) or None) for n in view["nodes"]]
    return StateIR(title=view["title"], entity="", initial=initial, states=states, transitions=transitions)


__all__ = [
    "ANY_STATE", "SPEC_DOC_GAPS", "component_from_view", "component_spec_of", "from_spec_doc", "state_from_view", "view_graph",
]

FILE:src/specir/visual/spec_models.py
"""The spec models of the eight diagram types, taken from SLDB (D3), never defined here.

The models, their loading and their validation live in sldb (`sldb.models.notation.diagram_specs`,
with `load_spec` and `validate_spec` in `sldb.api.notations`). `sldb.api.notations` exports the two
functions but not the model classes yet, so this module is the only one of specIR that reaches
`sldb.models.notation.diagram_specs` (tests/test_imports.py allows it here and nowhere else). IR12
adds the union of the eight types (`AnyDiagram`), `DiagramType` and the catalog envelope
(`DiagramStoreEnvelope`), which the JSON Schema export needs. When
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
from sldb.models.notation.diagram_specs.base import BaseDiagram, DiagramType
from sldb.models.notation.diagram_specs.catalog import DiagramStoreEnvelope
from sldb.models.notation.diagram_specs.loader import AnyDiagram
from sldb.models.notation.diagram_specs.reflection import EnforcementArtifact, EnforcementFact

#: The eight diagram spec models, in the order spec2viz's `compile_ir` dispatched them.
SPEC_MODELS = (
    ClassDiagram, SequenceDiagram, StateDiagram, ComponentDiagram,
    ActivityDiagram, DeploymentDiagram, MatrixDiagram, ReflectionDiagram,
)

__all__ = [
    "ActivityDiagram", "AnyDiagram", "BaseDiagram", "DiagramStoreEnvelope", "DiagramType", "ClassDiagram", "ComponentDiagram", "DeploymentDiagram",
    "EnforcementArtifact", "EnforcementFact", "MatrixDiagram", "ReflectionDiagram", "SPEC_MODELS",
    "SequenceDiagram", "StateDiagram", "load_spec", "validate_spec",
]

FILE:src/specir/visual/notation_style.py
"""Style resolution and the error root of sldb's notations, taken from SLDB, never defined here.

The renderers color elements with the one precedence that sldb owns (glyph > `style.kinds` of the
spec > palette, `sldb.notations.resolve_style`) and write text in the ink of sldb's builtin
`default` palette (`sldb.notations.load_palette`). The commands report sldb's loading and
validation errors (`sldb.notations.NotationError`, the root of `ParseError` and `ValidationError`).
`sldb.api` does not export these three yet (asked to sldb's desk), so this module is the only one of
specIR that reaches `sldb.notations` (tests/test_imports.py allows it here and nowhere else). When
sldb exports them from `sldb.api.notations`, only these imports change."""

from __future__ import annotations

from functools import lru_cache

from sldb.notations import NotationError, load_palette, resolve_style


@lru_cache(maxsize=1)
def default_ink() -> dict[str, str]:
    """The text color (`{light, dark}`) of sldb's builtin `default` palette."""
    return load_palette().ink.model_dump()


__all__ = ["NotationError", "default_ink", "resolve_style"]

FILE:src/specir/visual/renderers/__init__.py
"""Render dispatch: the nine renderers of spec2viz, by name, with their extensions and the default
renderer per intermediate representation (migrated from `spec2viz.renderers`)."""
from __future__ import annotations
import json
from specir.visual.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, MatrixIR
from specir.visual.spec_models import EnforcementArtifact
from specir.visual.renderers.plantuml import PlantUMLRenderer
from specir.visual.renderers.vega     import VegaRenderer
from specir.visual.renderers.mermaid  import MermaidRenderer
from specir.visual.renderers.d2       import D2Renderer
from specir.visual.renderers.antonia_html import AntoniaHtmlRenderer
from specir.visual.renderers.tree     import TreeRenderer
from specir.visual.renderers.graph_html import GraphRenderer
from specir.visual.renderers.bpmn import BpmnRenderer
from specir.visual.renderers.json_out import JsonRenderer
from specir.visual.exceptions import RenderError
from specir.visual.ir import ClassIR


RENDERER_MAP = {
    "plantuml": PlantUMLRenderer,
    "vega":     VegaRenderer,
    "mermaid":  MermaidRenderer,
    "d2":       D2Renderer,
    "antonia-html": AntoniaHtmlRenderer,
    "tree":     TreeRenderer,
    "graph":    GraphRenderer,
    "bpmn":     BpmnRenderer,
    "json":     JsonRenderer,
}

EXT_MAP = {
    "plantuml": ".puml",
    "vega":     ".vega.json",
    "mermaid":  ".mmd",
    "d2":       ".d2",
    "antonia-html": ".html",
    "tree":     ".tree.html",
    "graph":    ".graph.html",
    "bpmn":     ".bpmn",
    "json":     ".artifact.json",
}

DEFAULT_RENDERER = {
    ClassIR:      "mermaid",
    SequenceIR:   "plantuml",
    StateIR:      "plantuml",
    ComponentIR:  "graph",
    ActivityIR:   "plantuml",
    DeploymentIR: "plantuml",
    MatrixIR:     "vega",
    EnforcementArtifact: "json",
}


def render(ir, renderer: str | None = None) -> str | dict:
    name = renderer or DEFAULT_RENDERER.get(type(ir))
    if name is None:
        raise RenderError(f"No default renderer for {type(ir).__name__}")
    cls = RENDERER_MAP.get(name)
    if cls is None:
        raise RenderError(f"Unknown renderer: {name}")
    return cls().render(ir)


__all__ = ["DEFAULT_RENDERER", "EXT_MAP", "RENDERER_MAP", "JsonRenderer", "render"]

FILE:src/specir/visual/renderers/mermaid.py
from __future__ import annotations
from specir.visual.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR
from specir.visual.exceptions import RenderError
from specir.visual.ir import ANY_STATE, ClassIR
from specir.visual.renderers.class_diagram import render_mermaid_class

# Mermaid sequence arrows. Return must be "-->>" (dashed). "<<--" is NOT
# valid mermaid and breaks the parser in the browser.
_SEQ_ARROW = {"sync": "->>", "async": "-->>", "return": "-->>"}
_PARTICIPANT_KW = {"actor": "actor", "database": "participant", "boundary": "participant"}


def _esc_label(text: object) -> str:
    """Escape text for a quoted mermaid label (node, subgraph, decision, edge).

    Mermaid treats '(', '{', '[' and bare '"' as syntax. Wrapping the label in
    double quotes handles brackets/parens; the inner '"' and angle brackets are
    replaced with mermaid HTML entities so they render literally instead of
    breaking the parser in the browser.
    """
    s = "" if text is None else str(text)
    return (
        s.replace("&", "#amp;")
        .replace('"', "#quot;")
        .replace("<", "#lt;")
        .replace(">", "#gt;")
    )


def _esc_message(text: object) -> str:
    """Escape text for an unquoted sequence message (after the ':').

    Sequence messages are not quoted, so only the HTML-significant angle
    brackets and ampersand must be neutralised; parentheses are safe here.
    ';' ends a statement in mermaid, so it must be escaped as an entity too.
    """
    s = "" if text is None else str(text)
    return (
        s.replace(";", "#59;")
        .replace("&", "#amp;")
        .replace("<", "#lt;")
        .replace(">", "#gt;")
    )


def _kind_classes(style_kinds: dict[str, dict], kind_of: dict[str, str]) -> list[str]:
    """`classDef` y `class` de mermaid desde `style.kinds` del spec (claves neutrales fill,
    stroke), resueltas con la misma precedencia que `resolve_view` (tema claro). Solo los kinds que
    algun elemento usa; sin `style.kinds` neutral no emite nada."""
    from specir.visual.notation_style import default_ink, resolve_style

    neutral = {k: {p: (v[p] if isinstance(v[p], dict) else str(v[p])) for p in ("fill", "stroke") if isinstance(v, dict) and v.get(p)}
               for k, v in style_kinds.items()}
    lines: list[str] = []
    for index, (kind, values) in enumerate((k, v) for k, v in neutral.items() if v):
        members = [eid for eid, ekind in kind_of.items() if ekind == kind]
        if not members:
            continue
        style = resolve_style(None, kind, {kind: values}, None)
        parts = [f"{prop}:{style[prop]['light']}" for prop in ("fill", "stroke") if prop in style]
        parts.append(f"color:{default_ink()['light']}")
        name = f"kind{index}"
        lines.append(f"    classDef {name} {','.join(parts)}")
        lines.append(f"    class {','.join(members)} {name}")
    return lines


# flowcharts con el layout ELK y aristas ortogonales (curva linear sobre los codos que calcula ELK):
# con nodos anidados o un nodo central, dagre cruza y curva las flechas largas y pisa los rotulos
FLOWCHART_CONFIG = "---\nconfig:\n  layout: elk\n  flowchart:\n    curve: linear\n---"


def _flowchart(direction: str = "TD") -> list[str]:
    """Cabecera de un flowchart: frontmatter de config (ELK, curva linear) y `flowchart <dir>`."""
    return [*FLOWCHART_CONFIG.split("\n"), f"flowchart {direction}"]


#: The id of the pseudostate that the transitions without a source state (`ANY_STATE`) leave.
ANY_STATE_ID = "__any_state"


class MermaidRenderer:
    def render(self, ir) -> str:
        match ir:
            case ClassIR():      return render_mermaid_class(ir)
            case SequenceIR():   return self._sequence(ir)
            case StateIR():      return self._state(ir)
            case ComponentIR():  return self._component(ir)
            case ActivityIR():   return self._activity(ir)
            case DeploymentIR(): return self._deployment(ir)
            case _: raise RenderError(f"MermaidRenderer cannot render {type(ir).__name__}")

    def _sequence(self, ir: SequenceIR) -> str:
        lines = ["sequenceDiagram"]
        for p in ir.participants:
            kw = _PARTICIPANT_KW.get(p.kind, "participant")
            lines.append(f"    {kw} {p.id}")
        # Consecutive messages sharing a group render as one labeled block.
        current = None
        for msg in ir.messages:
            if msg.group != current:
                if current is not None:
                    lines.append("    end")
                if msg.group is not None:
                    lines.append("    rect rgba(127, 127, 127, 0.1)")
                    lines.append(f"    Note over {msg.from_},{msg.to}: {_esc_message(msg.group)}")
                current = msg.group
            arrow = _SEQ_ARROW.get(msg.kind, "->>")
            text = msg.message if not msg.condition else f"{msg.message} [{msg.condition}]"
            lines.append(f"    {msg.from_}{arrow}{msg.to}: {_esc_message(text)}")
        if current is not None:
            lines.append("    end")
        return "\n".join(lines)

    def _state(self, ir: StateIR) -> str:
        lines = ["stateDiagram-v2"]
        
        state_map = {s.id: s for s in ir.states}
        children_ids = {child for s in ir.states if s.contains for child in s.contains}
        root_states = [s for s in ir.states if s.id not in children_ids]
        
        def render_state(s, indent="    "):
            lines.append(f'{indent}state "{_esc_label(s.label)}" as {s.id}' + (' {' if s.contains else ''))
            if s.contains:
                for child_id in s.contains:
                    if child_id in state_map:
                        render_state(state_map[child_id], indent + "    ")
                lines.append(f'{indent}}}')
                
        for s in root_states:
            render_state(s)
        
        # una transicion sin estado de origen (ANY_STATE) sale de un pseudoestado `*` punteado
        if any(t.from_ == ANY_STATE for t in ir.transitions):
            lines.append(f'    state "{ANY_STATE}" as {ANY_STATE_ID}')
            lines.append(f"    classDef anyState stroke-dasharray:4 4")
            lines.append(f"    class {ANY_STATE_ID} anyState")
        if ir.initial:
            lines.append(f"    [*] --> {ir.initial}")
        for t in ir.transitions:
            label = t.on or ""
            if t.guard:
                label += f" [{t.guard}]"
            source = ANY_STATE_ID if t.from_ == ANY_STATE else t.from_
            lines.append(f"    {source} --> {t.to} : {_esc_message(label)}")
        return "\n".join(lines)

    def _component(self, ir: ComponentIR) -> str:
        lines = _flowchart("TD")
        child_ids = {child for node in ir.nodes for child in node.contains}

        def render_node(node_id, indent="    "):
            node = next((n for n in ir.nodes if n.id == node_id), None)
            if not node:
                lines.append(f"{indent}{node_id}")
                return
            label = _esc_label(node.label or node.id)
            if not node.contains:
                lines.append(f"{indent}{node.id}[\"{label}\"]")
            else:
                lines.append(f"{indent}subgraph {node.id} [\"{label}\"]")
                for child_id in node.contains:
                    render_node(child_id, indent + "    ")
                lines.append(f"{indent}end")

        for node in ir.nodes:
            if node.id not in child_ids:
                render_node(node.id)

        for edge in ir.edges:
            label = edge.label or edge.relation
            if label:
                lines.append(f'    {edge.from_} -->|"{_esc_label(label)}"| {edge.to}')
            else:
                lines.append(f"    {edge.from_} --> {edge.to}")
        lines.extend(_kind_classes(ir.style_kinds, {n.id: n.kind for n in ir.nodes}))
        lines.extend(f'    click {n.id} href "{_esc_label(n.href)}"' for n in ir.nodes if n.href)
        return "\n".join(lines)

    def _activity(self, ir: ActivityIR) -> str:
        lines = [*_flowchart("TD"), "    __start([Start])"]

        def node_lines(step, indent: str) -> list[str]:
            # decision y merge son rombos; una nota es un nodo aparte unido por una linea punteada
            if step.kind in ("decision", "merge"):
                # mermaid no acepta un rombo con rotulo vacio (el merge UML no lleva rotulo)
                out = [f"{indent}{step.id}{{\"{_esc_label(step.label) or ' '}\"}}"]
            else:
                out = [f"{indent}{step.id}[\"{_esc_label(step.label)}\"]"]
            if step.notes:
                out.append(f"{indent}{step.id}__note[\"{_esc_label(step.notes)}\"]:::note")
            return out

        # particiones (swimlanes): un subgraph por particion, en orden de aparicion
        lanes: dict[str, list] = {}
        for step in ir.steps:
            if step.partition:
                lanes.setdefault(step.partition, []).append(step)
        for step in ir.steps:
            if not step.partition:
                lines.extend(node_lines(step, "    "))
        for index, (lane, steps) in enumerate(lanes.items()):
            lines.append(f'    subgraph __lane{index} ["{_esc_label(lane)}"]')
            for step in steps:
                lines.extend(node_lines(step, "        "))
            lines.append("    end")
        lines.append(f"    __end([End])")
        lines.append(f"    __start --> {ir.start}")
        for step in ir.steps:
            if step.kind == "decision":
                for branch, target in step.branches.items():
                    dest = "__end" if target == ir.end else target
                    lines.append(f'    {step.id} -->|"{_esc_label(branch)}"| {dest}')
            elif step.next:
                dest = "__end" if step.next == ir.end else step.next
                lines.append(f"    {step.id} --> {dest}")
        for step in ir.steps:
            if step.notes:
                lines.append(f"    {step.id} -.- {step.id}__note")
        if any(step.notes for step in ir.steps):
            lines.append("    classDef note fill:#fff8c5,stroke:#9a6700,color:#1f2328")
        lines.extend(_kind_classes(ir.style_kinds, {st.id: st.kind for st in ir.steps}))
        return "\n".join(lines)

    def _deployment(self, ir: DeploymentIR) -> str:
        art_map = {a.id: a for a in ir.artifacts}
        node_map = {n.id: n for n in ir.nodes}
        nested = {ref for n in ir.nodes for ref in n.contains if ref in node_map}
        lines = _flowchart("TD")

        def emit(node, indent: str) -> None:
            # un nodo es un subgraph; dentro, sus artefactos y sus nodos hijos (anidados)
            lines.append(f'{indent}subgraph {node.id} ["{_esc_label(node.label)}"]')
            for ref in node.contains:
                if ref in art_map:
                    lines.append(f'{indent}    {ref}["{_esc_label(art_map[ref].label)}"]')
                elif ref in node_map:
                    emit(node_map[ref], indent + "    ")
            lines.append(f"{indent}end")

        for node in ir.nodes:
            if node.id not in nested:
                emit(node, "    ")
        for conn in ir.connections:
            label = conn.text
            arrow = "-.->" if conn.kind in ("deploy", "manifest") else "-->"
            if label:
                lines.append(f'    {conn.from_} {arrow}|"{_esc_label(label)}"| {conn.to}')
            else:
                lines.append(f"    {conn.from_} {arrow} {conn.to}")
        lines.extend(_kind_classes(ir.style_kinds, {**{a.id: a.kind for a in ir.artifacts}, **{n.id: n.kind for n in ir.nodes}}))
        return "\n".join(lines)

FILE:src/specir/visual/renderers/plantuml.py
from __future__ import annotations
from specir.visual.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR
from specir.visual.exceptions import RenderError
from specir.visual.ir import ANY_STATE, ClassIR
from specir.visual.renderers.mermaid import ANY_STATE_ID
from specir.visual.renderers.class_diagram import render_plantuml_class

_PARTICIPANT_KW = {"actor": "actor", "boundary": "boundary", "database": "database"}
_ARROW = {"sync": "->", "async": "->>", "return": "<--"}
_NODE_KW = {"database": "database"}
_DEFAULT_COMPONENT_KIND_STYLES = {
    "core": {"background": "#D8ECFF", "border": "#4C78A8", "font": "#16324F"},
    "boundary": {"background": "#FCECC9", "border": "#D4A73C", "font": "#5E450B"},
    "database": {"background": "#DCEFD8", "border": "#5A9B5A", "font": "#1F4F1F"},
}


class PlantUMLRenderer:
    def render(self, ir) -> str:
        match ir:
            case ClassIR():
                return render_plantuml_class(ir)
            case SequenceIR():
                return self._sequence(ir)
            case StateIR():
                return self._state(ir)
            case ComponentIR():
                return self._component(ir)
            case ActivityIR():
                return self._activity(ir)
            case DeploymentIR():
                return self._deployment(ir)
            case _:
                raise RenderError(f"PlantUMLRenderer cannot render {type(ir).__name__}")

    def _sequence(self, ir: SequenceIR) -> str:
        lines = ["@startuml"]
        for p in ir.participants:
            lines.append(f"{_PARTICIPANT_KW.get(p.kind, 'participant')} {p.id}")
        lines.append("")
        # Consecutive messages sharing a group render as one group block.
        current = None
        for msg in ir.messages:
            if msg.group != current:
                if current is not None:
                    lines.append("end")
                if msg.group is not None:
                    lines.append(f"group {msg.group}")
                current = msg.group
            arrow = _ARROW.get(msg.kind, "->")
            line = f"{msg.from_} {arrow} {msg.to}: {msg.message}"
            if msg.condition:
                line += f"  [{msg.condition}]"
            lines.append(line)
        if current is not None:
            lines.append("end")
        lines.append("@enduml")
        return "\n".join(lines)

    def _state(self, ir: StateIR) -> str:
        lines = ["@startuml"]
        # una transicion sin estado de origen (ANY_STATE) sale de un pseudoestado `*` punteado
        if any(t.from_ == ANY_STATE for t in ir.transitions):
            lines.append(f'state "{ANY_STATE}" as {ANY_STATE_ID} ##[dashed]')
        if ir.initial:
            lines.append(f"[*] --> {ir.initial}")
        lines.append("")
        for t in ir.transitions:
            source = ANY_STATE_ID if t.from_ == ANY_STATE else t.from_
            line = f"{source} --> {t.to} : {t.on}"
            if t.guard:
                line += f" [{t.guard}]"
            if t.action:
                line += f" / {t.action}"
            lines.append(line)
        lines.append("@enduml")
        return "\n".join(lines)

    def _component(self, ir: ComponentIR) -> str:
        lines = ["@startuml"]
        style_kinds = self._resolve_component_kind_styles(ir)
        if style_kinds:
            lines.extend(self._emit_component_kind_styles(style_kinds))
            lines.append("")
        node_map = {node.id: node for node in ir.nodes}
        contained = {
            child_id
            for node in ir.nodes
            for child_id in node.contains
            if child_id in node_map
        }
        for node in ir.nodes:
            if node.id in contained:
                continue
            self._emit_component_node(lines, node, node_map, indent="")
        lines.append("")
        for edge in ir.edges:
            lines.append(f"{edge.from_} --> {edge.to} : {edge.label or edge.relation}")
        lines.append("@enduml")
        return "\n".join(lines)

    def _emit_component_node(
        self,
        lines: list[str],
        node,
        node_map: dict[str, object],
        indent: str,
    ) -> None:
        if node.contains:
            lines.append(
                f'{indent}package "{node.label}" as {node.id} <<{node.kind}>> {{'
            )
            for child_id in node.contains:
                child = node_map.get(child_id)
                if child is None:
                    lines.append(f"{indent}  [{child_id}]")
                    continue
                self._emit_component_node(lines, child, node_map, indent=f"{indent}  ")
            lines.append(f"{indent}}}")
            return

        kw = self._component_keyword(node.kind)
        lines.append(f'{indent}{kw} "{node.label}" as {node.id} <<{node.kind}>>')

    def _component_keyword(self, kind: str) -> str:
        if kind == "boundary":
            return "rectangle"
        if kind == "database":
            return "database"
        return "component"

    def _resolve_component_kind_styles(
        self, ir: ComponentIR
    ) -> dict[str, dict[str, str]]:
        styles = {
            kind: dict(values)
            for kind, values in _DEFAULT_COMPONENT_KIND_STYLES.items()
        }
        for kind, config in ir.style_kinds.items():
            plantuml = config.get("plantuml") if isinstance(config, dict) else None
            if not isinstance(plantuml, dict):
                continue
            current = styles.get(kind, {})
            merged = dict(current)
            for key in ("background", "border", "font"):
                value = plantuml.get(key)
                if isinstance(value, str) and value:
                    merged[key] = value
            if merged:
                styles[kind] = merged
        used_kinds = {node.kind for node in ir.nodes}
        return {kind: styles[kind] for kind in used_kinds if kind in styles}

    def _emit_component_kind_styles(
        self, styles: dict[str, dict[str, str]]
    ) -> list[str]:
        lines: list[str] = []
        for kind, values in sorted(styles.items()):
            background = values.get("background")
            border = values.get("border")
            font = values.get("font")
            for shape in ("component", "rectangle", "database", "package"):
                if background:
                    lines.append(
                        f"skinparam {shape}<<{kind}>> BackgroundColor {background}"
                    )
                if border:
                    lines.append(f"skinparam {shape}<<{kind}>> BorderColor {border}")
                if font:
                    lines.append(f"skinparam {shape}<<{kind}>> FontColor {font}")
        return lines

    def _activity(self, ir: ActivityIR) -> str:
        lines = ["@startuml"]
        step_map = {s.id: s for s in ir.steps}
        # con particiones, PlantUML necesita el primer carril antes de `start`
        first = step_map.get(ir.start)
        lane = [first.partition if first is not None and any(s.partition for s in ir.steps) else None]
        if lane[0]:
            lines.append(f"|{lane[0]}|")
        lines.append("start")
        self._emit_steps(lines, step_map, ir.start, ir.end, set(), lane)
        lines.extend(["stop", "@enduml"])
        return "\n".join(lines)

    def _emit_steps(self, lines, step_map, current, end, visited, lane=None):
        lane = lane if lane is not None else [None]
        while current and current != end and current not in visited:
            visited.add(current)
            step = step_map.get(current)
            if step is None:
                break
            if step.partition and step.partition != lane[0]:
                lines.append(f"|{step.partition}|")
                lane[0] = step.partition
            if step.kind == "merge":
                # el `endif` de PlantUML ya une las ramas: el merge no dibuja nada propio
                current = step.next
                continue
            if step.kind == "decision":
                lines.append(f"if ({step.label}?) then (yes)")
                yes = step.branches.get("yes")
                self._emit_steps(lines, step_map, yes, end, set(visited), lane)
                lines.append("else (no)")
                no = step.branches.get("no")
                self._emit_steps(lines, step_map, no, end, set(visited), lane)
                lines.append("endif")
                return
            else:
                lines.append(f":{step.label};")
                if step.notes:
                    lines.append(f"note right: {step.notes}")
                current = step.next

    def _deployment(self, ir: DeploymentIR) -> str:
        art_map = {a.id: a for a in ir.artifacts}
        node_map = {n.id: n for n in ir.nodes}
        nested = {ref for n in ir.nodes for ref in n.contains if ref in node_map}
        lines = ["@startuml"]

        def emit(node, indent: str) -> None:
            kw = _NODE_KW.get(node.kind, "node")
            lines.append(f'{indent}{kw} "{node.label}" as {node.id} {{')
            for ref in node.contains:
                if ref in art_map:
                    lines.append(f'{indent}  artifact "{art_map[ref].label}" as {ref}')
                elif ref in node_map:
                    emit(node_map[ref], indent + "  ")
            lines.append(f"{indent}}}")

        for node in ir.nodes:
            if node.id not in nested:
                emit(node, "")
        lines.append("")
        for conn in ir.connections:
            arrow = "..>" if conn.kind in ("deploy", "manifest") else "-->"
            line = f"{conn.from_} {arrow} {conn.to}"
            if conn.text:
                line += f" : {conn.text}"
            lines.append(line)
        lines.append("@enduml")
        return "\n".join(lines)

FILE:src/specir/visual/renderers/d2.py
from __future__ import annotations
from specir.visual.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR
from specir.visual.exceptions import RenderError
from specir.visual.ir import ANY_STATE
from specir.visual.renderers.mermaid import ANY_STATE_ID

class D2Renderer:
    def render(self, ir) -> str:
        match ir:
            case SequenceIR():   return self._sequence(ir)
            case StateIR():      return self._state(ir)
            case ComponentIR():  return self._component(ir)
            case ActivityIR():   return self._activity(ir)
            case DeploymentIR(): return self._deployment(ir)
            case _: raise RenderError(f"D2Renderer cannot render {type(ir).__name__}")

    def _sequence(self, ir: SequenceIR) -> str:
        lines = ["direction: right"]
        for p in ir.participants:
            lines.append(f"{p.id}: {p.id}")
        for msg in ir.messages:
            lines.append(f"{msg.from_} -> {msg.to}: {msg.message}")
        return "\n".join(lines)

    def _state(self, ir: StateIR) -> str:
        lines = ["direction: right"]
        # una transicion sin estado de origen (ANY_STATE) sale de un pseudoestado `*` punteado
        if any(t.from_ == ANY_STATE for t in ir.transitions):
            lines.append(f'{ANY_STATE_ID}: "{ANY_STATE}" {{style.stroke-dash: 3}}')
        for t in ir.transitions:
            label = t.on
            if t.guard:
                label += f" [{t.guard}]"
            source = ANY_STATE_ID if t.from_ == ANY_STATE else t.from_
            lines.append(f"{source} -> {t.to}: {label}")
        return "\n".join(lines)

    def _component(self, ir: ComponentIR) -> str:
        lines = ["direction: right"]
        for node in ir.nodes:
            label = node.label or node.id
            lines.append(f"{node.id}: \"{label}\"")
            for child in node.contains:
                lines.append(f"{node.id}.{child}: \"{child}\"")
        for edge in ir.edges:
            label = edge.label or edge.relation
            lines.append(f"{edge.from_} -> {edge.to}: \"{label}\"")
        return "\n".join(lines)

    def _activity(self, ir: ActivityIR) -> str:
        lines = ["direction: down", "__start: Start"]
        # con particiones, cada carril es un contenedor y los pasos se nombran `carril.paso`
        lanes = list(dict.fromkeys(s.partition for s in ir.steps if s.partition))
        lane_key = {lane: f"__lane{i}" for i, lane in enumerate(lanes)}
        path = {s.id: f"{lane_key[s.partition]}.{s.id}" if s.partition else s.id for s in ir.steps}
        for lane in lanes:
            lines.append(f'{lane_key[lane]}: "{lane}"')
        for step in ir.steps:
            ref = path[step.id]
            if step.kind in ("decision", "merge"):
                lines.append(f"{ref}: \"{step.label}\"")
                lines.append(f"{ref}.shape: diamond")
            else:
                lines.append(f"{ref}: \"{step.label}\"")
            if step.notes:
                lines.append(f'{ref}__note: "{step.notes}"')
                lines.append(f"{ref}__note.shape: page")
        lines.append(f"__end: End")
        lines.append(f"__start -> {path.get(ir.start, ir.start)}")
        for step in ir.steps:
            ref = path[step.id]
            if step.kind == "decision":
                for branch, target in step.branches.items():
                    dest = "__end" if target == ir.end else path.get(target, target)
                    lines.append(f"{ref} -> {dest}: \"{branch}\"")
            elif step.next:
                dest = "__end" if step.next == ir.end else path.get(step.next, step.next)
                lines.append(f"{ref} -> {dest}")
            if step.notes:
                lines.append(f"{ref} -- {ref}__note: {{style.stroke-dash: 3}}")
        return "\n".join(lines)

    def _deployment(self, ir: DeploymentIR) -> str:
        lines = ["direction: right"]
        art_map = {a.id: a for a in ir.artifacts}
        node_map = {n.id: n for n in ir.nodes}
        nested = {ref for n in ir.nodes for ref in n.contains if ref in node_map}
        # cada elemento se nombra por su ruta de contenedores (`vpc.subnet.cluster`): las aristas
        # tienen que usar esa ruta, si no d2 crea un elemento suelto con el mismo id
        path: dict[str, str] = {}

        def emit(node, prefix: str) -> None:
            ref_path = f"{prefix}{node.id}"
            path[node.id] = ref_path
            lines.append(f"{ref_path}: \"{node.label}\"")
            for ref in node.contains:
                if ref in art_map:
                    path.setdefault(ref, f"{ref_path}.{ref}")
                    lines.append(f"{ref_path}.{ref}: \"{art_map[ref].label}\"")
                elif ref in node_map:
                    emit(node_map[ref], f"{ref_path}.")

        for node in ir.nodes:
            if node.id not in nested:
                emit(node, "")
        for conn in ir.connections:
            src, dst = path.get(conn.from_, conn.from_), path.get(conn.to, conn.to)
            dashed = " {style.stroke-dash: 3}" if conn.kind in ("deploy", "manifest") else ""
            label = conn.text
            if label:
                lines.append(f"{src} -> {dst}: \"{label}\"{dashed}")
            elif dashed:
                lines.append(f"{src} -> {dst}:{dashed}")
            else:
                lines.append(f"{src} -> {dst}")
        return "\n".join(lines)

FILE:src/specir/visual/renderers/vega.py
from __future__ import annotations
from specir.visual.ir import MatrixIR
from specir.visual.exceptions import RenderError

_KIND_COLORS = {
    "core": "#F59E0B", "boundary": "#60A5FA", "decision_engine": "#EC4899",
    "actor": "#A78BFA", "database": "#10B981",
}
_DEFAULT_COLOR = "#94A3B8"


class VegaRenderer:
    def render(self, ir) -> dict:
        if not isinstance(ir, MatrixIR):
            raise RenderError(f"VegaRenderer expects MatrixIR, got {type(ir).__name__}")
        # orden de primera aparicion: spec2viz iteraba un set, y el orden del dominio cambiaba con
        # PYTHONHASHSEED de una ejecucion a otra (el color de cada kind es el mismo)
        kinds = list(dict.fromkeys(s.kind for s in ir.spans))
        return {
            "$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": ir.title,
            "width": 220 + len(ir.stages) * 140 + 20,
            "height": max(120, 70 + len(ir.rows) * 34 + 20),
            "padding": 5,
            "signals": [
                {"name": "left",       "value": 220},
                {"name": "top",        "value": 70},
                {"name": "cellWidth",  "value": 140},
                {"name": "rowHeight",  "value": 34},
                {"name": "barPadding", "value": 6},
            ],
            "data": [
                {"name": "stages",         "values": [{"id": s.id, "index": s.index, "label": s.label, "view": s.view} for s in ir.stages]},
                {"name": "views", "source": "stages", "transform": [
                    {"type": "aggregate", "groupby": ["view"], "fields": ["index", "index"], "ops": ["min", "max"], "as": ["minIdx", "maxIdx"]}
                ]},
                {"name": "viewBoundaries", "source": "views", "transform": [
                    {"type": "formula", "expr": "[datum.minIdx, datum.maxIdx + 1]", "as": "indices"},
                    {"type": "flatten", "fields": ["indices"]},
                    {"type": "aggregate", "groupby": ["indices"]}
                ]},
                {"name": "stageBoundaries","values": [{"index": i} for i in range(len(ir.stages) + 1)]},
                {"name": "rows",           "values": [{"id": r.id, "label": r.label, "row": r.row, "depth": r.depth} for r in ir.rows]},
                {"name": "spans",          "values": [{"component": s.component, "row": s.row, "start": s.start, "end": s.end, "kind": s.kind, "depth": ir.rows[s.row].depth} for s in ir.spans]},
            ],
            "scales": [{"name": "kindColor", "type": "ordinal", "domain": kinds,
                        "range": [_KIND_COLORS.get(k, _DEFAULT_COLOR) for k in kinds]}],
            "marks": self._marks(ir),
        }

    def _marks(self, ir: MatrixIR) -> list[dict]:
        n = len(ir.rows)
        return [
            # View Labels
            {"type": "text", "from": {"data": "views"}, 
             "encode": {"enter": {
                "x": {"signal": "left + (datum.minIdx + datum.maxIdx + 1) * cellWidth / 2"},
                "y": {"value": 15}, "text": {"field": "view"},
                "align": {"value": "center"}, "fontWeight": {"value": "bold"}, "fontSize": {"value": 15}, "fill": {"value": "#475569"}
            }}},
            # Stage Labels
            {"type": "text", "from": {"data": "stages"}, "encode": {"enter": {
                "x": {"signal": "left + datum.index * cellWidth + cellWidth / 2"},
                "y": {"value": 40}, "text": {"field": "label"},
                "align": {"value": "center"}, "fontWeight": {"value": "bold"}, "fontSize": {"value": 13},
                "fill": {"value": "#475569"}
            }}},
            # Stage boundaries (dotted)
            {"type": "rule", "from": {"data": "stageBoundaries"}, "encode": {"enter": {
                "x": {"signal": "left + datum.index * cellWidth"},
                "y": {"signal": "top - 20"}, "y2": {"signal": f"top + {n} * rowHeight + 10"},
                "stroke": {"value": "#CBD5E1"}, "strokeDash": {"value": [4, 4]},
            }}},
            # View boundaries (solid, thick)
            {"type": "rule", "from": {"data": "viewBoundaries"}, "encode": {"enter": {
                "x": {"signal": "left + datum.indices * cellWidth"},
                "y": {"signal": "top - 40"}, "y2": {"signal": f"top + {n} * rowHeight + 20"},
                "stroke": {"value": "#475569"}, "strokeWidth": {"value": 2.5},
                "strokeOpacity": {"value": 0.6}
            }}},
            # Row Backgrounds (Zebra + Depth cues)
            {"type": "rect", "from": {"data": "rows"}, "encode": {"enter": {
                "x": {"value": 0}, "x2": {"signal": "width"},
                "y": {"signal": "top + datum.row * rowHeight"}, "height": {"signal": "rowHeight"},
                "fill": {"signal": "datum.depth === 0 ? (datum.row % 2 === 0 ? '#475569' : '#94A3B8') : (datum.row % 2 === 0 ? '#CBD5E1' : '#E2E8F0')"},
                "fillOpacity": {"value": 0.15}
            }}},
            # Hierarchy Indentation Cue (Vertical line on the left)
            {"type": "rule", "from": {"data": "rows"}, "encode": {"enter": {
                "x": {"signal": "12 + datum.depth * 18"}, "x2": {"signal": "12 + datum.depth * 18"},
                "y": {"signal": "top + datum.row * rowHeight + 2"}, 
                "y2": {"signal": "top + datum.row * rowHeight + rowHeight - 2"},
                "stroke": {"signal": "datum.depth === 0 ? '#475569' : '#94A3B8'"}, 
                "strokeWidth": {"signal": "datum.depth === 0 ? 3 : 1.5"}
            }}},
            # Component Labels
            {"type": "text", "from": {"data": "rows"}, "encode": {"enter": {
                "x": {"signal": "20 + datum.depth * 18"},
                "y": {"signal": "top + datum.row * rowHeight + rowHeight / 2"},
                "text": {"field": "label"}, "align": {"value": "left"},
                "baseline": {"value": "middle"}, "fontSize": {"value": 13}, "fill": {"value": "#111827"},
            }}},
            {"type": "rect", "from": {"data": "spans"}, "encode": {"enter": {
                "x": {"signal": "left + datum.start * cellWidth + 4"},
                "x2": {"signal": "left + datum.end * cellWidth - 4"},
                "y": {"signal": "top + datum.row * rowHeight + barPadding"},
                "height": {"signal": "rowHeight - barPadding * 2"},
                "cornerRadius": {"value": 7}, 
                "fill": {"scale": "kindColor", "field": "kind"},
                "fillOpacity": {"signal": "max(0.3, 1 - (datum.depth * 0.25))"},
                "stroke": {"scale": "kindColor", "field": "kind"}, 
                "strokeOpacity": {"value": 0.7},
                "strokeWidth": {"value": 1.5}
            }}},
        ]

FILE:src/specir/visual/renderers/bpmn.py
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from specir.visual.exceptions import RenderError
from specir.visual.ir import ActivityIR
from specir.visual.renderers.bpmn_palette import (
    END_TONE,
    GATEWAY_TONE,
    START_TONE,
    TONE_PALETTE,
)
from specir.visual.renderers.bpmn_viewer import render_bpmn_html, with_xml_provenance

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
BPMNDI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"
DC_NS = "http://www.omg.org/spec/DD/20100524/DC"
DI_NS = "http://www.omg.org/spec/DD/20100524/DI"
COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
NAMESPACES = {"bpmn": BPMN_NS, "bpmndi": BPMNDI_NS, "dc": DC_NS, "di": DI_NS, "color": COLOR_NS}

GATEWAY_KINDS = {"decision", "merge"}

# geometry (px); the viewer draws text at TEXT_FONT_SIZE in Arial, so a character's width
# depends on its class: uppercase, '_', 'm' and 'w' are wide, lowercase and digits medium,
# spaces and thin punctuation narrow
TEXT_FONT_SIZE = 14
CHAR_W_WIDE = 9.8
CHAR_W_LOWER = 7.7
CHAR_W_NARROW = 4.0
LINE_H = 17
TASK_MAX_W = 240
TASK_MIN_W = 120
TASK_PAD = 16      # text padding inside a task (bpmn-js wraps at width - 12)
TASK_MIN_H = 64
GATEWAY = 50
EVENT = 36
GATEWAY_LABEL_W = 190
EDGE_LABEL_W = 150
COL_GAP = 190
MIN_COL_GAP = 70
NODE_GAP = 44
DUMMY_GAP = 30
PARALLEL_STEP = 36
MARGIN = 60
LANE_STEP = 10
SUB_MIN_W = 150
SUB_MIN_H = 80
SHORT_LABEL = 42

# punctuation and separators that take almost no room in Arial 14
_NARROW_CHARS = set(" .,:;!?'\"`|()[]{}-–—/\\·&")
# lower-case letters that are as wide as an uppercase one
_WIDE_LOWER = set("mw")


def _q(ns: str, tag: str) -> str:
    return f"{{{NAMESPACES[ns]}}}{tag}"


def _ncname(raw: str) -> str:
    """An XML NCName from a step id: invalid characters become `_`."""
    s = re.sub(r"[^A-Za-z0-9_.-]", "_", raw)
    if not s or not re.match(r"[A-Za-z_]", s[0]):
        s = "_" + s
    return s


def _char_w(ch: str) -> float:
    """Estimated advance of `ch` in Arial 14px."""
    if ch in _NARROW_CHARS:
        return CHAR_W_NARROW
    if ch.isupper() or ch == "_" or ch in _WIDE_LOWER:
        return CHAR_W_WIDE
    return CHAR_W_LOWER


def _text_w(text: str) -> float:
    """Estimated rendered width of `text` in Arial 14px."""
    return sum(_char_w(ch) for ch in text)


def _task_box(label: str) -> tuple[int, int]:
    """A task box sized to its label: wrapped at most at TASK_MAX_W, at least TASK_MIN_W wide."""
    longest = max((_text_w(word) for word in label.split()), default=CHAR_W_LOWER)
    natural = longest + TASK_PAD
    w = int(min(TASK_MAX_W, max(TASK_MIN_W, natural)))
    lines = _wrap(label, w - TASK_PAD + 4)
    return w, max(TASK_MIN_H, lines * LINE_H + 24)


def _sub_box(label: str) -> tuple[int, int]:
    """A collapsed subprocess: compact by default, growing with its label."""
    natural = _text_w(label) + TASK_PAD
    w = int(min(TASK_MAX_W, max(SUB_MIN_W, natural)))
    lines = _wrap(label, w - TASK_PAD + 4)
    return w, max(SUB_MIN_H, lines * LINE_H + 24)


def _wrap(text: str, width_px: float) -> int:
    """Number of lines `text` takes when word-wrapped in `width_px`."""
    width = max(CHAR_W_NARROW, float(width_px))
    lines, current = 1, 0.0
    for word in text.split():
        w = _text_w(word)
        if current and current + CHAR_W_NARROW + w <= width:
            current += CHAR_W_NARROW + w
            continue
        if current:
            lines += 1
            current = 0.0
        while w > width:  # only a word wider than the whole line is broken
            w -= width
            lines += 1
        current = w
    return lines


@dataclass
class _Node:
    id: str            # BPMN id
    kind: str          # start | end | task | gateway | dummy
    name: str = ""
    step: str | None = None
    doc: str | None = None
    detail: str | None = None
    tone: str | None = None
    w: int = 0
    h: int = 0
    label_h: int = 0   # external label above (gateways)
    rank: int = 0
    x: int = 0
    y: int = 0

    @property
    def slot_h(self) -> int:
        return self.h + (self.label_h + 6 if self.label_h else 0)

    @property
    def cy(self) -> int:
        return self.y + self.h // 2


@dataclass
class _Edge:
    id: str
    src: str
    tgt: str
    name: str = ""
    back: bool = False
    chain: list[str] = field(default_factory=list)  # src, dummies..., tgt
    entry_dy: int = 0
    points: list[tuple[int, int]] = field(default_factory=list)
    label: tuple[int, int, int, int] | None = None


@dataclass
class _Plane:
    """The BPMNDiagram of a collapsed subProcess: its own nodes, edges and layout."""
    id: str
    bpmn_element: str
    nodes: dict[str, _Node] = field(default_factory=dict)
    edges: list[_Edge] = field(default_factory=list)


@dataclass
class _Diagram:
    nodes: dict[str, _Node]
    edges: list[_Edge]
    planes: list[_Plane] = field(default_factory=list)


class BpmnRenderer:
    """Renders an ActivityIR as BPMN 2.0 XML with diagram interchange (DI)."""

    def render(self, ir) -> str:
        if not isinstance(ir, ActivityIR):
            raise RenderError(f"BpmnRenderer cannot render {type(ir).__name__}")
        diagram = self._build(ir)
        self._layout(diagram.nodes, diagram.edges)
        for plane in diagram.planes:
            self._layout(plane.nodes, plane.edges)
        return self._xml(ir, diagram)

    def _build(self, ir: ActivityIR) -> _Diagram:
        if not ir.groups:
            nodes, edges = self._graph(ir)
            return _Diagram(nodes, edges)
        return self._grouped_graph(ir)

    @staticmethod
    def _step_node(uid, step) -> _Node:
        label = step.label or step.id
        if step.kind in GATEWAY_KINDS:
            return _Node(uid(f"Gateway_{_ncname(step.id)}"), "gateway", label, step.id, step.notes,
                         detail=step.detail, tone=step.tone, w=GATEWAY, h=GATEWAY,
                         label_h=_wrap(label, GATEWAY_LABEL_W) * LINE_H)
        w, h = _task_box(label)
        return _Node(uid(f"Task_{_ncname(step.id)}"), "task", label, step.id, step.notes,
                     detail=step.detail, tone=step.tone, w=w, h=h)

    @staticmethod
    def _short(text: str) -> str:
        text = " ".join((text or "").split())
        return text if len(text) <= SHORT_LABEL else text[:SHORT_LABEL - 1].rstrip() + "…"

    def _grouped_graph(self, ir: ActivityIR) -> _Diagram:
        """Steps in a group become a collapsed subProcess with its own drill-down plane."""
        used: set[str] = set()

        def uid(base: str) -> str:
            cand, i = base, 2
            while cand in used:
                cand, i = f"{base}_{i}", i + 1
            used.add(cand)
            return cand

        by_step = {step.id: step for step in ir.steps}
        if ir.start not in by_step:
            raise RenderError(f"Start step '{ir.start}' not found")
        step_level: dict[str, str | None] = {}
        for step in ir.steps:
            if step.group is not None and step.group not in ir.groups:
                raise RenderError(f"Step '{step.id}' references unknown group '{step.group}'")

        top_nodes: dict[str, _Node] = {}
        level_nodes: dict[str | None, dict[str, _Node]] = {None: top_nodes}
        level_edges: dict[str | None, list[_Edge]] = {None: []}
        group_node: dict[str, str] = {}
        planes: dict[str, _Plane] = {}

        top_start = _Node(uid(f"StartEvent_{_ncname(ir.start)}"), "start", w=EVENT, h=EVENT)
        top_nodes[top_start.id] = top_start
        for gid, group in ir.groups.items():
            if not any(step.group == gid for step in ir.steps):
                raise RenderError(f"Group '{gid}' has no steps")
            nid = uid(f"SubProcess_{_ncname(gid)}")
            group_node[gid] = nid
            sub_w, sub_h = _sub_box(group.label or gid)
            top_nodes[nid] = _Node(
                nid, "subprocess", group.label or gid, doc=group.detail, tone=group.tone,
                w=sub_w, h=sub_h,
            )
            level_nodes[gid] = {}
            level_edges[gid] = []
            planes[gid] = _Plane(uid(f"BPMNPlane_{_ncname(gid)}"), nid, level_nodes[gid], level_edges[gid])

        node_of: dict[str, str] = {}
        for step in ir.steps:
            node = self._step_node(uid, step)
            level = step.group
            level_nodes[level][node.id] = node
            node_of[step.id] = node.id
            step_level[step.id] = level

        top_end = _Node(uid(f"EndEvent_{_ncname(ir.end)}"), "end", w=EVENT, h=EVENT)
        top_nodes[top_end.id] = top_end

        def resolve(ref: str) -> tuple[str, str | None]:
            if ref in by_step:
                return node_of[ref], step_level[ref]
            if ref == ir.end:
                return top_end.id, None
            raise RenderError(f"Activity reference '{ref}' is neither a step nor the end")

        def add_edge(level: str | None, src: str, tgt: str, name: str = "") -> _Edge:
            nodes = level_nodes[level]
            s, t = nodes[src], nodes[tgt]
            base = f"Flow_{_ncname(s.step or s.id)}__{_ncname(t.step or t.id)}"
            edge = _Edge(uid(base), src, tgt, name)
            level_edges[level].append(edge)
            return edge

        def target_label(ref: str, level: str | None) -> str:
            if level is not None:
                return ir.groups[level].label or level
            if ref in by_step:
                return by_step[ref].label or ref
            return "fin"

        external_in: dict[str, list[str]] = {gid: [] for gid in ir.groups}
        external_out: dict[str, dict[str, tuple[str | None, str, str]]] = {
            gid: {} for gid in ir.groups
        }

        # the top-level start event enters the subProcess when the start step lives inside one
        start_level = step_level[ir.start]
        start_target = group_node[start_level] if start_level else node_of[ir.start]
        add_edge(None, top_start.id, start_target)
        if start_level:
            external_in[start_level].append(node_of[ir.start])

        for step in ir.steps:
            src_level = step_level[step.id]
            outs = list(step.branches.items())
            if step.next:
                outs.append(("", step.next))
            if not outs:  # terminal step: to the process end event, even when it is this step
                outs.append(("", None))
            for label, ref in outs:
                if ref is None:
                    tgt, tgt_level = top_end.id, None
                else:
                    tgt, tgt_level = resolve(ref)
                if src_level == tgt_level:
                    add_edge(src_level, node_of[step.id], tgt, label)
                elif src_level is None:
                    dest = group_node[tgt_level] if tgt_level else tgt
                    add_edge(None, node_of[step.id], dest, label)
                    if tgt_level:
                        external_in[tgt_level].append(tgt)
                else:
                    key = tgt_level if tgt_level is not None else tgt
                    if key not in external_out[src_level]:
                        suffix = tgt_level or (by_step[ref].id if ref in by_step else "fin")
                        end_id = uid(f"EndEvent_{_ncname(src_level)}__{_ncname(suffix)}")
                        name = target_label(ref, tgt_level) if ref is not None else "fin"
                        end_node = _Node(end_id, "end", self._short(name), w=EVENT, h=EVENT)
                        level_nodes[src_level][end_id] = end_node
                        external_out[src_level][key] = (tgt_level, tgt, end_id)
                    add_edge(src_level, node_of[step.id], external_out[src_level][key][2], label)

        # the internal start event feeds every step that received a flow from outside
        for gid, entries in external_in.items():
            unique = list(dict.fromkeys(entries))
            if not unique:
                continue
            start = _Node(uid(f"StartEvent_{_ncname(gid)}__in"), "start", w=EVENT, h=EVENT)
            planes[gid].nodes = {start.id: start, **planes[gid].nodes}
            level_nodes[gid] = planes[gid].nodes
            first: list[_Edge] = []
            for entry in unique:
                base = f"Flow_{_ncname(gid)}__in_{_ncname(level_nodes[gid][entry].step or entry)}"
                first.append(_Edge(uid(base), start.id, entry))
            level_edges[gid][0:0] = first
            planes[gid].edges = level_edges[gid]

        # one top-level flow per distinct external destination; labelled when the group has several
        for gid, destinations in external_out.items():
            many = len(destinations) > 1
            for tgt_level, tgt, end_id in destinations.values():
                dest = group_node[tgt_level] if tgt_level else tgt
                name = ""
                if many:
                    end_node = level_nodes[gid][end_id]
                    name = end_node.name
                add_edge(None, group_node[gid], dest, name)

        return _Diagram(top_nodes, level_edges[None], list(planes.values()))

    # ── graph ────────────────────────────────────────────────────────────────

    def _graph(self, ir: ActivityIR) -> tuple[dict[str, _Node], list[_Edge]]:
        used: set[str] = set()

        def uid(base: str) -> str:
            cand, i = base, 2
            while cand in used:
                cand, i = f"{base}_{i}", i + 1
            used.add(cand)
            return cand

        nodes: dict[str, _Node] = {}
        start = _Node(uid(f"StartEvent_{_ncname(ir.start)}"), "start", w=EVENT, h=EVENT)
        nodes[start.id] = start
        by_step: dict[str, str] = {}
        for step in ir.steps:
            label = step.label or step.id
            if step.kind in GATEWAY_KINDS:
                node = _Node(uid(f"Gateway_{_ncname(step.id)}"), "gateway", label, step.id, step.notes,
                             tone=step.tone, w=GATEWAY, h=GATEWAY,
                             label_h=_wrap(label, GATEWAY_LABEL_W) * LINE_H)
            else:
                w, h = _task_box(label)
                node = _Node(uid(f"Task_{_ncname(step.id)}"), "task", label, step.id, step.notes,
                             tone=step.tone, w=w, h=h)
            nodes[node.id] = node
            by_step[step.id] = node.id
        end = _Node(uid(f"EndEvent_{_ncname(ir.end)}"), "end", w=EVENT, h=EVENT)
        nodes[end.id] = end

        def target(ref: str) -> str:
            if ref in by_step:
                return by_step[ref]
            if ref == ir.end:
                return end.id
            raise RenderError(f"Activity reference '{ref}' is neither a step nor the end")

        pairs: list[tuple[str, str, str]] = []
        if ir.start not in by_step:
            raise RenderError(f"Start step '{ir.start}' not found")
        pairs.append((start.id, by_step[ir.start], ""))
        for step in ir.steps:
            src = by_step[step.id]
            outs = [(label, target(t)) for label, t in step.branches.items()]
            if step.next:
                outs.append(("", target(step.next)))
            if not outs:  # a step without outgoing flow is terminal: it ends the process
                outs.append(("", end.id))
            for label, tgt in outs:
                pairs.append((src, tgt, label))

        key = {start.id: "start", end.id: "end"}
        key.update({nid: _ncname(sid) for sid, nid in by_step.items()})
        edges: list[_Edge] = []
        for src, tgt, label in pairs:
            base = f"Flow_{key[src]}__{key[tgt]}"
            edges.append(_Edge(uid(base), src, tgt, label))
        return nodes, edges

    # ── layout ───────────────────────────────────────────────────────────────

    def _layout(self, nodes: dict[str, _Node], edges: list[_Edge]) -> None:
        real = list(nodes)
        out: dict[str, list[_Edge]] = {n: [] for n in real}
        for e in edges:
            out[e.src].append(e)

        # back edges: DFS from the start event, then from any unvisited node, in spec order
        state: dict[str, int] = {}
        order: list[str] = []

        def dfs(root: str) -> None:
            stack = [(root, iter(out[root]))]
            state[root] = 1
            order.append(root)
            while stack:
                n, it = stack[-1]
                e = next(it, None)
                if e is None:
                    state[n] = 2
                    stack.pop()
                    continue
                s = state.get(e.tgt, 0)
                if s == 1:
                    e.back = True
                elif s == 0:
                    state[e.tgt] = 1
                    order.append(e.tgt)
                    stack.append((e.tgt, iter(out[e.tgt])))

        for n in real:
            if n not in state:
                dfs(n)

        # longest-path ranks on the DAG (Kahn's order)
        fwd = [e for e in edges if not e.back]
        indeg = {n: 0 for n in real}
        for e in fwd:
            indeg[e.tgt] += 1
        queue = [n for n in order if indeg[n] == 0]
        rank = {n: 0 for n in real}
        while queue:
            n = queue.pop(0)
            for e in out[n]:
                if e.back:
                    continue
                rank[e.tgt] = max(rank[e.tgt], rank[n] + 1)
                indeg[e.tgt] -= 1
                if indeg[e.tgt] == 0:
                    queue.append(e.tgt)
        ends = [n for n in real if nodes[n].kind == "end"]
        if ends:
            last = max(rank.values()) if len(real) > 1 else 0
            for end_id in ends:
                rank[end_id] = last
            if any(rank[n] == last for n in real if nodes[n].kind != "end"):
                for end_id in ends:
                    rank[end_id] = last + 1
        for n in real:
            nodes[n].rank = rank[n]

        # dummies for long forward edges
        all_nodes: dict[str, _Node] = dict(nodes)
        for e in edges:
            e.chain = [e.src, e.tgt]
            if e.back:
                continue
            rs, rt = rank[e.src], rank[e.tgt]
            if rt - rs > 1:
                dummies = []
                for r in range(rs + 1, rt):
                    d = _Node(f"__dummy_{e.id}_{r}", "dummy", w=0, h=0, rank=r)
                    all_nodes[d.id] = d
                    dummies.append(d.id)
                e.chain = [e.src, *dummies, e.tgt]

        # parallel flows between the same pair enter the target at different heights
        groups: dict[tuple[str, str], list[_Edge]] = {}
        for e in edges:
            if not e.back:
                groups.setdefault((e.src, e.tgt), []).append(e)
        for group in groups.values():
            k = len(group)
            for i, e in enumerate(group):
                e.entry_dy = int((i - (k - 1) / 2) * PARALLEL_STEP)

        # order inside each rank: discovery order, then barycenter sweeps
        disc = {n: i for i, n in enumerate(order)}
        pred: dict[str, list[str]] = {n: [] for n in all_nodes}
        succ: dict[str, list[str]] = {n: [] for n in all_nodes}
        for e in edges:
            if e.back:
                continue
            for a, b in zip(e.chain, e.chain[1:]):
                succ[a].append(b)
                pred[b].append(a)
        max_rank = max(n.rank for n in all_nodes.values())
        layers: list[list[str]] = [[] for _ in range(max_rank + 1)]
        # dummies are discovered right after their edge's source
        dkey: dict[str, float] = {}
        for e in edges:
            for j, d in enumerate(e.chain[1:-1]):
                dkey[d] = disc[e.src] + 0.001 * (edges.index(e) + 1)
        for nid, n in all_nodes.items():
            layers[n.rank].append(nid)
        for layer in layers:
            layer.sort(key=lambda n: disc.get(n, dkey.get(n, 0.0)))

        def sweep(down: bool) -> None:
            rng = range(1, len(layers)) if down else range(len(layers) - 2, -1, -1)
            for r in rng:
                ref = layers[r - 1] if down else layers[r + 1]
                pos = {n: i for i, n in enumerate(ref)}
                cur = {n: i for i, n in enumerate(layers[r])}

                def bary(n: str) -> float:
                    nb = [pos[m] for m in (pred[n] if down else succ[n]) if m in pos]
                    return sum(nb) / len(nb) if nb else float(cur[n])

                layers[r].sort(key=lambda n: (bary(n), cur[n]))

        for _ in range(4):
            sweep(True)
            sweep(False)
        sweep(True)

        # x per column, y per slot (each column centered on the tallest)
        # a gateway's column is as wide as its label, so the label never reaches into a gap
        col_w = [max((GATEWAY_LABEL_W if all_nodes[n].label_h else all_nodes[n].w for n in layer), default=0) or EVENT
                 for layer in layers]
        # the gap between two columns is only as wide as the longest edge label crossing it,
        # so a mostly linear plan stays compact instead of paying COL_GAP at every column
        gap_need = [0.0] * max(len(layers) - 1, 0)
        for e in edges:
            if e.back or not e.name:
                continue
            need = _text_w(e.name) + 40
            # the label is drawn on the flow's first segment, so only that gap needs room
            r = all_nodes[e.chain[0]].rank
            if r < len(gap_need):
                gap_need[r] = max(gap_need[r], need)
        col_gap = [int(min(COL_GAP, max(MIN_COL_GAP, need))) for need in gap_need]
        col_x, x = [], MARGIN
        for i, w in enumerate(col_w):
            col_x.append(x)
            x += w + (col_gap[i] if i < len(col_gap) else COL_GAP)
        # y: each rank starts stacked, then every slot is pulled toward the median of its neighbors
        # in the next/previous rank; the order and minimum gaps hold (isotonic regression per rank)
        def head(n: _Node) -> float:  # slot top -> center
            return (n.label_h + 6 if n.label_h else 0) + n.h / 2

        def gap(a: _Node, b: _Node) -> int:
            return DUMMY_GAP if (a.kind == "dummy" and b.kind == "dummy") else NODE_GAP

        def offsets(layer: list[str]) -> list[float]:
            offs, acc = [], 0.0
            for i, nid in enumerate(layer):
                if i:
                    a, b = all_nodes[layer[i - 1]], all_nodes[nid]
                    acc += a.h / 2 + gap(a, b) + head(b)
                offs.append(acc)
            return offs

        center: dict[str, float] = {}
        for layer in layers:
            for nid, off in zip(layer, offsets(layer)):
                center[nid] = off

        def median(vals: list[float]) -> float:
            vals = sorted(vals)
            m = len(vals) // 2
            return vals[m] if len(vals) % 2 else (vals[m - 1] + vals[m]) / 2

        def place(layer: list[str], neighbors) -> None:
            offs = offsets(layer)
            z = []
            for nid, off in zip(layer, offs):
                nb = [center[m] for m in neighbors(nid)]
                z.append((median(nb) if nb else center[nid]) - off)
            blocks: list[list[float]] = []  # pool adjacent violators: non-decreasing fit of z
            for v in z:
                blocks.append([v, 1])
                while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
                    s_, c_ = blocks.pop()
                    blocks[-1][0] += s_
                    blocks[-1][1] += c_
            fit = [b[0] / b[1] for b in blocks for _ in range(int(b[1]))]
            for nid, f, off in zip(layer, fit, offs):
                center[nid] = f + off

        for _ in range(6):
            for layer in layers[1:]:
                place(layer, lambda n: pred[n])
            for layer in reversed(layers[:-1]):
                place(layer, lambda n: succ[n])
        def both(n: str) -> list[str]:
            # a long edge stays straight: its slots follow the neighbor slot of the same edge
            if all_nodes[n].kind == "dummy":
                for m in pred[n] + succ[n]:
                    if all_nodes[m].kind == "dummy":
                        return [m]
            return pred[n] + succ[n]

        for _ in range(2):
            for layer in layers:
                place(layer, both)

        shift = MARGIN - min(center[n] - head(all_nodes[n]) for n in all_nodes)
        for r, layer in enumerate(layers):
            for nid in layer:
                node = all_nodes[nid]
                node.x = col_x[r] + (col_w[r] - node.w) // 2
                node.y = int(round(center[nid] + shift - node.h / 2))

        self._route(all_nodes, edges, col_x, col_w, col_gap)

    def _route(self, nodes: dict[str, _Node], edges: list[_Edge], col_x: list[int],
               col_w: list[int], col_gap: list[int]) -> None:
        # hops in each gap that change height get a vertical lane: fan-outs near the source column,
        # fan-ins near the target column
        hops: list[tuple[_Edge, int, int, int, int]] = []  # edge, hop index, gap, y_from, y_to

        def station_y(e: _Edge, i: int) -> int:
            n = nodes[e.chain[i]]
            if n.kind == "dummy":
                return n.y
            if i == len(e.chain) - 1:
                return n.cy + max(-(n.h // 2) + 6, min(n.h // 2 - 6, e.entry_dy))
            return n.cy

        lanes: dict[int, dict[tuple, int]] = {}
        for e in edges:
            if e.back:
                continue
            for i in range(len(e.chain) - 1):
                a = nodes[e.chain[i]]
                ya, yb = station_y(e, i), station_y(e, i + 1)
                hops.append((e, i, a.rank, ya, yb))
                if ya != yb:
                    key = ("out", a.id) if a.kind != "dummy" else ("in", e.chain[i + 1], yb)
                    lanes.setdefault(a.rank, {}).setdefault(key, ya)
        lane_x: dict[tuple[int, tuple], int] = {}
        for gap, keys in lanes.items():
            left = col_x[gap] + col_w[gap]
            gap_w = col_gap[gap] if gap < len(col_gap) else COL_GAP
            right = left + gap_w
            outs = sorted((k for k in keys if k[0] == "out"), key=lambda k: keys[k])
            ins = sorted((k for k in keys if k[0] == "in"), key=lambda k: keys[k])
            # narrow gaps still split in two lanes (fan-out left, fan-in right), at a smaller step
            half = max(6, gap_w // 2 - 18)
            step = max(4, min(LANE_STEP, half // max(1, max(len(outs), len(ins)))))
            for i, k in enumerate(outs):
                lane_x[(gap, k)] = left + 18 + i * step
            for i, k in enumerate(ins):
                lane_x[(gap, k)] = right - 18 - i * step

        for e in edges:
            if e.back:
                continue
            src, tgt = nodes[e.src], nodes[e.tgt]
            pts = [(src.x + src.w, src.cy)]
            label_seg = None
            for i in range(len(e.chain) - 1):
                a, b = nodes[e.chain[i]], nodes[e.chain[i + 1]]
                ya, yb = station_y(e, i), station_y(e, i + 1)
                gap_left = col_x[a.rank] + col_w[a.rank]
                pts.append((gap_left, ya))
                if ya != yb:
                    key = ("out", a.id) if a.kind != "dummy" else ("in", b.id, yb)
                    lx = lane_x[(a.rank, key)]
                    pts += [(lx, ya), (lx, yb)]
                    seg = (lx, yb)
                else:
                    seg = (gap_left if i else src.x + src.w, yb)
                if b.kind == "dummy":
                    pts += [(col_x[b.rank], yb), (col_x[b.rank] + col_w[b.rank], yb)]
                    end_x = col_x[b.rank] + col_w[b.rank]
                else:
                    pts.append((tgt.x, yb))
                    end_x = tgt.x
                if label_seg is None:
                    label_seg = (seg[0], end_x, seg[1])
            e.points = _compress(pts)
            if e.name and label_seg:
                x0, x1, y = label_seg
                w = max(40, min(EDGE_LABEL_W, x1 - x0 - 12))
                h = _wrap(e.name, w) * LINE_H
                e.label = (x0 + 6, y - h - 3, w, h)

        # back edges loop below everything
        bottom = max(n.y + n.h for n in nodes.values() if n.kind != "dummy")
        for k, e in enumerate(x for x in edges if x.back):
            src, tgt = nodes[e.src], nodes[e.tgt]
            yl = bottom + 40 + k * 20
            e.points = _compress([
                (src.x + src.w // 2, src.y + src.h), (src.x + src.w // 2, yl),
                (tgt.x + tgt.w // 2, yl), (tgt.x + tgt.w // 2, tgt.y + tgt.h),
            ])
            if e.name:
                w = EDGE_LABEL_W
                h = _wrap(e.name, w) * LINE_H
                e.label = (min(src.x, tgt.x) + src.w // 2 + 6, yl + 3, w, h)

    # ── xml ──────────────────────────────────────────────────────────────────

    def _xml(self, ir: ActivityIR, diagram: _Diagram) -> str:
        for prefix, uri in NAMESPACES.items():
            ET.register_namespace(prefix, uri)
        pid = "Process_1"
        defs = ET.Element(_q("bpmn", "definitions"), {
            "id": "Definitions_1",
            "targetNamespace": "http://spec2viz/bpmn",
            "exporter": "spec2viz",
        })
        proc = ET.SubElement(defs, _q("bpmn", "process"), {"id": pid, "name": ir.title, "isExecutable": "false"})
        tags = {
            "start": "startEvent", "end": "endEvent", "task": "task",
            "gateway": "exclusiveGateway", "subprocess": "subProcess",
        }
        planes_by_element = {plane.bpmn_element: plane for plane in diagram.planes}

        def indexes(nodes: dict[str, _Node], edges: list[_Edge]):
            incoming: dict[str, list[str]] = {n: [] for n in nodes}
            outgoing: dict[str, list[str]] = {n: [] for n in nodes}
            for e in edges:
                outgoing[e.src].append(e.id)
                incoming[e.tgt].append(e.id)
            return incoming, outgoing

        def emit_flows(parent: ET.Element, edges: list[_Edge]) -> None:
            for e in edges:
                attrs = {"id": e.id, "sourceRef": e.src, "targetRef": e.tgt}
                if e.name:
                    attrs["name"] = e.name
                ET.SubElement(parent, _q("bpmn", "sequenceFlow"), attrs)

        def emit_element(parent: ET.Element, n: _Node, incoming, outgoing) -> None:
            attrs = {"id": n.id}
            if n.name:
                attrs["name"] = n.name
            el = ET.SubElement(parent, _q("bpmn", tags[n.kind]), attrs)
            if n.doc:
                ET.SubElement(el, _q("bpmn", "documentation")).text = n.doc
            if n.detail:
                ET.SubElement(el, _q("bpmn", "documentation")).text = n.detail
            for f in incoming[n.id]:
                ET.SubElement(el, _q("bpmn", "incoming")).text = f
            for f in outgoing[n.id]:
                ET.SubElement(el, _q("bpmn", "outgoing")).text = f
            if n.kind == "subprocess":
                plane = planes_by_element[n.id]
                inner_in, inner_out = indexes(plane.nodes, plane.edges)
                for child in plane.nodes.values():
                    emit_element(el, child, inner_in, inner_out)
                emit_flows(el, plane.edges)

        top_in, top_out = indexes(diagram.nodes, diagram.edges)
        for n in diagram.nodes.values():
            emit_element(proc, n, top_in, top_out)
        emit_flows(proc, diagram.edges)

        def emit_shapes(plane_el: ET.Element, nodes: dict[str, _Node], edges: list[_Edge]) -> None:
            gateway_border = {n.id: _tone_colors(n)[1] for n in nodes.values() if n.kind == "gateway"}
            for n in nodes.values():
                attrs = {"id": f"{n.id}_di", "bpmnElement": n.id}
                if n.kind == "gateway":
                    attrs["isMarkerVisible"] = "true"
                if n.kind == "subprocess":
                    attrs["isExpanded"] = "false"
                colors = _tone_colors(n)
                if colors[0]:
                    attrs[_q("color", "background-color")] = colors[0]
                if colors[1]:
                    attrs[_q("color", "border-color")] = colors[1]
                shape = ET.SubElement(plane_el, _q("bpmndi", "BPMNShape"), attrs)
                _bounds(shape, n.x, n.y, n.w, n.h)
                if n.kind == "gateway":
                    lw = GATEWAY_LABEL_W
                    label = ET.SubElement(shape, _q("bpmndi", "BPMNLabel"))
                    _bounds(label, n.x + n.w // 2 - lw // 2, n.y - n.label_h - 6, lw, n.label_h)
            for e in edges:
                attrs = {"id": f"{e.id}_di", "bpmnElement": e.id}
                border = gateway_border.get(e.src)
                if border:
                    attrs[_q("color", "border-color")] = border
                edge = ET.SubElement(plane_el, _q("bpmndi", "BPMNEdge"), attrs)
                for x, y in e.points:
                    ET.SubElement(edge, _q("di", "waypoint"), {"x": str(x), "y": str(y)})
                if e.label:
                    label = ET.SubElement(edge, _q("bpmndi", "BPMNLabel"))
                    _bounds(label, *e.label)

        top_diagram = ET.SubElement(defs, _q("bpmndi", "BPMNDiagram"), {"id": "BPMNDiagram_1"})
        top_plane = ET.SubElement(top_diagram, _q("bpmndi", "BPMNPlane"),
                                  {"id": "BPMNPlane_1", "bpmnElement": pid})
        emit_shapes(top_plane, diagram.nodes, diagram.edges)

        for plane in diagram.planes:
            suffix = plane.id[len("BPMNPlane_"):]
            sub_diagram = ET.SubElement(defs, _q("bpmndi", "BPMNDiagram"),
                                        {"id": f"BPMNDiagram_{suffix}"})
            sub_plane = ET.SubElement(sub_diagram, _q("bpmndi", "BPMNPlane"),
                                      {"id": plane.id, "bpmnElement": plane.bpmn_element})
            emit_shapes(sub_plane, plane.nodes, plane.edges)

        ET.indent(defs, space="  ")
        body = ET.tostring(defs, encoding="unicode")
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n"


def _tone_colors(node: "_Node") -> tuple[str | None, str | None]:
    """The BPMN in Color (background, border) of a node; plain tasks without tone stay default."""
    if node.kind == "start":
        return START_TONE
    if node.kind == "end":
        return END_TONE
    if node.kind == "gateway":
        return TONE_PALETTE.get(node.tone or "", GATEWAY_TONE)
    if node.kind in ("task", "subprocess") and node.tone in TONE_PALETTE:
        return TONE_PALETTE[node.tone]
    return None, None


def _bounds(parent: ET.Element, x: int, y: int, w: int, h: int) -> None:
    ET.SubElement(parent, _q("dc", "Bounds"), {"x": str(int(x)), "y": str(int(y)), "width": str(int(w)), "height": str(int(h))})


def _compress(pts: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Drops repeated points and the middle point of collinear runs."""
    out: list[tuple[int, int]] = []
    for p in pts:
        p = (int(p[0]), int(p[1]))
        if out and out[-1] == p:
            continue
        if len(out) >= 2:
            (x0, y0), (x1, y1) = out[-2], out[-1]
            if (x0 == x1 == p[0]) or (y0 == y1 == p[1]):
                out[-1] = p
                continue
        out.append(p)
    return out


__all__ = ["BpmnRenderer", "render_bpmn_html", "with_xml_provenance", "NAMESPACES", "BPMN_NS"]

FILE:src/specir/visual/renderers/bpmn_palette.py
"""BPMN in Color palette shared by the renderer and the offline viewer page."""

TONE_PALETTE: dict[str, tuple[str, str]] = {
    "success": ("#E3F4E6", "#2E7D32"),
    "warning": ("#FFEFC7", "#B26A00"),
    "danger": ("#FBE3E3", "#B42318"),
    "info": ("#E1EEFB", "#1D4ED8"),
    "neutral": ("#EEF0F3", "#6B7280"),
    "rule1": ("#EDE9FE", "#6D4AFF"),
    "rule2": ("#FDE7D9", "#C2410C"),
    "rule3": ("#DCF5EE", "#0F766E"),
    "rule4": ("#FDE7F1", "#BE185D"),
    "rule5": ("#EAF0D8", "#4D7C0F"),
}
GATEWAY_TONE = ("#F4F0FB", "#7E57C2")
START_TONE = ("#E3F4E6", "#2E7D32")
END_TONE = ("#FBE3E3", "#8B1A1A")
DEFAULT_LEGEND_LABELS = {
    "success": "favorable",
    "warning": "atención",
    "danger": "rechazo",
    "info": "informativo",
    "neutral": "neutro",
    "rule1": "regla 1",
    "rule2": "regla 2",
    "rule3": "regla 3",
    "rule4": "regla 4",
    "rule5": "regla 5",
    "gateway": "gateway por defecto",
    "start": "inicio",
    "end": "fin",
}

__all__ = ["TONE_PALETTE", "GATEWAY_TONE", "START_TONE", "END_TONE", "DEFAULT_LEGEND_LABELS"]

FILE:src/specir/visual/renderers/bpmn_viewer.py
"""Self-contained HTML viewer for BPMN XML: vendored bpmn-js, legend, metadata and side panel."""

from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from specir.visual.exceptions import RenderError
from specir.visual.renderers.bpmn_palette import (
    DEFAULT_LEGEND_LABELS,
    GATEWAY_TONE,
    TONE_PALETTE,
)

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
VENDOR_DIR = Path(__file__).resolve().parent.parent / "templates" / "vendor" / "bpmn-js"
NODE_TAGS = {"startEvent", "endEvent", "task", "exclusiveGateway", "subProcess"}


def _vendor(name: str) -> str:
    path = VENDOR_DIR / name
    if not path.exists():
        raise RenderError(f"Vendored bpmn-js asset missing: {path}")
    return path.read_text(encoding="utf-8")


def _script_safe(text: str) -> str:
    """Text that can sit inside an inline <script> or <style> element."""
    return re.sub(r"</(script|style)", r"<\\/\1", text, flags=re.IGNORECASE)


def _json_for_script(value) -> str:
    return (json.dumps(value, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def element_info(xml: str) -> dict[str, dict]:
    """label/detail/branches indexed by BPMN element id, read from the generated XML."""
    try:
        root = ET.fromstring(xml.encode("utf-8"))
    except ET.ParseError:
        return {}
    elements: dict[str, ET.Element] = {}
    for el in root.iter():
        tag = _local(el.tag)
        if tag in NODE_TAGS and el.get("id"):
            elements[el.get("id")] = el
    name = {eid: (el.get("name") or eid) for eid, el in elements.items()}
    flows = [el for el in root.iter() if _local(el.tag) == "sequenceFlow"]
    info: dict[str, dict] = {}
    for eid, el in elements.items():
        docs = [d.text for d in el if _local(d.tag) == "documentation" and d.text]
        branches = [
            {
                "label": f.get("name") or "",
                "target": name.get(f.get("targetRef"), f.get("targetRef") or ""),
            }
            for f in flows
            if f.get("sourceRef") == eid
        ]
        info[eid] = {
            "label": el.get("name") or eid,
            "detail": docs[-1] if docs else None,
            "branches": branches,
            "subprocess": _local(el.tag) == "subProcess",
        }
    return info


def _used_legend_keys(xml: str) -> list[str]:
    """Legend entries that the diagram really uses, in palette order (no start/end events)."""
    keys: set[str] = set()
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return [*TONE_PALETTE, "gateway"]
    by_background = {background: tone for tone, (background, _) in TONE_PALETTE.items()}
    for el in root.iter():
        if not _local(el.tag) == "BPMNShape":
            continue
        element_id = el.get("bpmnElement") or ""
        if element_id.startswith(("StartEvent_", "EndEvent_")):
            continue
        background = el.get(f"{{{COLOR_NS}}}background-color")
        if background == GATEWAY_TONE[0]:
            keys.add("gateway")
        elif background in by_background:
            keys.add(by_background[background])
    order = [*TONE_PALETTE, "gateway"]
    return [key for key in order if key in keys]


def _legend_html(xml: str, metadata: dict | None = None) -> str:
    custom = metadata.get("legend") if isinstance(metadata, dict) else None
    custom = custom if isinstance(custom, dict) else {}
    items = []
    for key in _used_legend_keys(xml):
        if key in TONE_PALETTE:
            background, border = TONE_PALETTE[key]
        else:
            background, border = GATEWAY_TONE
        label = custom.get(key) if isinstance(custom.get(key), str) else DEFAULT_LEGEND_LABELS[key]
        items.append(
            f'    <span class="item"><i class="swatch" style="background:{background};border-color:{border}"></i>'
            f"{html.escape(label)}</span>"
        )
    return ('  <div class="legend" aria-label="Leyenda de colores">\n'
            '    <span class="title">Colores:</span>\n' + "\n".join(items) + "\n  </div>")


def _meta_html(metadata: dict | None) -> str:
    """Description and open questions, collapsed into a <details> so they do not take the screen."""
    if not isinstance(metadata, dict):
        return ""
    desc = metadata.get("description")
    questions = metadata.get("preguntas_abiertas")
    if isinstance(questions, str):
        questions = [questions]
    body: list[str] = []
    if desc:
        body.append(f'      <p class="description">{html.escape(str(desc).strip())}</p>')
    if questions:
        items = "\n".join(f"        <li>{html.escape(str(q))}</li>" for q in questions)
        body.append('      <h2>Preguntas abiertas</h2>\n      <ul class="preguntas-abiertas">\n'
                    + items + "\n      </ul>")
    if not body:
        return ""
    return ('    <details class="meta">\n'
            '      <summary>Descripción y preguntas abiertas</summary>\n'
            '      <div class="meta-body">\n' + "\n".join(body) + "\n      </div>\n"
            "    </details>")


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@</title>
<style>
@@DIAGRAM_CSS@@
</style>
<style>
@@BPMN_CSS@@
</style>
<style>
  html, body { margin: 0; height: 100%; font-family: system-ui, -apple-system, "Segoe UI", Arial, sans-serif; color: #1f2328; background: #fff; }
  body { height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
  header { flex: 0 0 auto; padding: 6px 14px 4px; border-bottom: 1px solid #d0d7de; background: #fff; position: relative; z-index: 5; }
  .row { display: flex; align-items: center; gap: 12px; justify-content: space-between; }
  .row.second { justify-content: flex-start; gap: 16px; margin-top: 2px; }
  h1 { font-size: 16px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .toolbar { display: flex; gap: 6px; flex: 0 0 auto; }
  .toolbar button { font: inherit; font-size: 12px; padding: 2px 9px; border: 1px solid #d0d7de; background: #f6f8fa; border-radius: 5px; cursor: pointer; }
  details.meta { flex: 0 0 auto; font-size: 12px; line-height: 1.4; }
  details.meta summary { cursor: pointer; padding: 2px 0; white-space: nowrap; }
  details.meta .meta-body { position: absolute; left: 0; right: 0; top: 100%; max-height: 60vh; overflow: auto; padding: 10px 14px 12px; background: #fff; border-bottom: 1px solid #d0d7de; box-shadow: 0 6px 16px rgba(0, 0, 0, .12); z-index: 20; }
  .meta-body p { margin: 3px 0; font-size: 13px; line-height: 1.45; max-width: 120ch; }
  .meta-body h2 { font-size: 13px; margin: 8px 0 3px; }
  .meta-body ul { margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.45; max-width: 120ch; }
  .legend { flex: 1 1 auto; display: flex; flex-wrap: nowrap; gap: 4px 14px; overflow-x: auto; white-space: nowrap; font-size: 12px; align-items: center; }
  .legend .item { flex: 0 0 auto; display: inline-flex; align-items: center; gap: 5px; }
  .legend .swatch { width: 16px; height: 13px; border-radius: 3px; border: 2px solid #555; box-sizing: border-box; }
  .legend .title { flex: 0 0 auto; font-weight: 600; }
  main { flex: 1 1 auto; min-height: 0; display: flex; }
  #canvas { flex: 1 1 auto; min-height: 0; position: relative; }
  #panel { flex: 0 0 340px; max-width: 340px; border-left: 1px solid #d0d7de; overflow: auto; padding: 12px 14px; font-size: 13px; line-height: 1.45; background: #fbfcfd; box-sizing: border-box; }
  body.panel-collapsed #panel { display: none; }
  #panel h2 { font-size: 14px; margin: 0 0 8px; }
  #panel h3 { font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: #57606a; margin: 14px 0 5px; }
  #panel p { margin: 0 0 8px; white-space: pre-wrap; }
  #panel ul { margin: 0; padding-left: 18px; }
  #panel li { margin: 3px 0; }
  #panel .muted { color: #57606a; }
  #panel .branch-label { font-weight: 600; }
  #error { color: #b42318; font-size: 12px; white-space: pre-wrap; position: absolute; right: 14px; top: 6px; }
</style>
</head>
<body>
<header>
  <div class="row">
    <h1>@@TITLE@@</h1>
    <div class="toolbar">
      <button type="button" id="fit">Fit</button>
      <button type="button" id="zoom-in">Zoom +</button>
      <button type="button" id="zoom-out">Zoom &minus;</button>
      <button type="button" id="toggle-panel">Detalle</button>
    </div>
  </div>
  <div class="row second">
@@META@@
@@LEGEND@@
  </div>
  <div id="error"></div>
</header>
<main>
  <div id="canvas"></div>
  <aside id="panel" aria-live="polite">
    <h2>Detalle</h2>
    <p class="muted" id="panel-body">Haz clic en una tarea, gateway o subproceso.</p>
  </aside>
</main>
<script>
@@VIEWER_JS@@
</script>
<script>
(function () {
  var xml = @@XML_JSON@@;
  var info = @@INFO_JSON@@;
  var viewer = new BpmnJS({
    container: '#canvas',
    textRenderer: {
      defaultStyle: { fontFamily: 'Arial, sans-serif', fontSize: @@FONT@@, lineHeight: 1.2 },
      externalStyle: { fontFamily: 'Arial, sans-serif', fontSize: @@FONT@@, lineHeight: 1.2 }
    }
  });
  window.bpmnViewer = viewer;
  var MIN_ZOOM = 0.6;  // the initial view never shows the diagram smaller than this
  function fitViewport() {
    viewer.get('canvas').zoom('fit-viewport', 'auto');
  }
  function initialView() {
    fitViewport();
    var canvas = viewer.get('canvas');
    if (canvas.zoom() < MIN_ZOOM) {
      // too big to fit legibly: zoom in and start at the diagram's left edge,
      // with the start event in view, instead of in the middle of the flow
      canvas.zoom(MIN_ZOOM);
      var start = viewer.get('elementRegistry').filter(function (el) {
        return el.type === 'bpmn:StartEvent';
      })[0];
      if (start) {
        var box = canvas.getAbsoluteBBox(start);
        var outer = canvas.viewbox().outer;
        canvas.scroll({ dx: 40 - box.x, dy: Math.round(outer.height * 0.4) - box.y });
      }
    }
  }
  function el(tag, text, cls) {
    var node = document.createElement(tag);
    if (text !== undefined && text !== null) { node.textContent = text; }
    if (cls) { node.className = cls; }
    return node;
  }
  function showInfo(id) {
    var data = info[id];
    var body = document.getElementById('panel-body');
    body.className = '';
    body.textContent = '';
    if (!data) {
      body.className = 'muted';
      body.textContent = 'Sin informacion para este elemento.';
      return;
    }
    body.appendChild(el('p', data.label, 'element-label'));
    if (data.detail) {
      body.appendChild(el('h3', data.subprocess ? 'Detalle del grupo' : 'Detalle'));
      body.appendChild(el('p', data.detail));
    }
    body.appendChild(el('h3', 'Ramas salientes'));
    if (!data.branches.length) {
      body.appendChild(el('p', 'Sin ramas.', 'muted'));
    } else {
      var ul = el('ul');
      data.branches.forEach(function (branch) {
        var li = el('li');
        if (branch.label) { li.appendChild(el('span', branch.label, 'branch-label')); li.appendChild(document.createTextNode(' → ')); }
        li.appendChild(document.createTextNode(branch.target));
        ul.appendChild(li);
      });
      body.appendChild(ul);
    }
  }
  viewer.on('element.click', function (evt) { showInfo(evt.element.id); });
  viewer.on('root.set', function () { try { initialView(); } catch (e) {} });
  viewer.importXML(xml).then(function (result) {
    if (result.warnings && result.warnings.length) { console.warn('bpmn-js import warnings', result.warnings); }
    initialView();
    window.bpmnReady = true;
  }).catch(function (err) {
    document.getElementById('error').textContent = 'Could not render the BPMN diagram: ' + err.message;
    console.error(err);
  });
  document.getElementById('fit').addEventListener('click', fitViewport);
  document.getElementById('zoom-in').addEventListener('click', function () { viewer.get('zoomScroll').stepZoom(1); });
  document.getElementById('zoom-out').addEventListener('click', function () { viewer.get('zoomScroll').stepZoom(-1); });
  document.getElementById('toggle-panel').addEventListener('click', function () {
    document.body.classList.toggle('panel-collapsed');
    setTimeout(function () { viewer.get('canvas').resized(); }, 0);
  });
  window.addEventListener('resize', function () { viewer.get('canvas').resized(); });
})();
</script>
</body>
</html>
"""


def render_bpmn_html(xml: str, title: str, metadata: dict | None = None) -> str:
    """A self-contained page that renders `xml` with the vendored bpmn-js NavigatedViewer."""
    # JSON with `<`, `>` and `&` escaped can never close the script element it lives in
    values = {
        "@@DIAGRAM_CSS@@": _script_safe(_vendor("diagram-js.css")),
        "@@BPMN_CSS@@": _script_safe(_vendor("bpmn-js.css")),
        "@@VIEWER_JS@@": _script_safe(_vendor("bpmn-navigated-viewer.production.min.js")),
        "@@XML_JSON@@": _json_for_script(xml),
        "@@INFO_JSON@@": _json_for_script(element_info(xml)),
        "@@META@@": _meta_html(metadata),
        "@@LEGEND@@": _legend_html(xml, metadata),
        "@@FONT@@": "14",
        "@@TITLE@@": html.escape(title),
    }
    return re.sub("|".join(re.escape(k) for k in values), lambda m: values[m.group(0)], HTML_TEMPLATE)


def provenance_comment(text: str) -> str:
    """`text` as an XML comment (`--` is not allowed inside one)."""
    return "<!-- " + text.replace("--", "- -") + " -->\n"


def with_xml_provenance(xml: str, header: str) -> str:
    """The XML with a provenance comment right after its declaration."""
    decl, sep, rest = xml.partition("\n")
    if not decl.startswith("<?xml"):
        return provenance_comment(header) + xml
    return decl + sep + provenance_comment(header) + rest


__all__ = ["render_bpmn_html", "with_xml_provenance", "element_info", "HTML_TEMPLATE"]

FILE:src/specir/visual/renderers/tree.py
"""Tree renderer: collapsible hierarchical HTML from ComponentIR."""

from __future__ import annotations
import json
from specir.visual.ir import ComponentIR, ComponentNode
from specir.visual.exceptions import RenderError


class TreeRenderer:
    """Renders a ComponentIR as a standalone interactive collapsible tree HTML."""

    def render(self, ir) -> str:
        if not isinstance(ir, ComponentIR):
            raise RenderError(f"TreeRenderer cannot render {type(ir).__name__}")
        return self._build_html(ir)

    def _build_html(self, ir: ComponentIR) -> str:
        tree_data = self._build_tree(ir)
        edge_data = self._build_edge_map(ir)
        node_labels = {n.id: n.label for n in ir.nodes}
        node_kinds = {n.id: n.kind for n in ir.nodes}
        return HTML_TEMPLATE.format(
            title=ir.title,
            tree_json=json.dumps(tree_data, indent=2),
            edges_json=json.dumps(edge_data),
            labels_json=json.dumps(node_labels),
            kinds_json=json.dumps(node_kinds),
        )

    def _build_tree(self, ir: ComponentIR) -> dict:
        """Build a nested tree from flat node IDs using their hierarchy."""
        root = {"name": "sldb", "type": "root", "children": []}
        lookup = {n.id: n for n in ir.nodes}

        for node in ir.nodes:
            parts = node.id.split("_")
            current = root
            path = []
            for i, part in enumerate(parts):
                path.append(part)
                full_id = "_".join(path)
                # Check if this intermediate level has a module node
                existing = self._find_child(current, full_id)
                if existing:
                    current = existing
                else:
                    entry = {
                        "name": full_id,
                        "label": lookup.get(full_id, ComponentNode(id=full_id, label=part, kind="module")).label,
                        "type": lookup.get(full_id, ComponentNode(id=full_id, label=part, kind="module")).kind,
                        "children": [],
                    }
                    current["children"].append(entry)
                    current = entry

        self._deduplicate_leaves(root)
        return root

    def _find_child(self, parent: dict, name: str) -> dict | None:
        for c in parent.get("children", []):
            if c["name"] == name:
                return c
        return None

    def _deduplicate_leaves(self, node: dict) -> None:
        """Remove leaf nodes that are just the parent path repeated (e.g.
        module_cli_commands is both a leaf and a parent)."""
        children = node.get("children", [])
        if not children:
            return
        # If a child has no children and its name == parent name (same depth), skip it
        children[:] = [c for c in children if c.get("children") or c["name"] != node["name"]]
        for c in children:
            self._deduplicate_leaves(c)

    def _build_edge_map(self, ir: ComponentIR) -> dict:
        """Build a dict of node_id -> {imports: [target_ids], imported_by: [source_ids]}."""
        edge_map: dict[str, dict[str, list[str]]] = {}
        for n in ir.nodes:
            edge_map[n.id] = {"imports": [], "imported_by": []}
        for e in ir.edges:
            if e.from_ in edge_map and e.to in edge_map:
                edge_map[e.from_]["imports"].append(e.to)
                edge_map[e.to]["imported_by"].append(e.from_)
        return edge_map


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Collapsible Tree</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0a0a0f;color:#f5f0e8;display:flex;height:100vh;overflow:hidden}}
aside{{width:400px;min-width:400px;border-right:1px solid rgba(212,165,116,.2);overflow-y:auto;padding:16px;background:#12121a}}
main{{flex:1;overflow-y:auto;padding:24px}}
.tree-toggle{{cursor:pointer;user-select:none;display:inline-flex;align-items:center;gap:4px}}
.tree-toggle:hover{{color:#d4a574}}
.tree-icon{{display:inline-block;width:16px;text-align:center;color:#d4a574;font-size:12px}}
.node-name{{color:#f5f0e8}}
.node-name:hover{{color:#d4a574}}
.node-kind{{color:rgba(245,240,232,.4);font-size:11px;margin-left:6px}}
ul{{list-style:none;padding-left:16px}}
li{{padding:2px 0}}
li.selected>.tree-toggle>.node-name{{color:#d4a574;font-weight:600}}
.class{{color:#7ec8e3}}
.module{{color:rgba(245,240,232,.7)}}
.external{{color:rgba(245,240,232,.35)}}
.core{{color:#7ec8e3}}
.database{{color:#e3b37e}}
.boundary{{color:rgba(245,240,232,.45)}}
.badge{{font-size:10px;padding:1px 6px;border-radius:8px;margin-left:6px;background:rgba(212,165,116,.15);color:#d4a574}}
#detail-panel{{background:#161621;border:1px solid rgba(212,165,116,.2);border-radius:12px;padding:20px;margin-bottom:16px}}
#detail-panel h3{{font-size:11px;text-transform:uppercase;letter-spacing:.15em;color:#d4a574;margin-bottom:8px}}
#detail-panel p{{margin:4px 0;font-size:13px}}
.dep-list{{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}}
.dep-tag{{font-size:11px;padding:2px 8px;border-radius:6px;background:rgba(212,165,116,.1);color:rgba(245,240,232,.8);cursor:pointer}}
.dep-tag:hover{{background:rgba(212,165,116,.3);color:#f5f0e8}}
.empty-state{{color:rgba(245,240,232,.4);font-size:13px;font-style:italic}}
.search-box{{width:100%;padding:8px 12px;background:#0a0a0f;border:1px solid rgba(212,165,116,.2);border-radius:8px;color:#f5f0e8;font-size:13px;margin-bottom:12px;outline:none}}
.search-box:focus{{border-color:#d4a574}}
#tree-root{{font-size:13px;line-height:1.6}}
#title-bar{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#d4a574;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid rgba(212,165,116,.15)}}
.count{{color:rgba(245,240,232,.35);font-size:11px;margin-left:4px}}
</style>
</head>
<body>
<aside>
<div id="title-bar">📁 {title}</div>
<input class="search-box" id="search" placeholder="Filter nodes..." oninput="filterTree(this.value)">
<div id="tree-root"></div>
</aside>
<main>
<div id="detail-panel">
<h3>🔍 Node Detail</h3>
<p class="empty-state">Click a node in the tree to see its dependencies</p>
</div>
<div id="edge-info" style="color:rgba(245,240,232,.4);font-size:12px"></div>
</main>
<script>
const TREE = {tree_json};
const EDGES = {edges_json};
const LABELS = {labels_json};
const KINDS = {kinds_json};

function treeHTML(node, depth) {{
    const hasKids = node.children && node.children.length > 0;
    const label = LABELS[node.name] || node.label || node.name.split('_').pop();
    const kind = KINDS[node.name] || node.type || 'module';
    const kindClass = kind === 'class' ? 'class' : kind === 'module' ? 'module' : kind === 'external' ? 'external' : kind;
    const count = hasKids ? `<span class="count">${{node.children.length}}</span>` : '';
    const cl = kindClass;
    let html = `<li><div class="tree-toggle" onclick="toggle(this)" data-path="${{node.name}}">`;
    if (hasKids) {{
        html += `<span class="tree-icon">▸</span>`;
    }} else {{
        html += `<span class="tree-icon" style="color:transparent">▸</span>`;
    }}
    html += `<span class="node-name ${{cl}}">${{label}}</span>${{count}}<span class="node-kind">${{kind}}</span>`;
    html += `</div>`;
    if (hasKids) {{
        html += `<ul style="display:none">`;
        for (const c of node.children) {{
            html += treeHTML(c, depth + 1);
        }}
        html += `</ul>`;
    }}
    html += `</li>`;
    return html;
}}

function toggle(el) {{
    const ul = el.nextElementSibling;
    const icon = el.querySelector('.tree-icon');
    if (ul && ul.tagName === 'UL') {{
        const showing = ul.style.display !== 'none';
        ul.style.display = showing ? 'none' : 'block';
        icon.textContent = showing ? '▸' : '▾';
    }}
    showDetail(el.dataset.path);
}}

function showDetail(nodeId) {{
    // Remove selected class
    document.querySelectorAll('.selected').forEach(el => el.classList.remove('selected'));
    const toggles = document.querySelectorAll(`[data-path="${{nodeId}}"]`);
    toggles.forEach(t => t.parentElement.classList.add('selected'));

    const panel = document.getElementById('detail-panel');
    const label = LABELS[nodeId] || nodeId.split('_').pop();
    const kind = KINDS[nodeId] || 'module';
    const deps = EDGES[nodeId];
    if (!deps) {{
        panel.innerHTML = `<h3>🔍 ${{label}}</h3><p class="empty-state">No dependency data</p>`;
        return;
    }}
    let html = `<h3>🔍 ${{label}} <span style="font-weight:400;color:rgba(245,240,232,.4)">(${{kind}})</span></h3>`;
    html += `<p><strong>ID:</strong> <code style="color:#d4a574">${{nodeId}}</code></p>`;
    if (deps.imports.length > 0) {{
        html += `<p><strong>Imports:</strong></p><div class="dep-list">`;
        for (const t of deps.imports) {{
            const tl = LABELS[t] || t.split('_').pop();
            html += `<span class="dep-tag" onclick="showDetail('${{t}}')">${{tl}}</span>`;
        }}
        html += `</div>`;
    }} else {{
        html += `<p><strong>Imports:</strong> <span class="empty-state">none</span></p>`;
    }}
    if (deps.imported_by.length > 0) {{
        html += `<p style="margin-top:12px"><strong>Imported by:</strong></p><div class="dep-list">`;
        for (const t of deps.imported_by) {{
            const tl = LABELS[t] || t.split('_').pop();
            html += `<span class="dep-tag" onclick="showDetail('${{t}}')">${{tl}}</span>`;
        }}
        html += `</div>`;
    }} else {{
        html += `<p style="margin-top:12px"><strong>Imported by:</strong> <span class="empty-state">none</span></p>`;
    }}
    panel.innerHTML = html;
}}

function filterTree(query) {{
    const items = document.querySelectorAll('#tree-root li');
    const q = query.toLowerCase();
    items.forEach(li => {{
        const name = li.querySelector('.node-name');
        if (!name) return;
        const matches = !q || name.textContent.toLowerCase().includes(q);
        li.style.display = matches ? '' : 'none';
        if (matches && q) {{
            // auto-expand parents
            let p = li.parentElement;
            while (p && p.id !== 'tree-root') {{
                if (p.tagName === 'UL') {{
                    p.style.display = 'block';
                    const prev = p.previousElementSibling;
                    if (prev) {{
                        const icon = prev.querySelector('.tree-icon');
                        if (icon) icon.textContent = '▾';
                    }}
                }}
                p = p.parentElement;
            }}
        }}
    }});
}}

// Initialize
document.getElementById('tree-root').innerHTML = `<ul>${{treeHTML(TREE, 0)}}</ul>`;
// Auto-expand first level
document.querySelectorAll('#tree-root > ul > li > ul').forEach(ul => {{
    ul.style.display = 'block';
    const icon = ul.previousElementSibling?.querySelector('.tree-icon');
    if (icon) icon.textContent = '▾';
}});
</script>
</body>
</html>"""

FILE:src/specir/visual/renderers/graph_html.py
"""Pure DOM collapsible hierarchical tree renderer for specIR ComponentIR (migrated from spec2viz).
No external dependencies (no D3, no CDN). Works from file://."""

from __future__ import annotations

import json

from specir.visual.exceptions import RenderError
from specir.visual.ir import ComponentIR


class GraphRenderer:
    """Renders a ComponentIR as a pure-DOM collapsible hierarchical tree."""

    def render(self, ir) -> str:
        if not isinstance(ir, ComponentIR):
            raise RenderError(f"GraphRenderer cannot render {type(ir).__name__}")
        return self._build_html(ir)

    def _build_html(self, ir: ComponentIR) -> str:
        tree_data = self._build_tree(ir)
        edges_map = self._build_edges(ir)
        node_lookup = {n.id: {"label": n.label, "kind": n.kind, "contains": n.contains} for n in ir.nodes}
        return HTML_TEMPLATE.format(
            title=ir.title,
            tree_json=json.dumps(tree_data),
            edges_json=json.dumps(edges_map),
            nodes_json=json.dumps(node_lookup),
        )

    def _build_tree(self, ir: ComponentIR) -> dict:
        lookup = {n.id: n for n in ir.nodes}
        root_children = []
        added = set()

        for node in ir.nodes:
            parts = node.id.split("_")
            current_parents: list[dict] = [{"children": root_children}]
            path = ""
            for part in parts:
                path = f"{path}_{part}" if path else part
                if path in added:
                    continue
                existing = lookup.get(path)
                entry = {
                    "id": path,
                    "label": existing.label if existing else part,
                    "kind": existing.kind if existing else "module",
                    "children": [],
                }
                current_parents[-1]["children"].append(entry)
                current_parents.append(entry)
                added.add(path)
            self._deduplicate_leaves(current_parents[-1] if len(current_parents) > 1 else {"children": root_children})

        tree = {
            "id": "root",
            "label": ir.title.split(" ")[0] if ir.title else "sldb",
            "kind": "root",
            "children": root_children,
        }
        self._sort_children(tree)
        return tree

    def _sort_children(self, node: dict) -> None:
        node["children"].sort(key=lambda c: (not bool(c["children"]), c["label"]))
        for c in node["children"]:
            self._sort_children(c)

    def _deduplicate_leaves(self, parent: dict) -> None:
        children = parent.get("children", [])
        if not children:
            return
        children[:] = [c for c in children if c.get("children") or c["id"] != parent.get("id")]
        for c in children:
            self._deduplicate_leaves(c)

    def _build_edges(self, ir: ComponentIR) -> dict[str, dict[str, list[dict]]]:
        edge_map: dict[str, dict[str, list[dict]]] = {}
        for n in ir.nodes:
            edge_map[n.id] = {"imports": [], "imported_by": []}
        for e in ir.edges:
            if e.from_ in edge_map and e.to in edge_map:
                edge_map[e.from_]["imports"].append({"target": e.to, "relation": e.relation, "label": e.label or e.relation})
                edge_map[e.to]["imported_by"].append({"source": e.from_, "relation": e.relation, "label": e.label or e.relation})
        return edge_map


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Hierarchical Tree</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0a0a0f;color:#f5f0e8;display:flex;height:100vh;overflow:hidden}}
#sidebar{{width:420px;min-width:420px;background:#12121a;border-right:1px solid rgba(212,165,116,.2);display:flex;flex-direction:column;overflow:hidden}}
#tree-scroll{{flex:1;overflow-y:auto;padding:12px 8px 24px}}
#detail-panel{{width:380px;min-width:380px;background:#12121a;border-left:1px solid rgba(212,165,116,.2);padding:20px;overflow-y:auto}}
#title-bar{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#d4a574;padding:16px 16px 12px;border-bottom:1px solid rgba(212,165,116,.15)}}
#search{{margin:8px 12px;padding:8px 12px;background:#0a0a0f;border:1px solid rgba(212,165,116,.2);border-radius:8px;color:#f5f0e8;font-size:13px;outline:none}}
#search:focus{{border-color:#d4a574}}
#stats{{font-size:11px;color:rgba(245,240,232,.4);padding:4px 16px 8px}}
.toolbar{{display:flex;gap:6px;padding:4px 12px 8px;flex-wrap:wrap}}
.toolbar button{{background:#0a0a0f;border:1px solid rgba(212,165,116,.2);color:#f5f0e8;padding:4px 10px;border-radius:6px;cursor:pointer;font-size:11px}}
.toolbar button:hover{{border-color:#d4a574;color:#d4a574}}
.legend{{display:flex;flex-wrap:wrap;gap:6px;padding:4px 12px 10px;border-bottom:1px solid rgba(212,165,116,.1)}}
.legend-item{{display:flex;align-items:center;gap:5px;font-size:10px;color:rgba(245,240,232,.5)}}
.legend-dot{{width:8px;height:8px;border-radius:50%}}
#detail-panel h3{{font-size:11px;text-transform:uppercase;letter-spacing:.15em;color:#d4a574;margin-bottom:10px}}
#detail-panel p{{margin:4px 0;font-size:13px;line-height:1.5}}
.dep-tag{{display:inline-block;font-size:11px;padding:2px 8px;border-radius:6px;background:rgba(212,165,116,.1);color:rgba(245,240,232,.8);cursor:pointer;margin:2px;max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.dep-tag:hover{{background:rgba(212,165,116,.3);color:#f5f0e8}}
.empty-state{{color:rgba(245,240,232,.4);font-size:13px;font-style:italic}}

.tree-ul{{list-style:none;padding-left:0;position:relative}}
.tree-li{{padding:0;position:relative}}
.tree-line{{padding:1px 0 1px 24px;position:relative;display:flex;align-items:center;gap:4px;min-height:22px}}
.tree-line::before{{content:'';position:absolute;left:8px;top:0;bottom:50%;width:1px;background:rgba(212,165,116,.2)}}
.tree-line::after{{content:'';position:absolute;left:8px;top:50%;width:12px;height:1px;background:rgba(212,165,116,.2)}}
.tree-li:last-child>.tree-line::before{{bottom:50%;height:50%}}
.tree-li:only-child>.tree-line::before{{display:none}}
.tree-li:only-child>.tree-line::after{{display:none}}
.tree-root>.tree-line::before,.tree-root>.tree-line::after{{display:none}}
.tree-root{{padding-left:0}}
.tree-toggle{{cursor:pointer;user-select:none;display:inline-flex;align-items:center;gap:4px;padding:1px 4px;border-radius:4px;font-size:13px;line-height:1.5}}
.tree-toggle:hover{{background:rgba(212,165,116,.08)}}
.tree-toggle.selected{{background:rgba(212,165,116,.15);color:#d4a574}}
.tree-toggle.selected .node-name{{color:#d4a574;font-weight:600}}
.tree-icon{{display:inline-block;width:14px;text-align:center;color:#d4a574;font-size:10px;flex-shrink:0}}
.node-name{{color:#f5f0e8}}
.node-name:hover{{color:#d4a574}}
.node-kind-tag{{font-size:9px;padding:0 5px;border-radius:4px;color:rgba(245,240,232,.4);background:rgba(245,240,232,.05);margin-left:2px}}
.node-count{{color:rgba(245,240,232,.3);font-size:10px;margin-left:2px}}
.node-dot{{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:2px;flex-shrink:0}}
.color-core{{background:#7ec8e3}}
.color-module{{background:rgba(245,240,232,.6)}}
.color-class{{background:#7ec8e3}}
.color-database{{background:#e3b37e}}
.color-boundary{{background:rgba(245,240,232,.35)}}
.color-interface{{background:#d4a574}}
.color-external{{background:rgba(245,240,232,.25)}}
.color-root{{background:#d4a574}}
</style>
</head>
<body>
<div id="sidebar">
  <div id="title-bar">📁 {title}</div>
  <input id="search" placeholder="Filter nodes..." oninput="filterTree(this.value)">
  <div class="toolbar">
    <button onclick="expandAll()">⊕ Expand all</button>
    <button onclick="collapseAll()">⊖ Collapse all</button>
    <button onclick="expandDepth(1)">Level 1</button>
    <button onclick="expandDepth(2)">Level 2</button>
    <button onclick="expandDepth(3)">Level 3</button>
  </div>
  <div class="legend" id="legend"></div>
  <div id="stats"></div>
  <div id="tree-scroll">
    <ul class="tree-ul" id="tree-root"></ul>
  </div>
</div>
<div id="detail-panel">
  <h3>Node Detail</h3>
  <p class="empty-state">Click a node to see details</p>
</div>
<script>
const TREE = {tree_json};
const EDGES = {edges_json};
const NODES = {nodes_json};
const DEFAULT_EXPANDED_DEPTH = 2;
const totalNodes = Object.keys(NODES).length;

const KIND_COLORS = {{
  core: '#7ec8e3', module: 'rgba(245,240,232,.6)', class: '#7ec8e3',
  database: '#e3b37e', boundary: 'rgba(245,240,232,.35)',
  interface: '#d4a574', external: 'rgba(245,240,232,.25)', root: '#d4a574'
}};

const LEGEND_ITEMS = [
  ['core','#7ec8e3'],['module','rgba(245,240,232,.6)'],['database','#e3b37e'],
  ['boundary','rgba(245,240,232,.35)'],['interface','#d4a574'],['class','#7ec8e3']
];
document.getElementById('legend').innerHTML = LEGEND_ITEMS.map(([n,c]) =>
  `<span class="legend-item"><span class="legend-dot" style="background:${{c}}"></span>${{n}}</span>`
).join('');

function renderTree(node, depth) {{
  const hasKids = node.children && node.children.length > 0;
  const kind = node.kind || 'module';
  const colorClass = 'color-' + (KIND_COLORS[kind] ? kind : 'module');
  const count = hasKids ? `<span class="node-count">${{node.children.length}}</span>` : '';
  let html = `<li class="tree-li${{depth === 0 ? ' tree-root' : ''}}" data-depth="${{depth}}">`;
  html += `<div class="tree-line">`;
  html += `<span class="node-dot ${{colorClass}}"></span>`;
  if (hasKids) {{
    html += `<span class="tree-toggle" onclick="toggle(this)" data-id="${{node.id}}">`;
    html += `<span class="tree-icon">▸</span>`;
    html += `<span class="node-name">${{node.label}}</span>${{count}}<span class="node-kind-tag">${{kind}}</span>`;
    html += `</span>`;
    html += `</div>`;
    html += `<ul class="tree-ul" style="display:none">`;
    for (const c of node.children) {{
      html += renderTree(c, depth + 1);
    }}
    html += `</ul>`;
  }} else {{
    html += `<span class="tree-toggle no-children" onclick="showDetail('${{node.id}}')" data-id="${{node.id}}">`;
    html += `<span class="tree-icon" style="color:transparent">▸</span>`;
    html += `<span class="node-name">${{node.label}}</span><span class="node-kind-tag">${{kind}}</span>`;
    html += `</span>`;
    html += `</div>`;
  }}
  html += `</li>`;
  return html;
}}

function toggle(el) {{
  const ul = el.parentElement.nextElementSibling;
  const icon = el.querySelector('.tree-icon');
  if (ul && ul.tagName === 'UL') {{
    const showing = ul.style.display !== 'none';
    ul.style.display = showing ? 'none' : 'block';
    icon.textContent = showing ? '▸' : '▾';
  }}
  showDetail(el.dataset.id);
}}

function showDetail(nodeId) {{
  document.querySelectorAll('.tree-toggle.selected').forEach(el => el.classList.remove('selected'));
  document.querySelectorAll(`.tree-toggle[data-id="${{nodeId}}"]`).forEach(el => el.classList.add('selected'));

  const panel = document.getElementById('detail-panel');
  const node = NODES[nodeId];
  if (!node) {{
    panel.innerHTML = `<h3>${{nodeId}}</h3><p class="empty-state">No metadata</p>`;
    return;
  }}
  const ei = EDGES[nodeId] || {{imports:[], imported_by:[]}};
  let html = `<h3>${{node.label}} <span style="font-weight:400;color:rgba(245,240,232,.4)">(${{node.kind}})</span></h3>`;
  html += `<p><strong>ID:</strong> <code style="color:#d4a574;font-size:12px">${{nodeId}}</code></p>`;

  if (ei.imports.length) {{
    html += `<p style="margin-top:8px"><strong>Imports (${{ei.imports.length}}):</strong></p><div>`;
    ei.imports.forEach(i => {{
      const t = NODES[i.target];
      html += `<span class="dep-tag" onclick="showDetail('${{i.target}}')">${{t ? t.label : i.target}}</span>`;
    }});
    html += `</div>`;
  }}
  if (ei.imported_by.length) {{
    html += `<p style="margin-top:8px"><strong>Imported by (${{ei.imported_by.length}}):</strong></p><div>`;
    ei.imported_by.forEach(i => {{
      const s = NODES[i.source];
      html += `<span class="dep-tag" onclick="showDetail('${{i.source}}')">${{s ? s.label : i.source}}</span>`;
    }});
    html += `</div>`;
  }}
  if (!ei.imports.length && !ei.imported_by.length) {{
    html += `<p class="empty-state">No import connections</p>`;
  }}
  if (node.contains && node.contains.length) {{
    html += `<p style="margin-top:8px"><strong>Contains (${{node.contains.length}}):</strong></p><div>`;
    node.contains.forEach(c => {{
      const t = NODES[c];
      html += `<span class="dep-tag" onclick="showDetail('${{c}}')">${{t ? t.label : c}}</span>`;
    }});
    html += `</div>`;
  }}
  panel.innerHTML = html;
}}

function filterBranch(li, query) {{
  const label = li.querySelector(':scope > .tree-line .node-name')?.textContent.toLowerCase() || '';
  const childItems = Array.from(li.querySelectorAll(':scope > .tree-ul > .tree-li'));
  let childMatched = false;
  for (const child of childItems) {{
    if (filterBranch(child, query)) childMatched = true;
  }}
  const selfMatched = !query || label.includes(query);
  const visible = selfMatched || childMatched;
  li.style.display = visible ? '' : 'none';

  const ul = li.querySelector(':scope > .tree-ul');
  const icon = li.querySelector(':scope > .tree-line .tree-icon');
  if (ul) {{
    if (!query) {{
      ul.style.display = 'none';
      if (icon) icon.textContent = '▸';
    }} else if (visible) {{
      ul.style.display = childMatched ? 'block' : 'none';
      if (icon) icon.textContent = childMatched ? '▾' : '▸';
    }}
  }}
  return visible;
}}

function filterTree(query) {{
  const q = query.toLowerCase().trim();
  const roots = Array.from(document.querySelectorAll('#tree-root > .tree-li'));
  roots.forEach(li => filterBranch(li, q));
  if (!q) expandDepth(DEFAULT_EXPANDED_DEPTH);
}}

function expandAll() {{
  document.querySelectorAll('#tree-root .tree-li > .tree-ul').forEach(ul => ul.style.display = 'block');
  document.querySelectorAll('#tree-root .tree-li > .tree-line .tree-icon').forEach(ic => ic.textContent = '▾');
}}

function collapseAll() {{
  document.querySelectorAll('#tree-root .tree-li > .tree-ul').forEach(ul => ul.style.display = 'none');
  document.querySelectorAll('#tree-root .tree-li > .tree-line .tree-icon').forEach(ic => ic.textContent = '▸');
}}

function expandDepth(maxDepth) {{
  document.querySelectorAll('#tree-root .tree-li').forEach(li => {{
    const depth = parseInt(li.dataset.depth || '0', 10);
    const ul = li.querySelector(':scope > .tree-ul');
    if (!ul) return;
    const expanded = depth < maxDepth;
    ul.style.display = expanded ? 'block' : 'none';
    const icon = li.querySelector(':scope > .tree-line .tree-icon');
    if (icon) icon.textContent = expanded ? '▾' : '▸';
  }});
}}

document.getElementById('tree-root').innerHTML = renderTree(TREE, 0);
expandDepth(DEFAULT_EXPANDED_DEPTH);
document.getElementById('stats').textContent = `${{totalNodes}} nodes total`;
</script>
</body>
</html>"""

FILE:src/specir/visual/renderers/antonia_html.py
from __future__ import annotations

import html

from specir.visual.renderers.mermaid import MermaidRenderer

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>antonIA Diagram</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;1,400&family=Manrope:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.min.js"></script>
<style>
  :root{{--bg:#0a0a0f;--amber:#d4a574;--bone:#f5f0e8;--bone-dim:rgba(245,240,232,.6);--line:rgba(212,165,116,.25);--card:#12121a;}}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{background:var(--bg);color:var(--bone);font-family:'Manrope',sans-serif;}}
  section{{padding:44px 6%;}}
  .board{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:26px;overflow-x:auto;}}
  .mermaid{{display:flex;justify-content:center;min-width:600px;}}
</style>
</head>
<body>
<section>
  <div class="board"><pre class="mermaid">
{MERMAID_CONTENT}
  </pre></div>
</section>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'base',
    themeVariables: {{
      darkMode: true,
      background: '#12121a',
      primaryColor: '#1a1a24',
      primaryTextColor: '#f5f0e8',
      primaryBorderColor: '#d4a574',
      lineColor: '#d4a574',
      secondaryColor: '#22222e',
      tertiaryColor: '#12121a',
      fontFamily: 'Manrope, sans-serif',
      fontSize: '14px',
      noteBkgColor: '#2a2233',
      noteTextColor: '#f5f0e8',
      noteBorderColor: '#7c5d94',
      actorBkg: '#1a1a24',
      actorBorder: '#d4a574',
      actorTextColor: '#f5f0e8',
      signalColor: '#d4a574',
      signalTextColor: '#f5f0e8',
      labelBoxBkgColor: '#2a2233',
      labelTextColor: '#f5f0e8',
      loopTextColor: '#f5f0e8',
      altSectionBkgColor: 'rgba(212,165,116,0.06)',
      clusterBkg: 'rgba(245,240,232,0.03)',
      clusterBorder: 'rgba(212,165,116,0.35)',
      edgeLabelBackground: '#12121a',
      titleColor: '#f5f0e8'
    }},
    flowchart: {{ curve: 'basis', htmlLabels: true }},
    sequence: {{ mirrorActors: false, actorMargin: 40 }}
  }});
</script>
</body>
</html>
"""

class AntoniaHtmlRenderer:
    def render(self, ir) -> str:
        mermaid_content = MermaidRenderer().render(ir)
        # The mermaid source goes inside <pre>, so it must be HTML-escaped.
        # Class/sequence diagrams use stereotypes like <<record>>, which the
        # HTML parser would otherwise drop as a bogus tag, leaving mermaid to
        # read a mutilated "<>" from the DOM and fail to render.
        safe_content = html.escape(mermaid_content)
        return TEMPLATE.format(MERMAID_CONTENT=safe_content)

FILE:src/specir/visual/renderers/json_out.py
"""JSON output (`json` renderer, `.artifact.json`), migrated from `spec2viz.renderers.JsonRenderer`."""

from __future__ import annotations


class JsonRenderer:
    def render(self, ir):
        if hasattr(ir, "model_dump"):
            return ir.model_dump()
        return ir


__all__ = ["JsonRenderer"]

FILE:src/specir/visual/renderers/class_diagram.py
"""UML syntax backends for the shared, structured ClassIR."""
import re

from specir.visual.ir import ClassIR

VISIBILITY = {"public": "+", "private": "-", "protected": "#", "package": "~"}
MERMAID_RELATION = {
    "inheritance": "--|>", "realization": "..|>", "composition": "*--",
    "aggregation": "o--", "association": "-->", "dependency": "..>",
}
PLANTUML_RELATION = {**MERMAID_RELATION, "inheritance": "--|>", "realization": "..|>"}


def _mermaid_type(value: str) -> str:
    return value.replace("<", "~").replace(">", "~")


def _mermaid_label(value: str) -> str:
    return value.replace("&", "#amp;").replace("<", "#lt;").replace(">", "#gt;")


def _relation(edge, arrows, escape=lambda value: value):
    source = edge.from_
    target = edge.to
    if edge.from_multiplicity:
        source += f' "{edge.from_multiplicity}"'
    if edge.to_multiplicity:
        target = f'"{edge.to_multiplicity}" ' + target
    line = f'{source} {arrows[edge.relation]} {target}'
    if edge.label:
        line += f' : {escape(edge.label)}'
    return line


def _package_styles(ir: ClassIR) -> list[tuple[str, dict, list[str]]]:
    """(kind, estilo resuelto, clases) por kind de paquete con `style.kinds` neutral: cada clase
    toma el estilo de su paquete mas interno que lo tenga (la misma `resolve_style`)."""
    from specir.visual.notation_style import resolve_style

    styled = {k: {p: v[p] for p in ("fill", "stroke") if v.get(p)} for k, v in ir.style_kinds.items() if isinstance(v, dict)}
    kind_of = {p.id: p.kind for p in ir.packages}
    members: dict[str, list[str]] = {}
    for node in ir.classes:
        owner = ir.package_of(node.id)
        if owner is None:
            continue
        for pid in reversed(ir.package_path(owner)):
            if styled.get(kind_of[pid]):
                members.setdefault(kind_of[pid], []).append(node.id)
                break
    return [(k, resolve_style(None, k, {k: styled[k]}, None), ids) for k, ids in members.items()]


def _mermaid_namespace(label: str) -> str:
    """Nombre de namespace de mermaid: letras, digitos y `_`."""
    return re.sub(r"[^0-9A-Za-z_]+", "_", label).strip("_") or "package"


def _mermaid_class_lines(node, indent: str) -> list[str]:
    lines = [f'{indent}class {node.id}["{_mermaid_label(node.label)}"]', f'{indent}class {node.id} {{']
    if node.kind != "class":
        annotation = "enumeration" if node.kind == "enum" else node.kind
        lines.append(f'{indent}    <<{annotation}>>')
    for attribute in node.attributes:
        modifier = "$" if attribute.static else ""
        lines.append(f'{indent}    {VISIBILITY[attribute.visibility]}{_mermaid_type(attribute.type)} {attribute.name}{modifier}')
    for method in node.methods:
        params = ", ".join(f'{p.name}: {_mermaid_type(p.type)}' for p in method.parameters)
        modifier = "$" if method.static else "*" if method.abstract else ""
        lines.append(f'{indent}    {VISIBILITY[method.visibility]}{method.name}({params}){modifier} {_mermaid_type(method.returns)}')
    lines.append(f'{indent}}}')
    return lines


def render_mermaid_class(ir: ClassIR) -> str:
    lines = ["classDiagram", f"    direction {ir.direction}"]
    by_package: dict[str | None, list] = {}
    for node in ir.classes:
        by_package.setdefault(ir.package_of(node.id), []).append(node)
    for node in by_package.get(None, []):
        lines.extend(_mermaid_class_lines(node, "    "))
    # mermaid no anida `namespace`: cada paquete con clases propias es un namespace con el nombre
    # de su ruta (`Dominio.Facturacion`); PlantUML y graph_ui anidan de verdad
    labels = {p.id: p.label for p in ir.packages}
    for package in ir.packages:
        if package.id not in by_package:
            continue
        name = ".".join(_mermaid_namespace(labels[pid]) for pid in ir.package_path(package.id))
        lines.append(f"    namespace {name} {{")
        for node in by_package[package.id]:
            lines.extend(_mermaid_class_lines(node, "        "))
        lines.append("    }")
    lines.extend('    ' + _relation(edge, MERMAID_RELATION, _mermaid_label) for edge in ir.relations)
    for index, (kind, style, ids) in enumerate(_package_styles(ir)):
        parts = [f"{prop}:{style[prop]['light']}" for prop in ("fill", "stroke") if prop in style]
        lines.append(f"    classDef pkg{index} {','.join(parts)}")
        lines.append(f'    cssClass "{",".join(ids)}" pkg{index}')
    return '\n'.join(lines)


def _plantuml_class_lines(node, indent: str) -> list[str]:
    keyword = {"interface": "interface", "protocol": "interface", "abstract": "abstract class", "enum": "enum"}.get(node.kind, "class")
    stereotype = f' <<{node.kind}>>' if node.kind in {"record", "protocol"} else ""
    lines = [f'{indent}{keyword} "{node.label}" as {node.id}{stereotype} {{']
    for attribute in node.attributes:
        modifier = "{static} " if attribute.static else ""
        lines.append(f'{indent}    {modifier}{VISIBILITY[attribute.visibility]}{attribute.name}: {attribute.type}')
    for method in node.methods:
        modifier = "{static} " if method.static else "{abstract} " if method.abstract else ""
        params = ", ".join(f'{p.name}: {p.type}' for p in method.parameters)
        lines.append(f'{indent}    {modifier}{VISIBILITY[method.visibility]}{method.name}({params}): {method.returns}')
    lines.append(f'{indent}}}')
    return lines


def render_plantuml_class(ir: ClassIR) -> str:
    from specir.visual.notation_style import resolve_style

    lines = ["@startuml", "skinparam classAttributeIconSize 0"]
    if ir.direction == "LR":
        lines.append("left to right direction")
    by_id = {node.id: node for node in ir.classes}
    packages = {p.id: p for p in ir.packages}
    nested = {ref for p in ir.packages for ref in p.contains}
    styled = {k: {q: v[q] for q in ("fill", "stroke") if v.get(q)} for k, v in ir.style_kinds.items() if isinstance(v, dict)}

    def emit_package(package, indent: str) -> None:
        # paquete UML anidado; el relleno (tema claro) de su kind si `style.kinds` lo da
        style = resolve_style(None, package.kind, {package.kind: styled[package.kind]}, None) if styled.get(package.kind) else {}
        color = f" {style['fill']['light']}" if "fill" in style else ""
        lines.append(f'{indent}package "{package.label}" as {package.id}{color} {{')
        for ref in package.contains:
            if ref in packages:
                emit_package(packages[ref], indent + "    ")
            elif ref in by_id:
                lines.extend(_plantuml_class_lines(by_id[ref], indent + "    "))
        lines.append(f"{indent}}}")

    for package in ir.packages:
        if package.id not in nested:
            emit_package(package, "")
    for node in ir.classes:
        if ir.package_of(node.id) is None:
            lines.extend(_plantuml_class_lines(node, ""))
    lines.extend(_relation(edge, PLANTUML_RELATION) for edge in ir.relations)
    lines.append("@enduml")
    return '\n'.join(lines)

FILE:src/specir/visual/renderers/view_mermaid.py
"""Mermaid desde una vista resuelta (`notation_view.resolve_view` / `resolve_documents`).

Es la proyeccion estatica de lo mismo que graph_ui dibuja en vivo: la notacion ya eligio glifo,
forma, keyword, rotulo y compartimentos de cada nodo, el estilo ya esta resuelto con su
precedencia (glifo > style.kinds del spec > paleta) y cada link trae su trazo, terminales, rotulo
y color. Aqui solo se traduce a un `flowchart` de mermaid con layout ELK; nada se recalcula.

Cubre las vistas de layout `graph` (component, deployment, activity, clase, estado, reflection).
Las de `lanes` (secuencia) y `grid` (matriz) no son un grafo: `view_to_mermaid` lanza
`ValueError` y el catalogo usa su fuente renderizada.

Aproximaciones de forma (mermaid no tiene todas las de la notacion): `package` es `notch-rect`
(mermaid no tiene la carpeta con pestana), `note` es `doc`, `node-box`/`artifact`/`class-box` son
rectangulos, `stick-figure` es un estadio. Los iconos (Lucide) son para superficies que los
dibujan; mermaid no los muestra.
"""

from __future__ import annotations

import html
from typing import Any

from specir.visual.renderers.mermaid import FLOWCHART_CONFIG

# forma de la notacion -> nodo de mermaid; `{l}` es el rotulo ya escapado
_SHAPES = {
    "box": '["{l}"]', "node-box": '["{l}"]', "class-box": '["{l}"]', "boundary-box": '["{l}"]',
    "artifact": '["{l}"]', "row-header": '["{l}"]', "column-header": '["{l}"]',
    "rounded-box": '("{l}")', "rounded-container": '("{l}")',
    "diamond": '{{"{l}"}}',
    "cylinder": '[("{l}")]',
    "stick-figure": '(["{l}"])',
    "queue": '@{{ shape: h-cyl, label: "{l}" }}',
    "cloud": '@{{ shape: cloud, label: "{l}" }}',
    "package": '@{{ shape: notch-rect, label: "{l}" }}',
    "note": '@{{ shape: doc, label: "{l}" }}',
}
# formas sin rotulo (pseudonodos)
_BARE = {"filled-circle": "@{ shape: sm-circ }", "bullseye": "@{ shape: fr-circ }"}
_DIRECTIONS = {"TB": "TD", "TD": "TD", "BT": "BT", "LR": "LR", "RL": "RL"}


def _esc(text: Any) -> str:
    """Rotulo de mermaid con htmlLabels: HTML escapado, comillas como entidad de mermaid."""
    return html.escape(str(text), quote=False).replace('"', "#quot;")


def _item(value: Any) -> str:
    """Un elemento de compartimento: atributo `name: type`, metodo `name(params): returns` o texto."""
    if isinstance(value, dict):
        name = value.get("name", "")
        if "parameters" in value or "returns" in value:
            params = ", ".join(f"{p.get('name', '')}: {p.get('type', '')}" if isinstance(p, dict) else str(p) for p in value.get("parameters") or [])
            returns = value.get("returns")
            return f"{name}({params})" + (f": {returns}" if returns else "")
        return f"{name}: {value['type']}" if value.get("type") else str(name)
    return str(value)


def _label(node: dict[str, Any]) -> str:
    """keyword, rotulo y compartimentos del nodo, ya resueltos por la notacion."""
    lines = [_esc(node["keyword"])] if node.get("keyword") else []
    label = _esc(node.get("label", ""))
    if node.get("label_style") == "italic":
        label = f"<i>{label}</i>"
    elif node.get("label_style") == "bold":
        label = f"<b>{label}</b>"
    lines.append(label)
    for compartment in node.get("compartments") or []:
        items = [_esc(_item(v)) for v in compartment.get("items") or []]
        if items:
            lines.append("<hr/>" + "<br/>".join(items))
    return "<br/>".join(l for l in lines if l) or " "


def view_to_mermaid(view: dict[str, Any], theme: str = "dark", ink: str | None = None) -> str:
    """Un `flowchart` de mermaid (ELK) desde una vista resuelta de layout `graph`.

    `theme` elige el lado de cada color `{light, dark}`; `ink` es el color del texto sobre un
    relleno (por defecto el de la paleta default para ese tema).
    """
    layout = view.get("layout") or {}
    if layout.get("kind", "graph") != "graph":
        raise ValueError(f"layout {layout.get('kind')!r} is not a graph; view_to_mermaid draws graph layouts only")
    if ink is None:
        from specir.visual.notation_style import default_ink

        ink = default_ink()[theme]

    nodes = list(view.get("nodes") or [])
    ids = {node["doc"]: f"n{i}" for i, node in enumerate(nodes)}
    by_doc = {node["doc"]: node for node in nodes}
    nest = [l for l in view.get("links") or [] if l.get("draw") == "nest" and l["source"] in ids and l["target"] in ids]
    parent = {}
    for link in nest:
        parent.setdefault(link["target"], link["source"])
    children: dict[str, list[str]] = {}
    for child, owner in parent.items():
        children.setdefault(owner, []).append(child)

    lines = [*FLOWCHART_CONFIG.split("\n"), f"flowchart {_DIRECTIONS.get(str(layout.get('direction') or 'TB'), 'TD')}"]

    def emit(doc: str, indent: str) -> None:
        node = by_doc[doc]
        if doc in children:
            lines.append(f'{indent}subgraph {ids[doc]} ["{_label({**node, "compartments": []})}"]')
            for child in children[doc]:
                emit(child, indent + "    ")
            lines.append(f"{indent}end")
            return
        shape = node.get("shape", "")
        if shape in _BARE:
            lines.append(f"{indent}{ids[doc]}{_BARE[shape]}")
        else:
            lines.append(f"{indent}{ids[doc]}{_SHAPES.get(shape, _SHAPES['box']).format(l=_label(node))}")

    for node in nodes:
        if node["doc"] not in parent:
            emit(node["doc"], "    ")

    # marcas (el pseudoestado inicial de un statechart): un punto que apunta a su elemento
    for node in nodes:
        for index, marker in enumerate(node.get("markers") or []):
            mid = f"{ids[node['doc']]}m{index}"
            lines.append(f"    {mid}{_BARE.get(marker.get('shape', ''), '@{ shape: sm-circ }')}")
            lines.append(f"    {mid} --> {ids[node['doc']]}")

    link_styles: list[str] = []
    edge_index = sum(len(n.get("markers") or []) for n in nodes)
    for link in view.get("links") or []:
        if link.get("draw") == "nest" or link["source"] not in ids or link["target"] not in ids:
            continue
        dashed = link.get("line") in ("dashed", "dotted")
        headless = link.get("target_end", "open-arrow") == "none"
        arrow = ("-.-" if headless else "-.->") if dashed else ("---" if headless else "-->")
        text = " ".join(t for t in (link.get("source_label"), link.get("label"), link.get("target_label")) if t)
        label = f'|"{_esc(text)}"|' if text else ""
        lines.append(f"    {ids[link['source']]} {arrow}{label} {ids[link['target']]}")
        if link.get("color"):
            link_styles.append(f"    linkStyle {edge_index} stroke:{link['color'][theme]}")
        edge_index += 1
    lines.extend(link_styles)

    for node in nodes:
        style = node.get("style") or {}
        parts = [f"{prop}:{style[prop][theme]}" for prop in ("fill", "stroke") if prop in style]
        if parts:
            lines.append(f"    style {ids[node['doc']]} {','.join(parts)},color:{ink}")
    return "\n".join(lines)


__all__ = ["view_to_mermaid"]

FILE:src/specir/visual/lint_mermaid.py
"""Mermaid output linter (migrated from `spec2viz.linters.mermaid`).

Catches syntax that parses server-side but breaks the mermaid.js parser in the
browser. Each rule maps a regex to a human explanation so the failure names the
exact line and the fix, instead of a blank diagram at view time.

Scope: sequenceDiagram, flowchart/graph, stateDiagram. The linter is
conservative: it only flags patterns known to hard-fail mermaid rendering.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from specir.visual.exceptions import RenderError


class MermaidLintError(RenderError):
    """Rendered mermaid text contains a browser-breaking construct."""


@dataclass(frozen=True)
class _Rule:
    name: str
    pattern: re.Pattern[str]
    message: str


# First non-empty line declares the diagram kind.
_HEADER_KINDS = (
    "sequenceDiagram",
    "flowchart",
    "graph",
    "stateDiagram",
    "stateDiagram-v2",
    "classDiagram",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
)

# Valid mermaid sequence arrows. Anything else between two participants that
# looks like an arrow is almost always a renderer bug.
_VALID_SEQ_ARROWS = ("->>", "-->>", "->", "-->", "-x", "--x", "-)", "--)")

_RULES: tuple[_Rule, ...] = (
    _Rule(
        name="invalid-return-arrow",
        # "A<<--B" or "A <<-- B": the reversed dashed arrow is not mermaid.
        pattern=re.compile(r"\S\s*<<--\s*\S"),
        message=(
            "invalid sequence arrow '<<--'. Mermaid return arrows are '-->>'. "
            "Use kind: return -> '-->>' (dashed, forward)."
        ),
    ),
    _Rule(
        name="raw-angle-brackets",
        # Unescaped <...> inside a message/label is parsed as HTML by mermaid
        # and silently drops or breaks the node. Only fires outside of a
        # recognised arrow token.
        pattern=re.compile(r"(?<![-<>x)])<(?!<)[^<>\n]*>"),
        message=(
            "raw '<...>' in a label/message is parsed as HTML by mermaid and "
            "breaks the diagram. Escape as '&lt;...&gt;' or drop the brackets."
        ),
    ),
    _Rule(
        name="empty-label-braces",
        pattern=re.compile(r"\{\s*\"\"\s*\}|\{\s*\}"),
        message="empty decision node label '{}' is not renderable.",
    ),
)


def mmdc_path() -> str | None:
    """Return the mermaid-cli binary path if available, else None.

    Honors SPECIR_MMDC (or, as spec2viz did, SPEC2VIZ_MMDC) to point at a
    specific binary. Set it to 0 (or 'off'/'false') to force-disable the
    real-parser check.
    """
    override = os.environ.get("SPECIR_MMDC", os.environ.get("SPEC2VIZ_MMDC"))
    if override in {"0", "off", "false", "no"}:
        return None
    if override:
        return override if (Path(override).exists() or shutil.which(override)) else None
    return shutil.which("mmdc")


def _mmdc_check(text: str) -> list[str]:
    """Parse the mermaid text with the real mermaid-cli engine.

    Returns a list of problems (empty = clean). If mmdc is not installed the
    check is skipped and returns []. This is the source of truth: it catches
    browser-breaking syntax the regex heuristics miss (unescaped '()', '{}',
    nested quotes, HTML entities, etc.).
    """
    binary = mmdc_path()
    if not binary:
        return []
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "diagram.mmd"
        out = Path(td) / "diagram.svg"
        src.write_text(text, encoding="utf-8")
        try:
            proc = subprocess.run(
                [binary, "-i", str(src), "-o", str(out)],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:  # pragma: no cover
            return [f"mmdc could not run ({exc}); skipping real-parser check."]
        if proc.returncode == 0 and out.exists():
            return []
        detail = _extract_mmdc_error(proc.stdout, proc.stderr)
        return [f"mermaid engine (mmdc) rejected the diagram:\n    {detail}"]


def _extract_mmdc_error(stdout: str, stderr: str) -> str:
    blob = "\n".join(p for p in (stdout, stderr) if p).strip()
    lines = [ln for ln in blob.splitlines() if ln.strip()]
    picked = [ln.strip() for ln in lines if re.search(r"error|parse|expecting", ln, re.I)]
    chosen = picked or lines
    return "\n    ".join(chosen[:6]) or "unknown mmdc failure"


def _looks_like_sequence(text: str) -> bool:
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s.startswith("sequenceDiagram")
    return False


def _check_sequence_arrows(text: str) -> list[str]:
    """Flag sequence message lines whose arrow token is not valid mermaid."""
    problems: list[str] = []
    msg_re = re.compile(r"^\s*(\w+)\s*([-<>x()]{2,4})\s*(\w+)\s*:")
    for i, line in enumerate(text.splitlines(), 1):
        m = msg_re.match(line)
        if not m:
            continue
        arrow = m.group(2)
        if arrow not in _VALID_SEQ_ARROWS:
            problems.append(
                f"line {i}: invalid sequence arrow '{arrow}'. "
                f"Valid arrows: {', '.join(_VALID_SEQ_ARROWS)}."
            )
    return problems


def lint_mermaid(text: str, *, check_html: bool = True) -> list[str]:
    """Return a list of human-readable problems. Empty list means clean.

    check_html controls the raw-angle-bracket rule. Pass check_html=False when
    the caller will HTML-escape the content before embedding (e.g. the deskops
    build wraps mermaid in <pre> and escapes '<' to '&lt;' itself), so raw
    '<...>' in labels is safe in that path. Leave it True for standalone .mmd
    output that a mermaid engine parses verbatim.

    Does not raise; callers decide whether to raise MermaidLintError.
    """
    problems: list[str] = []
    lines = text.splitlines()

    for rule in _RULES:
        if rule.name == "raw-angle-brackets" and not check_html:
            continue
        for i, line in enumerate(lines, 1):
            if rule.pattern.search(line):
                problems.append(f"line {i}: {rule.message}\n    -> {line.strip()}")

    if _looks_like_sequence(text):
        problems.extend(_check_sequence_arrows(text))

    problems.extend(_mmdc_check(text))

    return problems


def assert_mermaid_ok(
    text: str, *, source: str | None = None, check_html: bool = True
) -> None:
    """Raise MermaidLintError if the mermaid text has breaking constructs."""
    problems = lint_mermaid(text, check_html=check_html)
    if problems:
        where = f" in {source}" if source else ""
        joined = "\n  - ".join(problems)
        raise MermaidLintError(
            f"Mermaid lint failed{where} ({len(problems)} issue(s)):\n  - {joined}"
        )


__all__ = ["MermaidLintError", "assert_mermaid_ok", "lint_mermaid", "mmdc_path"]

FILE:src/specir/visual/schema.py
"""JSON Schema export of diagram specs (per type or all) and of catalogs / diagram stores, migrated
from `spec2viz.schema`. The models are sldb's (D3); only the export is specIR's."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Type

from pydantic import TypeAdapter

from specir.visual.spec_models import (
    ActivityDiagram,
    AnyDiagram,
    BaseDiagram,
    ClassDiagram,
    ComponentDiagram,
    DeploymentDiagram,
    DiagramStoreEnvelope,
    DiagramType,
    MatrixDiagram,
    SequenceDiagram,
    StateDiagram,
)


_MODEL_BY_TYPE: dict[DiagramType, Type[BaseDiagram]] = {
    DiagramType.class_: ClassDiagram,
    DiagramType.sequence: SequenceDiagram,
    DiagramType.state: StateDiagram,
    DiagramType.component: ComponentDiagram,
    DiagramType.activity: ActivityDiagram,
    DiagramType.deployment: DeploymentDiagram,
    DiagramType.component_view_matrix: MatrixDiagram,
}


def json_schema(diagram_type: str | DiagramType | None = None) -> dict:
    if diagram_type is None:
        return TypeAdapter(AnyDiagram).json_schema()

    if str(diagram_type) in {"diagram-store", "catalog", "project"}:
        return DiagramStoreEnvelope.model_json_schema()

    resolved_type = DiagramType(diagram_type)
    return _MODEL_BY_TYPE[resolved_type].model_json_schema()


def write_json_schema(
    path: str | Path,
    diagram_type: str | DiagramType | None = None,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(json_schema(diagram_type), indent=2))
    return output_path


__all__ = ["json_schema", "write_json_schema"]

FILE:src/specir/visual/render_file.py
"""Render a spec file to an output file, with its provenance header (migrated from
`spec2viz.render_to_file` and its helpers).

The spec is loaded and validated by sldb (`sldb.api.notations.load_spec`/`validate_spec`, D3),
compiled by specIR's compilers (IR11) and drawn by specIR's renderers. A text output carries a header
that names its spec and the specIR command that validates it; a BPMN output is written twice, as
`<stem>.bpmn` (the XML) and `<stem>.bpmn.html` (the offline bpmn-js viewer)."""

from __future__ import annotations

import json
from pathlib import Path

from sldb.api.notations import load_spec, validate_spec

from specir.visual.compilers import compile_ir
from specir.visual.renderers import DEFAULT_RENDERER, EXT_MAP, render
from specir.visual.spec_models import BaseDiagram

#: The command that names the projections it writes (spec2viz wrote `spec2viz`).
COMMAND = "specir"


def render_to_file(
    path: str | Path,
    out: str | Path = ".",
    renderer: str | None = None,
) -> Path:
    path = Path(path)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    diagram = load_spec(path)
    validate_spec(diagram)
    ir = compile_ir(diagram)
    renderer_name = renderer or DEFAULT_RENDERER[type(ir)]
    ext = EXT_MAP[renderer_name]
    output_path = out_dir / (path.stem + ext)

    result = render(ir, renderer_name)
    if renderer_name == "bpmn":
        return _write_bpmn(path, output_path, result, diagram)
    if isinstance(result, dict):
        output_path.write_text(json.dumps(result, indent=2))
    else:
        result = with_provenance(renderer_name, path, result)
        if renderer_name == "mermaid":
            from specir.visual.lint_mermaid import assert_mermaid_ok

            assert_mermaid_ok(result, source=path.name)
        output_path.write_text(result)

    return output_path


def _write_bpmn(spec_path: Path, output_path: Path, xml: str, diagram: BaseDiagram) -> Path:
    """`<stem>.bpmn` (the XML) and `<stem>.bpmn.html` (the offline bpmn-js viewer)."""
    from specir.visual.renderers.bpmn import render_bpmn_html, with_xml_provenance

    output_path.write_text(with_xml_provenance(xml, provenance_text(spec_path)), encoding="utf-8")
    # description, preguntas_abiertas and legend are typed fields of the metadata model
    metadata = diagram.metadata.model_dump() if diagram.metadata else None
    page = render_bpmn_html(xml, diagram.title, metadata)
    output_path.with_name(output_path.name + ".html").write_text(page, encoding="utf-8")
    return output_path


# sintaxis de comentario de linea de cada salida de texto
_COMMENT_PREFIX = {"mermaid": "%%", "plantuml": "'", "d2": "#"}


def with_provenance(renderer_name: str, spec_path: str | Path, text: str) -> str:
    """El texto con su cabecera de trazabilidad. En mermaid, un frontmatter de config (`---`) tiene
    que ser la primera linea, asi que la cabecera va justo despues de el."""
    header = provenance_header(renderer_name, spec_path)
    if header and text.startswith("---\n"):
        end = text.find("\n---\n", 3)
        if end != -1:
            cut = end + len("\n---\n")
            return text[:cut] + header + text[cut:]
    return header + text


def provenance_header(renderer_name: str, spec_path: str | Path) -> str:
    """La cabecera de trazabilidad de una proyeccion de texto: de que spec sale y como se
    valida, para que nadie la edite a mano. Vacia para las salidas sin sintaxis de comentario."""
    prefix = _COMMENT_PREFIX.get(renderer_name)
    if prefix is None:
        return ""
    return f"{prefix} {provenance_text(spec_path)}\n"


def provenance_text(spec_path: str | Path) -> str:
    """El texto de la cabecera de trazabilidad, sin sintaxis de comentario."""
    spec = Path(spec_path)
    try:
        shown = spec.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        shown = spec
    return f"{COMMAND}: generated from {shown.as_posix()}; do not edit, run `{COMMAND} diagram validate {shown.as_posix()}` and re-render"


__all__ = ["COMMAND", "provenance_header", "provenance_text", "render_to_file", "with_provenance"]

FILE:src/specir/visual/commands.py
"""The render, lint and schema commands of the visual layer, migrated from `spec2viz.cli`.

`diagram render|lint|schema` and `catalog schema` keep spec2viz's arguments, options (`--renderer`
with its alias `--backend` and its nine values) and output. `diagram validate` runs sldb's
`load_spec`/`validate_spec` (D3) and is the command the provenance header of a projection names.
`main` is the `specir` command until IR13d gives it its full taxonomy (`src/specir/cli.py`), which
mounts these two groups; the top-level aliases and the rest of spec2viz's commands are IR13d's."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from sldb.api.notations import load_spec, validate_spec

from specir.visual.exceptions import Spec2VizError
from specir.visual.notation_style import NotationError
from specir.visual.render_file import render_to_file
from specir.visual.renderers import RENDERER_MAP
from specir.visual.schema import json_schema, write_json_schema

#: The values of `--renderer`, in spec2viz's order (the keys of the render dispatch).
DIAGRAM_RENDERERS = ["plantuml", "mermaid", "vega", "d2", "antonia-html", "tree", "graph", "bpmn", "json"]
assert set(DIAGRAM_RENDERERS) == set(RENDERER_MAP)

#: What a spec, a render or a lint can fail with: specIR's visual errors and sldb's notation errors.
ERRORS = (Spec2VizError, NotationError)


def _render_paths(paths: list[Path], out: Path, renderer: str | None):
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} -> {output}")
            if renderer == "bpmn":
                click.echo(f"Rendered {path.name} -> {output.with_name(output.name + '.html')}")
        except ERRORS as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)


def _validate_paths(paths: list[Path]):
    for path in paths:
        try:
            validate_spec(load_spec(path))
            click.echo(f"{path.name}: OK")
        except ERRORS as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            sys.exit(1)


def _lint_paths(paths: list[Path]):
    """Lint mermaid text files (.mmd) or render specs to mermaid then lint."""
    from specir.visual.compilers import compile_ir
    from specir.visual.lint_mermaid import lint_mermaid
    from specir.visual.renderers import render

    had_issue = False
    for path in paths:
        try:
            if path.suffix == ".mmd":
                text = path.read_text(encoding="utf-8")
            else:
                text = render(compile_ir(load_spec(path)), "mermaid")
            problems = lint_mermaid(text)
        except ERRORS as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            had_issue = True
            continue
        if problems:
            had_issue = True
            click.echo(f"{path.name}: {len(problems)} issue(s)", err=True)
            for p in problems:
                click.echo(f"  - {p}", err=True)
        else:
            click.echo(f"{path.name}: OK")
    if had_issue:
        sys.exit(1)


def _write_schema(diagram_type: str | None, out: Path | None):
    if out:
        write_json_schema(out, diagram_type=diagram_type)
        click.echo(f"Wrote schema to {out}")
    else:
        click.echo(json.dumps(json_schema(diagram_type), indent=2))


@click.group(help="specIR's visual layer: render, lint and export the schema of diagram specs.")
def main():
    pass


@main.group(help="Work with semantic diagram specs.")
def diagram():
    pass


@main.group(help="Work with diagram catalogs, vistas registries, and hierarchical stores.")
def catalog():
    pass


@diagram.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option(
    "--renderer",
    "--backend",
    type=click.Choice(DIAGRAM_RENDERERS),
    default=None,
    help="Force a renderer instead of using the spec type default.",
)
def diagram_render(paths: list[Path], out: Path, renderer: str | None):
    """Render one or more semantic diagram spec files."""
    _render_paths(paths, out, renderer)


@diagram.command("validate", short_help="Validate semantic diagram spec files (sldb's load_spec and validate_spec).")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def diagram_validate(paths: list[Path]):
    """Validate one or more semantic diagram spec files."""
    _validate_paths(paths)


@diagram.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def diagram_lint(paths: list[Path]):
    """Lint .mmd files, or render specs to mermaid and lint the result."""
    _lint_paths(paths)


@diagram.command("schema", short_help="Export JSON Schema for semantic diagram specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one type: class, sequence, state, component, activity, deployment, component_view_matrix, or diagram-store.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def diagram_schema(diagram_type: str | None, out: Path | None):
    """Export JSON Schema for all diagram spec types or one diagram type."""
    _write_schema(diagram_type, out)


@catalog.command("schema", short_help="Export JSON Schema for hierarchical diagram stores.")
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def catalog_schema(out: Path | None):
    """Export JSON Schema for diagram-store / project.yml configs."""
    _write_schema("diagram-store", out)


__all__ = ["DIAGRAM_RENDERERS", "catalog", "diagram", "main"]

FILE:src/specir/visual/templates/default.html
<!DOCTYPE html>
<html lang="es" data-lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{CATALOG_TITLE}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;1,400&family=Manrope:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <!-- mermaid con el layout ELK (aristas ortogonales, mejor con nodos anidados): modulos ES; se
       ejecutan antes de DOMContentLoaded, donde se inicializa y se dibuja -->
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.12.1/dist/mermaid.esm.min.mjs';
    import elkLayouts from 'https://cdn.jsdelivr.net/npm/@mermaid-js/layout-elk@0.2.3/dist/mermaid-layout-elk.esm.min.mjs';
    mermaid.registerLayoutLoaders(elkLayouts);
    window.mermaid = mermaid;
  </script>
  <style>
    :root{--bg:#0a0a0f;--amber:#d4a574;--bone:#f5f0e8;--bone-dim:rgba(245,240,232,.62);--line:rgba(212,165,116,.22);--card:#12121a;--card-2:#161621;--panel-shadow:0 18px 48px rgba(0,0,0,.45);--sidebar-w:360px;--drawer-w:420px;}
    *{box-sizing:border-box;margin:0;padding:0}
    html,body{height:100%}
    body{font-family:'Manrope',sans-serif;background:var(--bg);color:var(--bone);display:flex;overflow:hidden}
    a{color:inherit}

    aside{
      width:var(--sidebar-w);
      min-width:var(--sidebar-w);
      background:linear-gradient(180deg,rgba(18,18,26,.98),rgba(10,10,15,.98));
      border-right:1px solid var(--line);
      display:flex;
      flex-direction:column;
      position:relative;
      z-index:20;
    }

    .brand{
      padding:24px 22px 18px;
      border-bottom:1px solid var(--line);
    }
    .brand-kicker{
      font-family:'JetBrains Mono',monospace;
      font-size:10px;
      letter-spacing:.18em;
      text-transform:uppercase;
      color:var(--amber);
      margin-bottom:10px;
    }
    .brand-title{
      font-family:'Fraunces',serif;
      font-size:28px;
      font-weight:300;
      line-height:1.1;
    }
    .brand-title em{color:var(--amber);font-style:italic}
    .brand-sub{
      margin-top:10px;
      font-family:'JetBrains Mono',monospace;
      font-size:10px;
      letter-spacing:.14em;
      text-transform:uppercase;
      color:var(--bone-dim);
      line-height:1.5;
    }

    .sidebar-scroll{
      flex:1;
      overflow-y:auto;
      padding:16px 14px 18px;
      display:flex;
      flex-direction:column;
      gap:16px;
    }

    .sidebar-sticky-actions{
      position:sticky;
      top:0;
      z-index:25;
      margin:-16px -14px 0;
      padding:12px 14px 14px;
      background:linear-gradient(180deg,rgba(10,10,15,.98),rgba(10,10,15,.92) 78%,rgba(10,10,15,0));
    }

    .sidebar-card{
      background:rgba(18,18,26,.9);
      border:1px solid var(--line);
      border-radius:14px;
      padding:14px;
      box-shadow:var(--panel-shadow);
    }
    .sidebar-card-title{
      font-family:'JetBrains Mono',monospace;
      font-size:10px;
      letter-spacing:.18em;
      text-transform:uppercase;
      color:var(--amber);
      margin-bottom:12px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      user-select: none;
    }
    .sidebar-card-title::after {
      content: '▾';
      font-size: 12px;
      transition: transform 0.2s ease;
    }
    .sidebar-card.collapsed .sidebar-card-title {
      margin-bottom: 0;
    }
    .sidebar-card.collapsed .sidebar-card-title::after {
      transform: rotate(-90deg);
    }
    .sidebar-card.collapsed > :not(.sidebar-card-title) {
      display: none !important;
    }

    nav{display:flex;flex-direction:column;gap:10px}
    .nav-category{
      border:1px solid var(--line);
      border-radius:12px;
      background:rgba(245,240,232,.02);
      overflow:hidden;
    }
    .nav-category-head{
      width:100%;
      background:none;
      border:none;
      color:var(--bone);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      padding:12px 14px;
      cursor:pointer;
      text-align:left;
    }
    .nav-category-head:hover{background:rgba(212,165,116,.08)}
    .nav-category-label{
      font-family:'JetBrains Mono',monospace;
      font-size:11px;
      letter-spacing:.12em;
      text-transform:uppercase;
      color:var(--amber);
    }
    .nav-category-arrow{
      color:var(--bone-dim);
      font-size:12px;
      transition:transform .2s ease;
    }
    .nav-category.collapsed .nav-category-arrow{transform:rotate(-90deg)}
    .nav-links{
      display:flex;
      flex-direction:column;
      gap:6px;
      padding:0 10px 10px;
    }
    .nav-category.collapsed .nav-links{display:none}
    .nav-links a{
      text-decoration:none;
      border:1px solid var(--line);
      border-radius:10px;
      padding:9px 10px;
      color:var(--bone-dim);
      font-family:'JetBrains Mono',monospace;
      font-size:11px;
      line-height:1.45;
      transition:.2s;
      background:rgba(255,255,255,.01);
    }
    .nav-links a:hover,
    .nav-links a.active{color:var(--amber);border-color:var(--amber);background:rgba(212,165,116,.08)}

    .catalog-toolbar{display:flex;flex-direction:column;gap:12px}
    .catalog-toolbar-row{display:flex;flex-direction:column;gap:12px;margin:0}
    .catalog-toolbar label{
      display:flex;
      flex-direction:column;
      gap:6px;
      font-family:'JetBrains Mono',monospace;
      font-size:10px;
      letter-spacing:.08em;
      text-transform:uppercase;
      color:var(--bone-dim);
    }
    .catalog-toolbar select,
    .catalog-toolbar input,
    .sidebar-btn{
      width:100%;
      background:var(--card);
      color:var(--bone);
      border:1px solid var(--line);
      border-radius:10px;
      padding:10px 12px;
      font-family:'Manrope',sans-serif;
      font-size:13px;
    }
    .catalog-toolbar input::placeholder{color:var(--bone-dim)}
    .catalog-tags{display:flex;flex-wrap:wrap;gap:8px}
    .tag-chip,.meta-badge{
      border:1px solid var(--line);
      background:var(--card);
      color:var(--bone-dim);
      border-radius:999px;
      padding:5px 10px;
      font-size:11px;
      cursor:pointer;
      font-family:'JetBrains Mono',monospace;
    }
    .tag-chip.active,.sidebar-btn.active{
      background:var(--amber);
      color:var(--bg);
      border-color:var(--amber);
      font-weight:600;
    }

    .sidebar-actions{display:flex;flex-direction:column;gap:10px}
    .sidebar-btn{
      cursor:pointer;
      transition:.2s;
      font-family:'JetBrains Mono',monospace;
      letter-spacing:.04em;
      text-transform:uppercase;
    }
    .sidebar-btn:hover{color:var(--amber);border-color:var(--amber)}
    .sidebar-btn.ghost{background:transparent}
    .sidebar-note{
      color:var(--bone-dim);
      font-size:12px;
      line-height:1.55;
    }

    main{
      flex:1;
      overflow-y:auto;
      padding:34px 42px 48px;
      position:relative;
    }
    .catalog-header{margin-bottom:24px}
    .catalog-kicker{
      font-family:'JetBrains Mono',monospace;
      font-size:11px;
      letter-spacing:.18em;
      text-transform:uppercase;
      color:var(--amber);
      margin-bottom:12px;
    }
    .catalog-title{
      font-family:'Fraunces',serif;
      font-size:36px;
      font-weight:300;
      line-height:1.1;
    }
    .catalog-title em{color:var(--amber);font-style:italic}
    .catalog-meta{
      margin-top:10px;
      color:var(--bone-dim);
      font-size:14px;
    }

    .macro-separator{margin:34px 0 18px}
    .macro-separator h2{
      font-family:'JetBrains Mono',monospace;
      font-size:16px;
      letter-spacing:.1em;
      text-transform:uppercase;
      color:var(--amber);
      border-bottom:1px solid var(--line);
      padding-bottom:10px;
    }

    section{
      background:rgba(18,18,26,.9);
      border:1px solid var(--line);
      border-radius:14px;
      padding:28px;
      margin-bottom:28px;
      box-shadow:var(--panel-shadow);
      scroll-margin-top:22px;
    }
    .lbl{
      font-family:'JetBrains Mono',monospace;
      font-size:10px;
      letter-spacing:.22em;
      text-transform:uppercase;
      color:var(--amber);
      margin-bottom:10px;
    }
    section h2{
      font-family:'Fraunces',serif;
      font-weight:400;
      font-size:26px;
      margin-bottom:10px;
    }
    section .desc{
      color:var(--bone-dim);
      margin-bottom:18px;
      line-height:1.65;
      font-size:14px;
    }
    .section-meta{display:flex;flex-wrap:wrap;gap:8px;margin:-2px 0 16px}
    .meta-badge{cursor:default}
    .meta-badge.subtle{opacity:.86}

    .board{
      position:relative;
      background:var(--card);
      border:1px solid var(--line);
      border-radius:10px;
      padding:24px;
      overflow:auto;
    }
    .diagram-viewport{
      position:relative;
      overflow:auto;
      min-height:320px;
      cursor:grab;
    }
    .diagram-viewport.dragging{cursor:grabbing}
    .diagram-canvas{
      transform-origin:top left;
      width:max-content;
      min-width:100%;
      padding-bottom:28px;
    }
    .mermaid{display:block;min-width:max-content;padding-bottom:12px}
    .vega-host{padding:8px}
    .source-board{font-family:'JetBrains Mono',monospace;font-size:12px;white-space:pre-wrap;margin:0;padding:12px}
    .atom-refs{margin-top:14px;padding-top:10px;border-top:1px solid rgba(212,165,116,.25)}
    .atom-refs h4{margin:0 0 6px}
    .atom-refs ul{list-style:none;padding:0;margin:0}
    .atom-refs li{margin:0 0 8px}
    .atom-refs code{font-size:11px;opacity:.75}
    .atom-refs .ref-summary{font-size:12px;opacity:.8;margin-top:2px}
    .atom-edges{list-style:none;padding:0;margin:6px 0 0 10px;font-size:12px}
    .atom-edges li{margin:2px 0}
    .atom-edges .edge-dir{opacity:.6;margin-right:4px}
    .atom-edges code{font-size:11px;opacity:.75}
    .mermaid svg,
    .puml-board svg,
    .diagram-canvas svg{display:block;max-width:none;height:auto;margin:0 auto;overflow:visible}

    .board-controls{
      position:absolute;
      top:14px;
      right:14px;
      display:flex;
      gap:8px;
      z-index:10;
    }
    .board-btn{
      background:rgba(18,18,26,.78);
      border:1px solid var(--line);
      color:var(--bone-dim);
      padding:6px 10px;
      border-radius:6px;
      cursor:pointer;
      font-size:14px;
      font-family:'JetBrains Mono',monospace;
      transition:.2s;
      min-width:36px;
    }
    .board-btn:hover{color:var(--amber);border-color:var(--amber);background:rgba(18,18,26,.95)}
    .board:fullscreen{background:var(--bg);overflow:auto;padding:20px}
    .board:fullscreen .diagram-viewport{min-height:calc(100vh - 80px)}

    .mermaid .node,
    .mermaid g.classGroup,
    .mermaid g.stateGroup,
    .mermaid rect.actor,
    .mermaid g.cluster{transition:.22s ease}
    .mermaid .node:hover,
    .mermaid g.classGroup:hover,
    .mermaid g.stateGroup:hover,
    .mermaid rect.actor:hover,
    .mermaid g.cluster:hover{filter:drop-shadow(0 0 6px rgba(212,165,116,.45))}
    body.anno-mode .mermaid .node:hover,
    body.anno-mode .mermaid g.classGroup:hover,
    body.anno-mode .mermaid g.stateGroup:hover,
    body.anno-mode .mermaid rect.actor:hover,
    body.anno-mode .mermaid g.cluster:hover{filter:drop-shadow(0 0 8px var(--amber));cursor:crosshair}
    .anno-marked{filter:drop-shadow(0 0 8px var(--amber)) !important}
+
    .anno-popup{
      position:fixed;
      z-index:1200;
      width:320px;
      max-height:440px;
      overflow-y:auto;
      background:rgba(18,18,26,.98);
      border:1px solid var(--amber);
      border-radius:10px;
      padding:14px;
      box-shadow:0 16px 40px rgba(0,0,0,.55);
    }
    .anno-popup .who{color:var(--amber);font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;line-height:1.5;margin-bottom:10px}
    .anno-popup .prev{border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:rgba(245,240,232,.03);font-size:13px;line-height:1.55;color:var(--bone-dim);margin-bottom:8px}
    .anno-popup .prev span{display:block;margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--amber)}
    .anno-popup textarea{width:100%;min-height:96px;background:var(--card);color:var(--bone);border:1px solid var(--line);border-radius:8px;padding:10px 12px;resize:vertical;font-family:'Manrope',sans-serif;font-size:13px;margin-top:8px}
    .anno-popup .row{display:flex;gap:8px;margin-top:10px}
    .anno-popup button{flex:1;background:var(--card);color:var(--bone);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-family:'JetBrains Mono',monospace;font-size:11px;text-transform:uppercase;cursor:pointer}
    .anno-popup button:hover{color:var(--amber);border-color:var(--amber)}
    .anno-pin{pointer-events:none}

    .gap-notes{margin-top:14px;border:1px solid var(--line);border-radius:10px;padding:16px 20px;background:rgba(227,76,76,.05)}
    .gap-notes strong{color:#e07a6a;font-size:13px;letter-spacing:.08em;text-transform:uppercase}
    .gap-notes ul{margin:10px 0 0 18px;color:var(--bone-dim);font-size:14px;line-height:1.6}

    #hover-popover{
      position:fixed;
      display:none;
      z-index:1000;
      background:rgba(18,18,26,.96);
      border:1px solid var(--amber);
      border-radius:8px;
      padding:14px 18px;
      box-shadow:0 10px 25px rgba(0,0,0,.6);
      width:320px;
      backdrop-filter:blur(10px);
    }
    #hover-popover .title{font-size:.95rem;font-weight:700;color:var(--amber);margin-bottom:8px;border-bottom:1px solid var(--line);padding-bottom:4px}
    #hover-popover .badges{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:8px}
    .badge{font-size:.65rem;font-weight:700;text-transform:uppercase;padding:3px 6px;border-radius:4px;background:var(--bg);color:var(--bone-dim);border:1px solid var(--line)}
    .badge.active{background:var(--amber);color:var(--bg);border-color:var(--amber)}
    #hover-popover .snippet{font-size:.82rem;color:var(--bone);line-height:1.45;max-height:96px;overflow:hidden}

    #atom-panel{
      width:var(--drawer-w);
      background:var(--card-2);
      border-right:1px solid var(--line);
      display:flex;
      flex-direction:column;
      transform:translateX(calc(-100% - var(--sidebar-w)));
      transition:transform .3s ease;
      position:fixed;
      left:var(--sidebar-w);
      top:0;
      bottom:0;
      z-index:30;
      box-shadow:10px 0 30px rgba(0,0,0,.45);
    }
    #atom-panel.active{transform:translateX(0)}
    .atom-header{padding:20px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:12px}
    .atom-header h3{font-size:1.02rem;color:var(--amber);font-family:'Fraunces',serif;font-weight:400}
    .close-btn{background:none;border:none;color:var(--bone-dim);font-size:1.4rem;cursor:pointer}
    .atom-tabs{display:flex;flex-wrap:wrap;background:var(--bg);padding:8px;gap:6px;border-bottom:1px solid var(--line)}
    .atom-tab{padding:6px 10px;font-size:.72rem;font-weight:600;text-transform:uppercase;border:1px solid var(--line);background:var(--card);color:var(--bone-dim);cursor:pointer;border-radius:4px;transition:.2s;font-family:'JetBrains Mono',monospace}
    .atom-tab.active{background:var(--amber);color:var(--bg);border-color:var(--amber)}
    .atom-content{padding:20px;flex:1;overflow-y:auto;line-height:1.7;font-size:.95rem;color:var(--bone-dim)}
    .atom-content h4{color:var(--amber);margin-bottom:10px;font-size:.9rem;text-transform:uppercase;letter-spacing:.05em;font-family:'JetBrains Mono',monospace}
    .atom-content p{white-space:pre-wrap}

    @media (max-width: 1200px){
      :root{--sidebar-w:320px;--drawer-w:360px}
      main{padding:28px}
    }
    @media (max-width: 980px){
      body{display:block;overflow:auto}
      aside{width:100%;min-width:0;height:auto}
      main{padding:22px}
      #atom-panel{left:0;width:100%;max-width:100%;transform:translateX(-100%)}
      .diagram-viewport{min-height:240px}
    }
  </style>
</head>
<body>
  <aside>
    <div class="brand">
      <div class="brand-kicker">Spec2viz · catálogo real</div>
      <div class="brand-title">{{BRAND_NAME}} <em>diagram viewer</em></div>
      <div class="brand-sub">{{BRAND_SUBTITLE}}</div>
    </div>

    <div class="sidebar-scroll">
      <div class="sidebar-card">
        <div class="sidebar-card-title">Controles</div>
        {{FILTERS}}
      </div>

      <div class="sidebar-sticky-actions">
        <div class="sidebar-card">
          <div class="sidebar-card-title">Marcado</div>
          <div class="sidebar-actions">
            <button id="anno-btn" class="sidebar-btn">✎ Marcar comentarios</button>
            <button id="explore-anno-btn" class="sidebar-btn">Explorar comentarios</button>
            <div style="display:flex;gap:4px">
              <button id="export-anno-btn" class="sidebar-btn ghost" style="flex:1">Exportar</button>
              <button id="import-anno-btn" class="sidebar-btn ghost" style="flex:1">Importar</button>
            </div>
            <button id="clear-anno-btn" class="sidebar-btn ghost">Borrar comentarios</button>
            <div class="sidebar-note">Activa marcar y haz click sobre cualquier elemento del diagrama para dejar comentarios persistidos en este navegador.</div>
          </div>
        </div>
      </div>

      <div class="sidebar-card">
        <div class="sidebar-card-title">Navegación</div>
        <nav>
          {{NAV}}
        </nav>
      </div>
    </div>
  </aside>

  <div id="anno-explorer-modal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:9999;align-items:center;justify-content:center;">
    <div style="background:#12121a;border:1px solid #d4a574;border-radius:8px;width:600px;max-width:90%;max-height:80vh;display:flex;flex-direction:column;box-shadow:0 18px 48px rgba(0,0,0,.45);">
      <div style="padding:16px;border-bottom:1px solid rgba(212,165,116,.2);display:flex;justify-content:space-between;align-items:center;">
        <h2 style="margin:0;font-size:16px;color:#d4a574;text-transform:uppercase;letter-spacing:0.1em;">Explorador de Comentarios</h2>
        <button id="close-explorer-btn" style="background:transparent;border:none;color:#f5f0e8;cursor:pointer;font-size:18px;">✕</button>
      </div>
      <div id="anno-explorer-list" style="padding:16px;overflow-y:auto;flex:1;display:flex;flex-direction:column;gap:12px;"></div>
    </div>
  </div>

  <main>
    <div class="catalog-header">
      <div class="catalog-kicker">Viewer global</div>
      <div class="catalog-title">{{CATALOG_TITLE}}</div>
      <div class="catalog-meta">Filtros y acordeón en el sidebar izquierdo. El panel de detalle también abre a la izquierda.</div>
    </div>
    {{SECTIONS}}
  </main>

  <div id="hover-popover">
    <div class="title" id="popover-title">Node Title</div>
    <div class="badges" id="popover-badges"></div>
    <div class="snippet" id="popover-snippet">Pasa el mouse o haz clic para ver la KB.</div>
  </div>

  <div id="atom-panel">
    <div class="atom-header">
      <h3 id="atom-node-title">Atom Detail</h3>
      <button class="close-btn" onclick="closeAtomPanel()">&times;</button>
    </div>
    <div class="atom-tabs" id="atom-tabs"></div>
    <div class="atom-content" id="atom-content">
      <p>Haz clic en un nodo de diagrama para explorar su Knowledge Base de 5WH1+.</p>
    </div>
  </div>

  <script>
    function initMermaid() {
    mermaid.initialize({
      startOnLoad: false,
      layout: 'elk',
      securityLevel: 'loose',
      theme: 'dark',
      themeVariables: {
        primaryColor: '#12121a', primaryBorderColor: '#d4a574', primaryTextColor: '#f5f0e8', lineColor: '#d4a574',
        secondaryColor: '#0a0a0f', tertiaryColor: '#12121a', fontFamily: 'Manrope, sans-serif',
        clusterBkg: 'rgba(212,165,116,0.05)', clusterBorder: 'rgba(212,165,116,0.25)', edgeLabelBackground: '#0a0a0f',
        actorBkg: '#12121a', actorBorder: '#d4a574', actorTextColor: '#f5f0e8', signalColor: '#d4a574', signalTextColor: '#f5f0e8',
        noteBkgColor: 'rgba(212,165,116,0.12)', noteBorderColor: '#d4a574', noteTextColor: '#f5f0e8'
      },
      flowchart: { htmlLabels: true, curve: 'linear', subGraphTitleMargin: { top: 0, bottom: 32 } }
    });
    }
    window.SPEC2VIZ_CATALOG = {{CATALOG_METADATA}};

    const popover = document.getElementById('hover-popover');
    const popoverTitle = document.getElementById('popover-title');
    const popoverBadges = document.getElementById('popover-badges');
    const popoverSnippet = document.getElementById('popover-snippet');
    const annoBtn = document.getElementById('anno-btn');
    const clearAnnoBtn = document.getElementById('clear-anno-btn');
    const ANNO_SEL = '.mermaid .node, .mermaid g.classGroup, .mermaid g.stateGroup, .mermaid rect.actor, .mermaid g.actor, .mermaid .messageText, .mermaid .noteText, .mermaid g.cluster';
    const ANNO_STORE_KEY = 'spec2viz.catalog.annotations.v1';
    let annoMode = false;
    let annoCache = [];

    function closeAtomPanel() {
      document.getElementById('atom-panel').classList.remove('active');
    }

    function norm(str) {
      return str ? str.trim().toLowerCase().replace(/\s+/g, ' ') : '';
    }

    function applyBoardTransform(board) {
      const canvas = board.querySelector('.diagram-canvas');
      if (!canvas) return;
      const scale = Number(board.dataset.zoomScale || '1');
      const x = Number(board.dataset.panX || '0');
      const y = Number(board.dataset.panY || '0');
      canvas.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
    }

    function adjustBoardZoom(board, delta) {
      const current = Number(board.dataset.zoomScale || '1');
      const next = Math.min(4, Math.max(0.6, Math.round((current + delta) * 100) / 100));
      board.dataset.zoomScale = String(next);
      applyBoardTransform(board);
    }

    function resetBoardTransform(board) {
      board.dataset.zoomScale = '1';
      board.dataset.panX = '0';
      board.dataset.panY = '0';
      applyBoardTransform(board);
    }

    function enableBoardPan(board, viewport) {
      let dragging = false;
      let startX = 0;
      let startY = 0;
      let originX = 0;
      let originY = 0;

      viewport.addEventListener('mousedown', (e) => {
        if (e.target.closest('.board-btn, .atom-tab, .tag-chip, button, a, input, select, textarea')) return;
        dragging = true;
        viewport.classList.add('dragging');
        startX = e.clientX;
        startY = e.clientY;
        originX = Number(board.dataset.panX || '0');
        originY = Number(board.dataset.panY || '0');
      });

      window.addEventListener('mousemove', (e) => {
        if (!dragging) return;
        board.dataset.panX = String(originX + (e.clientX - startX));
        board.dataset.panY = String(originY + (e.clientY - startY));
        applyBoardTransform(board);
      });

      window.addEventListener('mouseup', () => {
        dragging = false;
        viewport.classList.remove('dragging');
      });

      viewport.addEventListener('wheel', (e) => {
        if (!e.ctrlKey && !document.fullscreenElement) return;
        e.preventDefault();
        adjustBoardZoom(board, e.deltaY < 0 ? 0.15 : -0.15);
      }, { passive: false });
    }

    function bindBoards() {
      document.querySelectorAll('.board').forEach(board => {
        if (!board.querySelector('.diagram-viewport')) {
          const viewport = document.createElement('div');
          viewport.className = 'diagram-viewport';
          const canvas = document.createElement('div');
          canvas.className = 'diagram-canvas';
          Array.from(board.childNodes).forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE && node.classList?.contains('board-controls')) return;
            canvas.appendChild(node);
          });
          viewport.appendChild(canvas);
          board.appendChild(viewport);
          board.dataset.zoomScale = board.dataset.zoomScale || '1';
          board.dataset.panX = board.dataset.panX || '0';
          board.dataset.panY = board.dataset.panY || '0';
          enableBoardPan(board, viewport);
          applyBoardTransform(board);
        }

        if (board.querySelector('.board-controls')) return;
        const controls = document.createElement('div');
        controls.className = 'board-controls';
        controls.innerHTML = `
          <button class="board-btn" data-act="zoom-out" title="Alejar">−</button>
          <button class="board-btn" data-act="zoom-in" title="Acercar">+</button>
          <button class="board-btn" data-act="reset" title="Reset">⟲</button>
          <button class="board-btn" data-act="fullscreen" title="Pantalla completa">⛶</button>
        `;
        controls.addEventListener('click', (e) => {
          const btn = e.target.closest('.board-btn');
          if (!btn) return;
          const act = btn.dataset.act;
          if (act === 'zoom-in') adjustBoardZoom(board, 0.15);
          if (act === 'zoom-out') adjustBoardZoom(board, -0.15);
          if (act === 'reset') resetBoardTransform(board);
          if (act === 'fullscreen') {
            if (!document.fullscreenElement) board.requestFullscreen();
            else document.exitFullscreen();
          }
        });
        board.appendChild(controls);
      });
    }

    function buildNavAccordion() {
      document.querySelectorAll('nav .nav-category').forEach((group, index) => {
        if (group.dataset.accordionReady === 'true') return;
        const label = group.querySelector('span')?.textContent?.trim() || 'Grupo';
        const links = Array.from(group.querySelectorAll('a'));
        group.innerHTML = '';
        const head = document.createElement('button');
        head.type = 'button';
        head.className = 'nav-category-head';
        head.innerHTML = `<span class="nav-category-label">${label}</span><span class="nav-category-arrow">▾</span>`;
        const wrap = document.createElement('div');
        wrap.className = 'nav-links';
        links.forEach(link => wrap.appendChild(link));
        if (index !== 0) group.classList.add('collapsed');
        head.addEventListener('click', () => group.classList.toggle('collapsed'));
        group.appendChild(head);
        group.appendChild(wrap);
        group.dataset.accordionReady = 'true';
      });
    }

    function getViewAtomsDb(nodeEl) {
      const viewKey = nodeEl?.closest('section')?.id;
      if (viewKey && window.ATOMS_BY_VIEW?.[viewKey]) return window.ATOMS_BY_VIEW[viewKey];
      return window.ATOMS_DB || {};
    }

    // <atom-match>
    const ATOM_MATCH_MIN_SCORE = 40;

    function normKey(str) {
      return norm(str).replace(/[^\p{L}\p{N}\s]+/gu, ' ').replace(/\s+/g, ' ').trim();
    }

    function tokenSet(str) {
      return new Set(normKey(str).split(/\s+/).filter(t => t && t.length >= 3));
    }

    // Puntaje de parecido nodo<->atomo. Un solo token compartido NO basta (daba falsos positivos
    // con cientos de atomos): se exige titulo/alias exacto, frase contenida (>=2 palabras) o
    // >=2 tokens compartidos que cubran >=60% del lado mas corto.
    function matchScore(cleanText, atomEntry) {
      let best = 0;
      const text = normKey(cleanText);
      if (!text) return 0;
      const aliases = [atomEntry?.title || '', ...(atomEntry?.aliases || [])];
      const textTokens = tokenSet(text);
      for (const alias of aliases) {
        const cleanAlias = normKey(alias);
        if (!cleanAlias) continue;
        if (text === cleanAlias) { best = Math.max(best, 100); continue; }
        const textWords = text.split(' ').length;
        const aliasWords = cleanAlias.split(' ').length;
        if (aliasWords >= 2 && (' ' + text + ' ').includes(' ' + cleanAlias + ' ')) best = Math.max(best, 80);
        else if (textWords >= 2 && (' ' + cleanAlias + ' ').includes(' ' + text + ' ')) best = Math.max(best, 80);
        const aliasTokens = tokenSet(cleanAlias);
        let overlap = 0;
        aliasTokens.forEach(tok => { if (textTokens.has(tok)) overlap += 1; });
        const smaller = Math.min(aliasTokens.size, textTokens.size);
        if (overlap >= 2 && smaller > 0 && overlap / smaller >= 0.6) best = Math.max(best, 40 + overlap);
      }
      return best;
    }

    // <atom-md>
    function escapeHtml(str) {
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // Busca un atomo por id: vinculados (un nivel desde los explicitos), explicitos de la vista y payload difuso.
    function lookupAtomById(id, nodeEl) {
      if (window.ATOMS_LINKED && window.ATOMS_LINKED[id]) return window.ATOMS_LINKED[id];
      const viewKey = nodeEl?.closest?.('section')?.id;
      const explicit = (viewKey && window.ATOMS_EXPLICIT?.[viewKey]) || {};
      for (const e of Object.values(explicit)) {
        const hit = (e.list || []).find(a => a.id === id);
        if (hit) return hit;
      }
      const db = (typeof getViewAtomsDb === 'function' ? getViewAtomsDb(nodeEl) : null) || {};
      for (const entry of Object.values(db)) {
        for (const [question, a] of Object.entries(entry.atoms || {})) {
          if (a.id === id) return { id, title: entry.title, question, body: a.body };
        }
      }
      return null;
    }

    // Markdown minimo y seguro: se escapa el HTML primero y solo se generan etiquetas conocidas.
    function renderAtomBody(body, lookup) {
      const find = lookup || (() => null);
      const stash = [];
      const keep = (html) => { stash.push(html); return '\u0000' + (stash.length - 1) + '\u0000'; };
      const atomLink = (id, label) => {
        const atom = find(id);
        if (!atom) return keep(`<span class="atom-link-missing" style="opacity:.55" title="${id}">${id}</span>`);
        return keep(`<a href="#" class="atom-link" data-atom-id="${id}">${label || escapeHtml(atom.title || id)}</a>`);
      };
      const inline = (text) => {
        let t = escapeHtml(text);
        t = t.replace(/`([^`]+)`/g, (_, c) => keep(`<code>${c}</code>`));
        t = t.replace(/\[([^\[\]:]+?)::\s*\[\[([^\[\]]+?)\]\]\s*\]/g, (_, pred, id) => keep(`<em>${pred.trim()}</em>: `) + atomLink(id.trim()));
        t = t.replace(/\[\[([^\[\]]+?)\]\]/g, (_, id) => atomLink(id.trim()));
        t = t.replace(/\[([^\]]+)\]\(((?:https?:\/\/|mailto:|#|\/)[^\s)]*)\)/g,
          (_, label, url) => keep(`<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`));
        t = t.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        t = t.replace(/(^|[^*])\*([^*\s][^*]*?)\*(?!\*)/g, '$1<em>$2</em>');
        return t;
      };
      const blocks = String(body == null ? '' : body).replace(/\r\n/g, '\n').trim().split(/\n{2,}/);
      const out = blocks.map(block => {
        const lines = block.split('\n');
        if (lines.every(l => /^\s*[-*]\s+/.test(l))) {
          return '<ul>' + lines.map(l => `<li>${inline(l.replace(/^\s*[-*]\s+/, ''))}</li>`).join('') + '</ul>';
        }
        return '<p>' + lines.map(inline).join('<br>') + '</p>';
      }).join('');
      let html = out;
      for (let i = 0; i < 4 && /\u0000\d+\u0000/.test(html); i++) {
        html = html.replace(/\u0000(\d+)\u0000/g, (_, n) => stash[Number(n)]);
      }
      return html;
    }
    function atomTabLabels(atoms, labelWithTitle) {
      return atoms.map(a => labelWithTitle ? `${a.question.replace('_', ' ')} · ${a.title}` : a.question.replace('_', ' '));
    }
    // </atom-md>

    // Vinculacion explicita (`atoms: [id]` en el spec): window.ATOMS_EXPLICIT[vista][etiqueta normalizada].
    function explicitAtomData(nodeText, nodeEl) {
      const viewKey = nodeEl?.closest('section')?.id;
      const map = viewKey && window.ATOMS_EXPLICIT?.[viewKey];
      return (map && map[normKey(nodeText)]) || null;
    }

    // Referencias explicitas (`refs: [Model:name]` en el spec): window.REFS_EXPLICIT[vista][etiqueta normalizada].
    function explicitRefs(nodeText, nodeEl) {
      const viewKey = nodeEl?.closest('section')?.id;
      const map = viewKey && window.REFS_EXPLICIT?.[viewKey];
      return (map && map[normKey(nodeText)]) || [];
    }

    // Aristas sldb de un documento (refs o atomos): [{relation, direction, node, ref, title}].
    function edgesHtml(edges) {
      if (!edges || !edges.length) return '';
      const items = edges.map(e => {
        const arrow = e.direction === 'in' ? '&larr;' : '&rarr;';
        const title = escapeHtml(e.title || e.ref || e.node);
        return `<li><span class="edge-dir">${arrow}</span><span class="meta-badge">${escapeHtml(e.relation)}</span> <strong>${title}</strong> <code>${escapeHtml(e.ref || e.node)}</code></li>`;
      }).join('');
      return `<ul class="atom-edges">${items}</ul>`;
    }

    function refsHtml(refs) {
      if (!refs || !refs.length) return '';
      const items = refs.map(r => {
        const title = escapeHtml(r.title || r.name || r.ref);
        const summary = r.summary ? `<div class="ref-summary">${escapeHtml(String(r.summary).slice(0, 160))}</div>` : '';
        return `<li><span class="meta-badge">${escapeHtml(r.model || '')}</span> <strong>${title}</strong> <code title="${escapeHtml(r.path || '')}">${escapeHtml(r.ref)}</code>${summary}${edgesHtml(r.edges)}</li>`;
      }).join('');
      return `<div class="atom-refs"><h4>Referencias sldb</h4><ul>${items}</ul></div>`;
    }

    // Lista plana de atomos de una entrada: explicita (todos) o por coincidencia difusa (por pregunta).
    function atomList(data) {
      if (!data) return [];
      if (data.explicit) return data.list || [];
      const questions = ['what', 'why', 'how', 'how_not', 'when', 'where', 'for_whom'];
      return questions.filter(q => data.atoms && data.atoms[q]).map(q => ({
        id: data.atoms[q].id, title: data.title, question: q, body: data.atoms[q].body, edges: data.atoms[q].edges || [],
      }));
    }

    function findAtomData(nodeText, nodeEl) {
      const explicit = explicitAtomData(nodeText, nodeEl);
      if (explicit) return explicit;
      const atomsDb = getViewAtomsDb(nodeEl);
      if (!atomsDb) return null;
      const cleanText = norm(nodeText);
      if (atomsDb[cleanText]) return atomsDb[cleanText];
      let best = null;
      let bestScore = 0;
      for (const entry of Object.values(atomsDb)) {
        const score = matchScore(cleanText, entry);
        if (score > bestScore) {
          best = entry;
          bestScore = score;
        }
      }
      return bestScore >= ATOM_MATCH_MIN_SCORE ? best : null;
    }
    // </atom-match>

    function annoLabel(el) {
      if (el.matches('g.cluster')) {
        return el.id || (el.querySelector('.cluster-label')?.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120);
      }
      if (el.matches('.actor')) {
        const textEl = el.tagName === 'rect' ? el.parentElement.querySelector('text.actor') : el;
        if (textEl) return textEl.textContent.replace(/\s+/g, ' ').trim().slice(0, 120);
      }
      if (el.matches('.messageText, .noteText')) {
        return el.textContent.replace(/\s+/g, ' ').trim().slice(0, 120);
      }
      const t = el.querySelector('.nodeLabel, .label, foreignObject, text');
      return ((t ? (t.innerText || t.textContent) : (el.innerText || el.textContent)) || '').replace(/\s+/g, ' ').trim().slice(0, 120);
    }

    function annoVista(el) {
      return el.closest('section')?.id || 'unknown';
    }

    function annoKey(vista, label) {
      return `${vista}::${label}`;
    }

    function annoReadStore() {
      try {
        return JSON.parse(localStorage.getItem(ANNO_STORE_KEY) || '[]');
      } catch {
        return [];
      }
    }

    function annoWriteStore(items) {
      annoCache = items;
      localStorage.setItem(ANNO_STORE_KEY, JSON.stringify(items));
    }

    function annoLoad() {
      annoCache = annoReadStore();
      annoRender();
    }

    function annoClose() {
      document.getElementById('anno-popup')?.remove();
    }

    function annoRender() {
      document.querySelectorAll('.anno-marked').forEach(el => el.classList.remove('anno-marked'));
      document.querySelectorAll('.anno-pin').forEach(el => el.remove());
      annoCache.forEach(a => {
        const sec = document.getElementById(a.vista);
        if (!sec) return;
        sec.querySelectorAll(ANNO_SEL).forEach(el => {
          if (annoLabel(el) !== a.label) return;
          el.classList.add('anno-marked');
          if (!el.matches('g.node, g.classGroup, g.stateGroup, g.cluster, .actor, .messageText, .noteText')) return;
          const svg = el.ownerSVGElement || el.closest('svg');
          if (!svg || !el.getBBox) return;
          const bbox = el.getBBox();
          const warn = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          warn.textContent = '✎';
          warn.setAttribute('x', bbox.x - (el.matches('.messageText') ? 0 : 8));
          warn.setAttribute('y', bbox.y + (el.matches('.messageText') ? 0 : 10));
          warn.setAttribute('fill', '#d4a574');
          warn.setAttribute('font-size', '14');
          warn.setAttribute('class', 'anno-pin');
          svg.appendChild(warn);
        });
      });
    }

    function annoPopup(el, x, y) {
      annoClose();
      const vista = annoVista(el);
      const label = annoLabel(el);
      const prev = annoCache.filter(a => a.key === annoKey(vista, label));
      const div = document.createElement('div');
      div.className = 'anno-popup';
      div.id = 'anno-popup';
      div.style.left = Math.min(x, window.innerWidth - 340) + 'px';
      div.style.top = Math.min(y, window.innerHeight - 300) + 'px';
      div.innerHTML =
        `<div class="who">${vista} · ${label}</div>` +
        prev.map(a => `<div class="prev">${a.comentario}<span>${a.ts}</span></div>`).join('') +
        `<textarea placeholder="comentario…"></textarea>
         <div class="row">
           <button data-act="save">guardar</button>
           ${prev.length ? '<button data-act="del">borrar</button>' : ''}
           <button data-act="x">cerrar</button>
         </div>`;
      div.addEventListener('click', e => {
        const act = e.target.dataset?.act;
        if (!act) return;
        if (act === 'x') return annoClose();
        if (act === 'del') {
          annoWriteStore(annoCache.filter(a => a.key !== annoKey(vista, label)));
          annoClose();
          annoRender();
          return;
        }
        const comentario = div.querySelector('textarea').value.trim();
        if (!comentario) return;
        annoWriteStore([
          ...annoCache,
          { key: annoKey(vista, label), vista, label, comentario, ts: new Date().toISOString().slice(0, 16).replace('T', ' ') }
        ]);
        annoClose();
        annoRender();
      });
      document.body.appendChild(div);
      div.querySelector('textarea').focus();
    }

    function initAnnotations() {
      annoBtn.addEventListener('click', e => {
        e.preventDefault();
        annoMode = !annoMode;
        document.body.classList.toggle('anno-mode', annoMode);
        annoBtn.classList.toggle('active', annoMode);
        annoBtn.textContent = annoMode ? '✎ Marcando comentarios' : '✎ Marcar comentarios';
        if (!annoMode) annoClose();
      });
      clearAnnoBtn.addEventListener('click', () => {
        if(confirm('¿Borrar todos los comentarios locales?')) {
          annoWriteStore([]);
          annoClose();
          annoRender();
        }
      });

      document.getElementById('export-anno-btn').addEventListener('click', () => {
        const data = annoReadStore();
        if (data.length === 0) return alert('No hay comentarios para exportar.');
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'comentarios-arquitectura.json';
        a.click();
        URL.revokeObjectURL(url);
      });

      document.getElementById('import-anno-btn').addEventListener('click', () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/json';
        input.onchange = e => {
          const file = e.target.files[0];
          if (!file) return;
          const reader = new FileReader();
          reader.onload = ev => {
            try {
              const data = JSON.parse(ev.target.result);
              if (!Array.isArray(data)) throw new Error('Formato inválido');
              const merged = [...annoReadStore(), ...data];
              const unique = Array.from(new Map(merged.map(item => [item.key + item.ts, item])).values());
              annoWriteStore(unique);
              annoRender();
              alert('Comentarios importados correctamente.');
            } catch (err) {
              alert('Error leyendo JSON de comentarios.');
            }
          };
          reader.readAsText(file);
        };
        input.click();
      });

      const explorerModal = document.getElementById('anno-explorer-modal');
      const explorerList = document.getElementById('anno-explorer-list');
      
      document.getElementById('explore-anno-btn').addEventListener('click', () => {
        const data = annoReadStore();
        explorerList.innerHTML = '';
        if (data.length === 0) {
          explorerList.innerHTML = '<div style="color:#888;font-size:13px;text-align:center;">No hay comentarios guardados.</div>';
        } else {
          data.forEach(item => {
            const div = document.createElement('div');
            div.style = 'background:#161621;border:1px solid rgba(212,165,116,0.2);padding:12px;border-radius:6px;cursor:pointer;';
            div.innerHTML = `
              <div style="font-size:11px;color:#d4a574;margin-bottom:4px;text-transform:uppercase;">${item.vista} &nbsp;▸&nbsp; ${item.label} <span style="float:right;color:#888;">${item.ts}</span></div>
              <div style="font-size:13px;line-height:1.4;">${item.comentario.replace(/</g,'&lt;')}</div>
            `;
            div.onclick = () => {
              explorerModal.style.display = 'none';
              const target = document.getElementById(item.vista);
              if(target) {
                target.scrollIntoView({ behavior: 'smooth' });
              }
            };
            explorerList.appendChild(div);
          });
        }
        explorerModal.style.display = 'flex';
      });

      document.getElementById('close-explorer-btn').addEventListener('click', () => {
        explorerModal.style.display = 'none';
      });

      document.addEventListener('click', e => {
        if (!annoMode || e.target.closest('.anno-popup')) return;
        const el = e.target.closest(ANNO_SEL);
        if (!el) return;
        e.preventDefault();
        e.stopPropagation();
        hideHoverPopover();
        annoPopup(el, e.clientX, e.clientY);
      }, true);
      annoLoad();
    }

    function showHoverPopover(e, nodeText, nodeEl) {
      const data = findAtomData(nodeText, nodeEl);
      popoverTitle.innerText = nodeText;
      popoverBadges.innerHTML = '';

      const list = atomList(data);
      const refCount = explicitRefs(nodeText, nodeEl).length;
      if (!list.length) {
        popoverSnippet.innerText = annoMode ? 'Modo comentarios activo.'
          : refCount ? `${refCount} referencia(s) sldb.` : 'Sin átomos 5WH1+ registrados.';
      } else {
        list.forEach(a => {
          const span = document.createElement('span');
          span.className = 'badge active';
          span.innerText = a.question.replace('_', ' ');
          popoverBadges.appendChild(span);
        });
        popoverSnippet.innerText = `[${list[0].question.toUpperCase()}] ${String(list[0].body).substring(0, 100)}...`;
      }

      const left = Math.min(e.clientX + 15, window.innerWidth - 340);
      const top = Math.min(e.clientY + 15, window.innerHeight - 160);
      popover.style.left = left + 'px';
      popover.style.top = top + 'px';
      popover.style.display = 'block';
    }

    function hideHoverPopover() {
      popover.style.display = 'none';
    }

    function selectNodeAtoms(nodeTitle, nodeEl) {
      hideHoverPopover();
      const panel = document.getElementById('atom-panel');
      const titleEl = document.getElementById('atom-node-title');
      const tabsEl = document.getElementById('atom-tabs');
      const contentEl = document.getElementById('atom-content');
      const data = findAtomData(nodeTitle, nodeEl);

      const list = atomList(data);
      const refs = refsHtml(explicitRefs(nodeTitle, nodeEl));
      if (!list.length) {
        titleEl.innerText = nodeTitle;
        tabsEl.innerHTML = '';
        contentEl.innerHTML = refs || '<p>No hay átomos 5WH1+ registrados para este componente.</p>';
        panel.classList.add('active');
        return;
      }

      const lookup = id => lookupAtomById(id, nodeEl);
      const showAtoms = (atoms, labelWithTitle) => {
        tabsEl.innerHTML = '';
        let firstActive = null;
        atomTabLabels(atoms, labelWithTitle).forEach((label, i) => {
          const a = atoms[i];
          const btn = document.createElement('button');
          btn.className = 'atom-tab';
          btn.innerText = label;
          btn.onclick = () => {
            document.querySelectorAll('.atom-tab').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            contentEl.innerHTML = `<h4>5WH1+: ${escapeHtml(a.question.toUpperCase())} (${escapeHtml(a.id)})</h4>${renderAtomBody(a.body, lookup)}${edgesHtml(a.edges)}${refs}`;
          };
          tabsEl.appendChild(btn);
          if (!firstActive) firstActive = btn;
        });
        if (firstActive) firstActive.click();
      };
      titleEl.innerText = data.explicit ? nodeTitle : data.title;
      showAtoms(list, !!data.explicit);
      contentEl.onclick = (ev) => {
        const link = ev.target.closest('a[data-atom-id]');
        if (!link) return;
        ev.preventDefault();
        const target = lookup(link.dataset.atomId);
        if (!target) return;
        titleEl.innerText = target.title || target.id;
        showAtoms([target], false);  // pestanas regeneradas para el atomo destino
      };
      panel.classList.add('active');
    }

    function applyCatalogFilters() {
      const typeValue = document.querySelector('select[data-filter="tipo"]')?.value || '';
      const projectValue = document.querySelector('select[data-filter="proyecto"]')?.value || '';
      const categoryValue = document.querySelector('select[data-filter="categoría"]')?.value || '';
      const searchValue = (document.getElementById('catalog-search')?.value || '').trim().toLowerCase();
      const activeTags = Array.from(document.querySelectorAll('.tag-chip.active')).map(btn => btn.dataset.tag || '');

      document.querySelectorAll('.catalog-item').forEach(section => {
        const sectionType = section.dataset.type || '';
        const sectionProject = section.dataset.project || '';
        const sectionCategory = section.dataset.category || '';
        const sectionTags = (section.dataset.tags || '').toLowerCase();
        const sectionText = section.innerText.toLowerCase();
        const matchesType = !typeValue || sectionType === typeValue;
        const matchesProject = !projectValue || sectionProject === projectValue;
        const matchesCategory = !categoryValue || sectionCategory === categoryValue;
        const matchesSearch = !searchValue || sectionText.includes(searchValue) || sectionTags.includes(searchValue);
        const matchesTags = activeTags.length === 0 || activeTags.every(tag => sectionTags.includes(tag.toLowerCase()));
        const visible = matchesType && matchesProject && matchesCategory && matchesSearch && matchesTags;
        section.style.display = visible ? '' : 'none';
      });

      document.querySelectorAll('.category-block').forEach(block => {
        const visibleItems = Array.from(block.querySelectorAll('.catalog-item')).some(item => item.style.display !== 'none');
        block.style.display = visibleItems ? '' : 'none';
      });
    }

    function bindMermaidNodes() {
      document.querySelectorAll('.mermaid .node, .mermaid g.classGroup, .mermaid g.stateGroup, .mermaid rect.actor, .mermaid g.cluster').forEach(node => {
        if (node.dataset.catalogBound === 'true') return;
        node.dataset.catalogBound = 'true';
        node.addEventListener('mouseenter', (e) => {
          const labelEl = node.querySelector('.nodeLabel, .label, foreignObject, text') || node;
          const text = (labelEl.innerText || labelEl.textContent || '').trim();
          if (text) showHoverPopover(e, text, node);
        });
        node.addEventListener('mouseleave', hideHoverPopover);
        node.addEventListener('click', () => {
          const labelEl = node.querySelector('.nodeLabel, .label, foreignObject, text') || node;
          const text = (labelEl.innerText || labelEl.textContent || '').trim();
          if (!text || annoMode) return;
          selectNodeAtoms(text, node);
        });
      });
    }

    function highlightActiveNav() {
      const links = Array.from(document.querySelectorAll('.nav-links a'));
      const sections = links.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          links.forEach(link => link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`));
        });
      }, { root: document.querySelector('main'), threshold: .28 });
      sections.forEach(section => observer.observe(section));
    }

    function calculateCoverage() {
      let totalNodes = 0;
      let totalMatched = 0;
      
      document.querySelectorAll('section.catalog-item').forEach(section => {
        const board = section.querySelector('.board');
        if (!board) return;
        const nodes = Array.from(board.querySelectorAll('.mermaid .node, .mermaid g.classGroup, .mermaid g.stateGroup, .mermaid rect.actor, .mermaid g.cluster'));
        if (nodes.length === 0) return;
        
        let sectionNodes = 0;
        let matched = 0;
        nodes.forEach(node => {
          const labelEl = node.querySelector('.nodeLabel, .label, foreignObject, text') || node;
          const text = (labelEl.innerText || labelEl.textContent || '').trim();
          if (!text) return;
          sectionNodes++;
          if (findAtomData(text, node)) matched++;
        });
        
        if (sectionNodes === 0) return;
        totalNodes += sectionNodes;
        totalMatched += matched;
        
        const pct = Math.round((matched / sectionNodes) * 100);
        const metaDiv = section.querySelector('.section-meta');
        if (metaDiv) {
          const badge = document.createElement('span');
          badge.className = 'meta-badge coverage';
          badge.style.marginLeft = 'auto';
          badge.style.border = '1px solid currentColor';
          badge.style.background = 'rgba(0,0,0,0.2)';
          badge.style.fontWeight = '500';
          
          if (pct === 100) badge.style.color = '#4ade80';
          else if (pct >= 50) badge.style.color = 'var(--amber)';
          else badge.style.color = '#f87171';
          
          badge.textContent = `Atoms: ${pct}%`;
          badge.title = `${matched} de ${sectionNodes} elementos documentados`;
          metaDiv.appendChild(badge);
        }
      });
      
      const sidebarScroll = document.querySelector('.sidebar-scroll');
      if (sidebarScroll && totalNodes > 0) {
        const globalPct = Math.round((totalMatched / totalNodes) * 100);
        const color = globalPct === 100 ? '#4ade80' : globalPct >= 50 ? 'var(--amber)' : '#f87171';
        const html = `
        <div class="sidebar-card" style="margin-top: 14px;">
          <div class="sidebar-card-title">Atom Coverage</div>
          <div style="font-size: 24px; font-weight: 300; font-family: 'JetBrains Mono', monospace; margin: 8px 0; color: ${color};">
            ${globalPct}%
          </div>
          <div class="sidebar-note">${totalMatched} de ${totalNodes} elementos del catálogo tienen su conocimiento 5WH1+ documentado en desk/atoms.</div>
        </div>`;
        sidebarScroll.insertAdjacentHTML('beforeend', html);
      }
    }

    function initSidebarAccordions() {
      document.querySelectorAll('.sidebar-card-title').forEach(title => {
        title.addEventListener('click', () => {
          title.parentElement.classList.toggle('collapsed');
        });
      });
    }

    // Vega boards (matrix views): the libraries load only when the catalog has one.
    function loadScript(src) {
      return new Promise((resolve, reject) => {
        const el = document.createElement('script');
        el.src = src; el.onload = resolve; el.onerror = () => reject(new Error('failed to load ' + src));
        document.head.appendChild(el);
      });
    }
    async function renderVegaBoards() {
      const boards = Array.from(document.querySelectorAll('.vega-board'));
      if (!boards.length) return;
      try {
        if (!window.vegaEmbed) {
          await loadScript('https://cdn.jsdelivr.net/npm/vega@5');
          await loadScript('https://cdn.jsdelivr.net/npm/vega-lite@5');
          await loadScript('https://cdn.jsdelivr.net/npm/vega-embed@6');
        }
        for (const board of boards) {
          const specEl = board.querySelector('script.vega-spec');
          if (!specEl) continue;
          const host = document.createElement('div');
          host.className = 'vega-host';
          board.appendChild(host);
          await window.vegaEmbed(host, JSON.parse(specEl.textContent), { actions: false });
        }
      } catch (err) {
        console.warn('vega boards not rendered:', err);
      }
    }

    document.addEventListener('DOMContentLoaded', async () => {
      initSidebarAccordions();
      buildNavAccordion();
      initAnnotations();
      document.querySelectorAll('.catalog-toolbar select, #catalog-search').forEach(el => {
        el.addEventListener('input', applyCatalogFilters);
        el.addEventListener('change', applyCatalogFilters);
      });
      document.querySelectorAll('.tag-chip').forEach(btn => {
        btn.addEventListener('click', () => {
          btn.classList.toggle('active');
          applyCatalogFilters();
        });
      });
      await renderVegaBoards();
      initMermaid();
      await mermaid.run({ querySelector: '.mermaid' });
      bindBoards();
      bindMermaidNodes();
      highlightActiveNav();
      applyCatalogFilters();
      calculateCoverage();
    });
  </script>
</body>
</html>

FILE:src/specir/visual/templates/vendor/bpmn-js/LICENSE
Copyright (c) 2014-present Camunda Services GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

The source code responsible for displaying the bpmn.io project watermark that
links back to https://bpmn.io as part of rendered diagrams MUST NOT be
removed or changed. When this software is being used in a website or application,
the watermark must stay fully visible and not visually overlapped by other elements.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

FILE:src/specir/visual/templates/vendor/bpmn-js/README.md
# Vendored bpmn-js

- Package: `bpmn-js` 18.31.1 (npm), the latest stable release on 2026-10-22
- Source: https://registry.npmjs.org/bpmn-js/-/bpmn-js-18.31.1.tgz
  (integrity `sha512-Hc7LzrgwfcBRUAdI/380Q2v1MJ115atGEVGadawLfDbHdo+r+IkmNj8fuYPFmWglUYt1KYIaC46OeX16HGTKQw==`,
  checked before extracting; no package scripts were run)
- Project: https://github.com/bpmn-io/bpmn-js, https://bpmn.io
- License: the bpmn.io license, copied verbatim in `LICENSE` (MIT-style, plus: the bpmn.io watermark that links
  back to https://bpmn.io must not be removed, changed or visually overlapped)

Files copied unchanged from the package's `dist/`:

| file | from |
| --- | --- |
| `bpmn-navigated-viewer.production.min.js` | `dist/bpmn-navigated-viewer.production.min.js` |
| `diagram-js.css` | `dist/assets/diagram-js.css` |
| `bpmn-js.css` | `dist/assets/bpmn-js.css` |
| `LICENSE` | `LICENSE` |

The `bpmn-font` icon font of `dist/assets/` is not vendored: it only draws the modeler's palette and context
pad, which the NavigatedViewer does not have. `spec2viz.renderers.bpmn.render_bpmn_html` inlines these files
into every `.bpmn.html`, so the page works offline from `file://`.

To upgrade: download the new tarball into an empty temp dir, verify its integrity against `npm view bpmn-js
dist.integrity`, extract it without running anything, copy the same four files and update this README.

FILE:src/specir/visual/templates/vendor/bpmn-js/bpmn-js.css
/**
 * Semantic tokens, copied from `@bpmn-io/theme` to style the components
 * according to this theme.
 *
 * Names and values of the tokens should stay intact with the `@bpmn-io/theme`
 * source of truth, to ensure matching styles and allow overrides with an
 * alternative theme.
 */
.bio-theme-parent {
  --bio-surface-subtle: hsl(225, 10%, 97%);
  --bio-text-on-primary: hsl(0, 0%, 100%);
  --bio-border: hsl(225, 10%, 75%);
  --bio-primary: hsl(205, 100%, 40%);
  --bio-focus: hsl(205, 100%, 40%);
  --bio-radius-md: 3px;
  --bio-radius-lg: 4px;
}

.bjs-container {
  --bjs-font-family: Arial, sans-serif;

  --accent-color: var(--bio-primary);

  --breadcrumbs-font-family: var(--bjs-font-family);
  --breadcrumbs-item-color: var(--accent-color);
  --breadcrumbs-background-color: var(--bio-surface-subtle);
  --breadcrumbs-border-color: var(--bio-border);
  --breadcrumbs-focus-outline-color: var(--bio-focus);
  --drilldown-fill-color: var(--bio-text-on-primary);
  --drilldown-background-color: var(--accent-color);
  --drilldown-focus-outline-color: var(--bio-focus);

  --button-border-radius: var(--bio-radius-md);
  --surface-border-radius: var(--bio-radius-lg);
}

.bjs-breadcrumbs {
  position: absolute;
  display: none;
  flex-wrap: wrap;
  align-items: center;
  top: 20px;
  left: 20px;
  padding: 5px 10px;
  margin: 0px;
  font-family: var(--breadcrumbs-font-family);
  font-size: 16px;
  line-height: normal;
  background-color: var(--breadcrumbs-background-color);
  border: solid 1px var(--breadcrumbs-border-color);
  border-radius: var(--surface-border-radius);
  row-gap: 5px;
}

.bjs-breadcrumbs-shown .bjs-breadcrumbs {
  display: flex;
}

.djs-palette-shown .bjs-breadcrumbs {
  left: 90px;
}

.djs-palette-shown.djs-palette-two-column .bjs-breadcrumbs {
  left: 140px;
}

.bjs-breadcrumbs li {
  display: inline-flex;
  align-items: center;
}

.bjs-breadcrumbs a.bjs-crumb {
  cursor: pointer;
  color: var(--breadcrumbs-item-color);
  text-decoration: none;
}

.bjs-breadcrumbs a.bjs-crumb:focus-visible {
  outline: solid 1px var(--breadcrumbs-focus-outline-color);
  outline-offset: 1px;
}

.bjs-breadcrumbs li:not(:first-child)::before {
  content: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" /><path d="M0 0h24v24H0z" fill="none" /></svg>');
  padding: 0 8px;
  height: 1em;
}

.bjs-breadcrumbs .bjs-crumb {
  display: inline-block;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bjs-drilldown {
  width: 20px;
  height: 20px;

  padding: 0px;
  margin-left: -20px;

  cursor: pointer;
  border: none;
  border-radius: var(--button-border-radius);

  fill: var(--drilldown-fill-color);
  background-color: var(--drilldown-background-color);
}

.bjs-drilldown:focus-visible {
  outline: solid 1px var(--drilldown-focus-outline-color);
  outline-offset: 1px;
}

.bjs-drilldown-empty {
  display: none;
}

.selected .bjs-drilldown-empty {
  display: inherit;
}

[data-popup="align-elements"] .djs-popup-results {
  display: flex;
}

[data-popup="align-elements"] .djs-popup-body [data-group] + [data-group] {
  border-left: 1px solid var(--popup-border-color);
}

[data-popup="align-elements"] [data-group="align"] {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

[data-popup="align-elements"] .djs-popup-body .entry {
  padding: 6px 8px;
}

[data-popup="align-elements"] .djs-popup-body .entry:not(:first-child) {
  margin-top: 0;
}

[data-popup="align-elements"] .djs-popup-entry-icon {
  display: block;
  margin: 0;
  height: 20px;
  width: 20px;
}

FILE:src/specir/visual/templates/vendor/bpmn-js/diagram-js.css
/**
 * Semantic tokens, copied from `@bpmn-io/theme` to style the components
 * according to this theme.
 *
 * Names and values of the tokens should stay intact with the `@bpmn-io/theme`
 * source of truth, to ensure matching styles and allow overrides with an
 * alternative theme.
 */
.bio-theme-parent {
  --bio-surface: hsl(0, 0%, 100%);
  --bio-surface-overlay: hsl(0, 0%, 100%);
  --bio-surface-subtle: hsl(225, 10%, 97%);
  --bio-surface-medium: hsl(225, 10%, 95%);
  --bio-surface-inverted: hsl(0, 0%, 22%);
  --bio-surface-inverted-subtle: hsl(225, 10%, 35%);
  --bio-text: hsl(225, 10%, 15%);
  --bio-text-subtle: hsl(225, 10%, 35%);
  --bio-text-subtlest: hsl(225, 10%, 55%);
  --bio-text-on-inverted: hsl(0, 0%, 100%);
  --bio-border: hsl(225, 10%, 75%);
  --bio-border-disabled: hsl(225, 10%, 90%);
  --bio-primary: hsl(205, 100%, 40%);
  --bio-primary-surface: hsl(205, 100%, 95%);
  --bio-danger: hsl(360, 100%, 45%);
  --bio-danger-surface-subtle: hsl(360, 100%, 97%);
  --bio-selected-surface: var(--bio-surface-medium);
  --bio-selected-text: var(--bio-text);
  --bio-focus: hsl(205, 100%, 40%);
  --bio-focus-surface: hsl(205, 100%, 95%);
  --bio-canvas-accent: hsl(205, 100%, 40%);
  --bio-canvas-accent-subtle: hsl(205, 100%, 75%);
  --bio-shadow: hsla(0, 0%, 0%, 30%);
  --bio-shadow-subtle: hsla(0, 0%, 0%, 10%);
  --bio-radius-sm: 2px;
  --bio-radius-md: 3px;
  --bio-radius-lg: 4px;
}

/**
 * color definitions
 *
 * Colours resolve through the semantic tokens in `@bpmn-io/theme`; a handful of
 * values with no matching token stay literal.
 */
.djs-parent {

  --button-border-radius: var(--bio-radius-md);
  --input-border-radius: var(--bio-radius-sm);
  --surface-border-radius: var(--bio-radius-lg);

  --canvas-fill-color: var(--bio-surface);

  --accent-color: var(--bio-canvas-accent);

  --bendpoint-fill-color: var(--bio-canvas-accent);
  --bendpoint-stroke-color: var(--canvas-fill-color);

  --context-pad-entry-background-color: var(--bio-surface);
  --context-pad-entry-hover-background-color: var(--bio-surface-medium);

  --element-dragger-color: var(--accent-color);
  --element-selected-outline-stroke-color: var(--accent-color);
  --element-selected-outline-secondary-stroke-color: var(--bio-canvas-accent-subtle);

  --lasso-fill-color: color-mix(in srgb, var(--bio-canvas-accent) 15%, transparent);
  --lasso-stroke-color: var(--element-selected-outline-stroke-color);

  --palette-entry-color: var(--bio-text);
  --palette-entry-hover-color: var(--bio-primary);
  --palette-entry-selected-color: var(--bio-primary);
  --palette-separator-color: var(--bio-border);
  --palette-toggle-hover-background-color: var(--bio-surface-medium);
  --palette-background-color: var(--bio-surface-subtle);
  --palette-border-color: var(--bio-border);

  --popup-font-family: "IBM Plex Sans", sans-serif;
  --popup-font-size: 14px;
  --popup-secondary-font-size: .9em;
  --popup-header-entry-selected-color: var(--bio-primary);
  --popup-header-font-weight: bolder;
  --popup-header-group-divider-color: var(--bio-border);
  --popup-background-color: var(--bio-surface-overlay);
  --popup-border-color: transparent;
  --popup-shadow-color: var(--bio-shadow);
  /* translucent, so the thumb darkens whatever it scrolls over */
  --popup-scrollbar-thumb-color: rgba(0, 0, 0, 0.2);
  --popup-button-background-color: var(--bio-surface-overlay);
  --popup-button-hover-background-color: var(--bio-surface-medium);
  --popup-disabled-color: var(--bio-text-subtle);
  --popup-description-color: var(--bio-text-subtle);
  --popup-no-results-color: var(--bio-text-subtlest);
  --popup-entry-title-color: var(--bio-text-subtlest);

  --popup-entry-selected-background-color: var(--bio-selected-surface);
  --popup-entry-selected-color: var(--bio-selected-text);
  --popup-search-border-color: var(--bio-border);
  --popup-search-focus-border-color: var(--bio-focus);
  --popup-search-focus-background-color: var(--bio-focus-surface);
  --popup-tab-color: var(--bio-text-subtlest);
  --popup-tab-hover-color: var(--bio-text);
  --popup-tab-active-color: var(--bio-text);
  --popup-tab-active-border-color: var(--bio-primary);
  --popup-tab-strip-border-color: var(--bio-border-disabled);
  --popup-tab-focus-border-color: var(--bio-focus);

  --resizer-fill-color: var(--bio-canvas-accent);
  --resizer-stroke-color: var(--canvas-fill-color);

  --search-font-family: "IBM Plex Sans", sans-serif;
  --search-font-size: 14px;
  --search-container-background-color: var(--bio-surface-overlay);
  --search-shadow-color: var(--bio-shadow);
  --search-input-border-color: var(--bio-border);
  --search-input-focus-border-color: var(--bio-focus);
  --search-input-focus-background-color: var(--bio-primary-surface);
  --search-result-hover-background-color: var(--bio-surface-medium);
  --search-result-secondary-color: var(--bio-text-subtlest);
  --search-preselected-background-color: color-mix(in srgb, var(--bio-canvas-accent) 15%, transparent);

  --shape-attach-allowed-stroke-color: var(--accent-color);
  --shape-connect-allowed-fill-color: var(--bio-surface-subtle);
  --shape-drop-allowed-fill-color: var(--bio-surface-subtle);
  --shape-drop-not-allowed-fill-color: var(--bio-danger-surface-subtle);
  --shape-resize-preview-stroke-color: var(--accent-color);

  --snap-line-stroke-color: color-mix(in srgb, var(--bio-canvas-accent) 30%, transparent);

  --space-tool-crosshair-stroke-color: var(--bio-text);

  --tooltip-error-background-color: var(--bio-danger-surface-subtle);
  --tooltip-error-border-color: var(--bio-danger);
  --tooltip-error-color: var(--bio-danger);

  --hover-tooltip-font-family: "IBM Plex Sans", sans-serif;
  --hover-tooltip-font-size: 12px;
  --hover-tooltip-secondary-font-size: 11px;
  --hover-tooltip-background-color: var(--bio-surface-inverted);
  --hover-tooltip-color: var(--bio-text-on-inverted);
  --hover-tooltip-shadow-color: var(--bio-shadow-subtle);

  --palette-tooltip-shortcut-background-color: var(--bio-surface-inverted-subtle);
}

/**
 * SVG styles
 */

.djs-container svg.drop-not-ok {
  background: var(--shape-drop-not-allowed-fill-color) !important;
}

.djs-container svg.new-parent {
  background: var(--shape-drop-allowed-fill-color) !important;
}

.djs-container svg:focus {
  outline-offset: -1px;
}

/**
 * outline styles
 */

.djs-outline,
.djs-selection-outline {
  fill: none;
  shape-rendering: geometricPrecision;
  stroke-width: 2px;
}

.djs-outline {
  visibility: hidden;
}

.djs-selection-outline {
  stroke: var(--element-selected-outline-stroke-color);
}

.djs-element.selected .djs-outline {
  visibility: visible;

  stroke: var(--element-selected-outline-stroke-color);
}

.djs-connection.selected .djs-outline {
  display: none;
}

.djs-multi-select .djs-element.selected .djs-outline,
.djs-dragging-active-lasso .djs-element.selected .djs-outline {
  stroke: var(--element-selected-outline-secondary-stroke-color);
  display: block;
}

.djs-outline-hidden .djs-outline {
  display: none !important;
}

.djs-shape.connect-ok .djs-visual > :nth-child(1) {
  fill: var(--shape-connect-allowed-fill-color) !important;
}

.djs-shape.connect-not-ok .djs-visual > :nth-child(1),
.djs-shape.drop-not-ok .djs-visual > :nth-child(1) {
  fill: var(--shape-drop-not-allowed-fill-color) !important;
}

.djs-shape.new-parent .djs-visual > :nth-child(1) {
  fill: var(--shape-drop-allowed-fill-color) !important;
}


/* Override move cursor during drop and connect */
.drop-not-ok,
.connect-not-ok,
.drop-not-ok *,
.connect-not-ok * {
  cursor: not-allowed !important;
}

.drop-ok,
.connect-ok,
.drop-ok *,
.connect-ok * {
  cursor: default !important;
}

.djs-element.attach-ok .djs-visual > :nth-child(1) {
  stroke-width: 5px !important;
  stroke: var(--shape-attach-allowed-stroke-color) !important;
}

.djs-frame.connect-not-ok .djs-visual > :nth-child(1),
.djs-frame.drop-not-ok .djs-visual > :nth-child(1) {
  stroke-width: 3px !important;
  stroke: var(--shape-drop-not-allowed-fill-color) !important;
  fill: none !important;
}

/**
* Selection box style
*
*/
.djs-lasso-overlay {
  fill: var(--lasso-fill-color);
  stroke: var(--lasso-stroke-color);
  stroke-width: 2px;
  shape-rendering: geometricPrecision;
  pointer-events: none;
}

/**
 * Resize styles
 */
.djs-resize-overlay {
  fill: none;

  stroke-dasharray: 5 1 3 1;
  stroke: var(--shape-resize-preview-stroke-color);

  pointer-events: none;
}

.djs-resizer-hit {
  fill: none;
  pointer-events: all;
}

.djs-resizer-visual {
  fill: var(--resizer-fill-color);
  stroke-width: 1px;
  stroke: var(--resizer-stroke-color);
  shape-rendering: geometricPrecision;
}

.djs-resizer:hover .djs-resizer-visual {
  stroke: var(--resizer-stroke-color);
  stroke-opacity: 1;
}

.djs-cursor-resize-ns,
.djs-resizer-n,
.djs-resizer-s {
  cursor: ns-resize;
}

.djs-cursor-resize-ew,
.djs-resizer-e,
.djs-resizer-w {
  cursor: ew-resize;
}

.djs-cursor-resize-nwse,
.djs-resizer-nw,
.djs-resizer-se {
  cursor: nwse-resize;
}

.djs-cursor-resize-nesw,
.djs-resizer-ne,
.djs-resizer-sw {
  cursor: nesw-resize;
}

.djs-shape.djs-resizing > .djs-outline {
  visibility: hidden !important;
}

.djs-shape.djs-resizing > .djs-resizer {
  visibility: hidden;
}

.djs-dragger > .djs-resizer {
  visibility: hidden;
}

/**
 * drag styles
 */
.djs-dragger * {
  fill: none !important;
  stroke: var(--element-dragger-color) !important;
}

.djs-dragger tspan,
.djs-dragger text {
  fill: var(--element-dragger-color) !important;
  stroke: none !important;
}

.djs-dragger marker circle,
.djs-dragger marker path,
.djs-dragger marker polygon,
.djs-dragger marker polyline,
.djs-dragger marker rect {
  fill: var(--element-dragger-color) !important;
  stroke: none !important;
}

.djs-dragger marker text,
.djs-dragger marker tspan {
  fill: none !important;
  stroke: var(--element-dragger-color) !important;
}

.djs-dragging,
.djs-dragging > * {
  opacity: 0.3 !important;
  pointer-events: none !important;
}

/**
 * no pointer events for visual
 */
.djs-visual,
.djs-outline {
  pointer-events: none;
}

.djs-element.attach-ok .djs-hit {
  stroke-width: 60px !important;
}

/**
 * all pointer events for hit shape
 */
.djs-element > .djs-hit-all,
.djs-element > .djs-hit-no-move {
  pointer-events: all;
}

.djs-element > .djs-hit-stroke,
.djs-element > .djs-hit-click-stroke {
  pointer-events: stroke;
}

/**
 * shape / connection basic styles
 */
.djs-connection .djs-visual {
  stroke-width: 2px;
  fill: none;
}

.djs-cursor-grab {
  cursor: -webkit-grab;
  cursor: -moz-grab;
  cursor: grab;
}

.djs-cursor-grabbing {
  cursor: -webkit-grabbing;
  cursor: -moz-grabbing;
  cursor: grabbing;
}

.djs-cursor-crosshair {
  cursor: crosshair;
}

.djs-cursor-move {
  cursor: move;
}

.djs-cursor-resize-ns {
  cursor: ns-resize;
}

.djs-cursor-resize-ew {
  cursor: ew-resize;
}


/**
 * snapping
 */
.djs-snap-line {
  stroke: var(--snap-line-stroke-color);
  stroke-linecap: round;
  stroke-width: 2px;
  pointer-events: none;
}

/**
 * snapping
 */
.djs-crosshair {
  stroke: var(--space-tool-crosshair-stroke-color);
  stroke-linecap: round;
  stroke-width: 1px;
  pointer-events: none;
  shape-rendering: geometricPrecision;
  stroke-dasharray: 5, 5;
}

/**
 * palette
 */

.djs-palette {
  position: absolute;
  left: 20px;
  top: 20px;

  box-sizing: border-box;
  width: 48px;
}

.djs-palette .separator {
  margin: 5px;
  padding-top: 5px;

  border: none;
  border-bottom: solid 1px var(--palette-separator-color);

  clear: both;
}

.djs-palette .entry:before {
  vertical-align: initial;
}

.djs-palette .djs-palette-toggle {
  cursor: pointer;
}

.djs-palette .entry,
.djs-palette .djs-palette-toggle {
  color: var(--palette-entry-color);
  font-size: 30px;

  text-align: center;
}

.djs-palette .entry {
  float: left;
}

.djs-palette .entry img {
  max-width: 100%;
}

.djs-palette .djs-palette-entries:after {
  content: '';
  display: table;
  clear: both;
}

.djs-palette .djs-palette-toggle:hover {
  background: var(--palette-toggle-hover-background-color);
}

.djs-palette .entry:hover {
  color: var(--palette-entry-hover-color);
}

.djs-palette .highlighted-entry {
  color: var(--palette-entry-selected-color) !important;
}

.djs-palette .entry,
.djs-palette .djs-palette-toggle {
  width: 46px;
  height: 46px;
  line-height: 46px;
  cursor: default;
}

/**
 * Palette open / two-column layout is controlled via
 * classes on the palette. Events to hook into palette
 * changed life-cycle are available in addition.
 */
.djs-palette.two-column.open {
  width: 94px;
}

.djs-palette:not(.open) .djs-palette-entries {
  display: none;
}

.djs-palette:not(.open) {
  overflow: hidden;
}

.djs-palette.open .djs-palette-toggle {
  display: none;
}

.djs-hover-tooltip {
  position: fixed;
  z-index: 1000;

  display: flex;
  align-items: center;
  gap: 6px;

  padding: 6px 10px;
  border-radius: var(--surface-border-radius);

  background-color: var(--hover-tooltip-background-color);
  color: var(--hover-tooltip-color);

  font-family: var(--hover-tooltip-font-family);
  font-size: var(--hover-tooltip-font-size);
  line-height: 1.2;
  white-space: nowrap;

  pointer-events: none;
  box-shadow: 0 1px 4px var(--hover-tooltip-shadow-color);
}

.djs-hover-tooltip--right {
  transform: translateY(-50%);
}

.djs-hover-tooltip--top {
  transform: translate(-50%, -100%);
}

.djs-palette-tooltip-shortcut {
  padding: 1px 5px;

  border-radius: var(--button-border-radius);

  background-color: var(--palette-tooltip-shortcut-background-color);

  font-family: monospace;
  font-size: var(--hover-tooltip-secondary-font-size);
  line-height: 1.2;
}

/**
 * context-pad
 */
.djs-context-pad {
  position: absolute;
  display: none;
  pointer-events: none;
  line-height: 1;
  width: 72px;
  z-index: 100;
}

.djs-context-pad .entry {
  width: 22px;
  height: 22px;
  text-align: center;
  display: inline-block;
  font-size: 22px;
  margin: 0 2px 2px 0;

  border-radius: 3px;

  cursor: default;

  background-color: var(--context-pad-entry-background-color);
  box-shadow: 0 0 2px 1px var(--context-pad-entry-background-color);
  pointer-events: all;
  vertical-align: middle;
}

.djs-context-pad .entry:hover {
  background: var(--context-pad-entry-hover-background-color);
}

.djs-context-pad.open {
  display: block;
}

/**
 * popup styles
 */
.djs-popup {
  line-height: 1;
  box-sizing: border-box;
  background: var(--popup-background-color);
  overflow: hidden;
  position: fixed;
  z-index: 200;
  box-shadow: 0px 2px 6px var(--popup-shadow-color);
  border: solid 1px var(--popup-border-color);
  min-width: 120px;
  max-width: 300px;
  outline: none;
  font-size: var(--popup-font-size);
  font-family: var(--popup-font-family);
}

.djs-popup-search input {
  width: 100%;
  box-sizing: border-box;
  font-size: var(--popup-font-size);
  padding: 3px 6px 3px 28px;
  border-radius: var(--input-border-radius);
  border: solid 1px var(--popup-search-border-color);
  line-height: 21px;
}

.djs-popup-search input:focus {
  background-color: var(--popup-search-focus-background-color);
  border: solid 1px var(--popup-search-focus-border-color);
  outline: none;
}

.djs-popup-header {
  display: flex;
  align-items: stretch;
  line-height: 20px;
  margin: 10px 12px 10px 12px;
}

.djs-popup-header .entry {
  border-radius: 2px;
}

.djs-popup button.entry {
  padding: 0;
  background: transparent;
  border: 0;
}

.djs-popup-header .entry.active {
  color: var(--popup-header-entry-selected-color);
}

.djs-popup-header .entry.disabled {
  color: inherit;
}

.djs-popup-header-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
}

.djs-popup-header-group .entry {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.djs-popup-header-group + .djs-popup-header-group:before {
  content: '';
  width: 1px;
  height: 20px;
  background: var(--popup-header-group-divider-color);
  margin: 0 5px;
}

.djs-popup-search {
  position: relative;
  width: auto;
  margin: 10px 12px;
}

.djs-popup-tabs-container {
  position: relative;
  border-bottom: solid 1px var(--popup-tab-strip-border-color);
}

/**
 * The scroll control doubles as the edge fade: tabs scrolled past it fade out
 * rather than being cut off behind an opaque block.
 */
.djs-popup-tabs-scroll {
  appearance: none;
  position: absolute;
  top: 0;
  bottom: 1px;
  width: 28px;
  display: flex;
  align-items: center;
  padding: 0;
  border: none;
  border-radius: 0;
  color: var(--popup-tab-color);
  cursor: pointer;
}

.djs-popup-tabs-scroll:hover {
  color: var(--popup-tab-hover-color);
}

.djs-popup-tabs-scroll-start {
  left: 0;
  justify-content: flex-start;
  background: linear-gradient(to left, transparent, var(--popup-background-color) 60%);
}

.djs-popup-tabs-scroll-end {
  right: 0;
  justify-content: flex-end;
  background: linear-gradient(to right, transparent, var(--popup-background-color) 60%);
}

.djs-popup-tabs-scroll-start svg {
  transform: rotate(180deg);
}

.djs-popup-tabs {
  display: flex;
  flex-wrap: nowrap;
  gap: 2px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 0 12px;

  /* keep scrolled-to tabs clear of the scroll controls */
  scroll-padding: 0 28px;
  scrollbar-width: none;
}

.djs-popup-tabs::-webkit-scrollbar {
  display: none;
}

.djs-popup-tab {
  appearance: none;
  background: transparent;
  border: none;
  border-bottom: solid 2px transparent;
  border-radius: 0;
  flex: 0 0 auto;
  padding: 6px 10px;
  font: inherit;
  font-size: var(--popup-font-size);
  color: var(--popup-tab-color);
  cursor: pointer;
  white-space: nowrap;
}

.djs-popup-tab:hover {
  color: var(--popup-tab-hover-color);
}

.djs-popup-tab:focus-visible {
  outline: solid 1px var(--popup-tab-focus-border-color);
  outline-offset: -2px;
}

.djs-popup-tab[aria-selected="true"] {
  color: var(--popup-tab-active-color);
  border-bottom-color: var(--popup-tab-active-border-color);
  font-weight: var(--popup-header-font-weight);
}

.djs-popup-title {
  font-size: var(--popup-font-size);
  font-weight: var(--popup-header-font-weight);
  flex: 1;
  margin: 0;
}

.djs-popup-breadcrumbs {
  display: flex;
  line-height: 20px;
  margin: 10px 12px;
}

.djs-popup-breadcrumbs-item {
  display: inline-flex;
  min-width: 0;
  padding: 0;
  margin: 0;
  background: transparent;
  border: 0;
  outline: none;
  appearance: none;
  color: var(--popup-description-color);
  font: inherit;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.djs-popup-breadcrumbs-item--separator::before {
  display: inline-block;
  content: '/';
  color: var(--popup-description-color);
  margin: 0 4px;
}

.djs-popup-breadcrumbs-item:hover {
  color: inherit;
  text-decoration: underline;
}

.djs-popup-breadcrumbs-item:focus-visible {
  outline: 1px solid var(--popup-search-focus-border-color);
  outline-offset: 2px;
}

.djs-popup-breadcrumbs-item--back {
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: 2px 3px;
  margin-right: 6px;
  border: 1px solid var(--popup-search-border-color);
  border-radius: 4px;
}

.djs-popup-breadcrumbs-item--back:hover {
  background: var(--popup-button-hover-background-color);
}

.djs-popup-breadcrumbs-item--current {
  font-weight: var(--popup-header-font-weight);
  color: inherit;
  cursor: default;
}

.djs-popup-breadcrumbs-item--current:hover {
  text-decoration: none;
}

.djs-popup-entry-actions {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  gap: 6px;
  margin-left: 6px;
}

.djs-popup-entry-chevron {
  display: flex;
  align-items: center;
  color: var(--popup-description-color);
}

.djs-popup-search-icon {
  position: absolute;
  left: 8px;
  top: 7px;
}

.djs-popup-search-count {
  margin: 0 12px;
  font-size: var(--popup-secondary-font-size);
  color: var(--popup-description-color);
}

.djs-popup-results {
  margin: 7px 3px 7px 12px;
  list-style: none;
  max-height: 280px;
  overflow: auto;
  padding-right: 9px;
}

/**
 * The results list is focusable (as a listbox holding
 * `aria-activedescendant`) when there is no search field.
 * The active entry is indicated via `.entry.selected`, so we hide
 * the outline on the list container itself.
 */
.djs-popup-results:focus {
  outline: none;
}

.djs-popup-group {
  margin: 0;
  padding: 0;
  width: 100%;
}

.djs-popup-body .entry,
.djs-popup-body .entry-header {
  padding: 5px 7px;
  cursor: default;
  border-radius: 4px;
}

.djs-popup-body .entry-header {
  font-weight: var(--popup-header-font-weight);
  color: var(--popup-entry-title-color);
  padding-left: 0;
}

.djs-popup [class*="icon"] .djs-popup-label,
.djs-popup-label:not(:first-child) {
  margin-left: .5em;
}

.djs-popup [class*="icon"]:before,
.djs-popup-entry-icon {
  width: 1em;
  height: 1em;
  display: inline-block;
  font-size: 1.4em;
  vertical-align: middle;
}

.djs-popup-body .entry-header:not(:first-child) {
  margin-top: 8px;
  margin-bottom: 2px;
}

.djs-popup-body .entry {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  height: min-content;
}

.djs-popup .entry.selected {
  color: var(--popup-entry-selected-color);
  background-color: var(--popup-entry-selected-background-color);
}

.djs-popup .entry.disabled {
  color: var(--popup-disabled-color);
  cursor: not-allowed;
}

.djs-popup-body .entry:not(:first-child) {
  margin-top: 2px;
}

.djs-popup-entry-content {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.djs-popup-entry-description {
  font-size: var(--popup-secondary-font-size);
  margin-top: .25em;

  color: var(--popup-description-color);
}

.djs-popup-label,
.djs-popup-entry-description {
  line-height: 1.4em;
}

.djs-popup .entry,
.djs-popup .entry-header {
  margin: 1px;
}

.djs-popup-body {
  flex-direction: column;
  width: auto;
}

.djs-popup *::-webkit-scrollbar {
  width: 6px;
}

.djs-popup *::-webkit-scrollbar-thumb {
  border-radius: 3px;
  background-color: var(--popup-scrollbar-thumb-color);
}

.djs-popup *::-webkit-scrollbar-track {
  box-shadow: none;
  background: transparent;
  margin: 0;
  padding: 5px;
}

.djs-popup-no-results {
  padding: 0 12px 12px 12px;
  color: var(--popup-no-results-color);
}

.djs-popup-footer {
  display: flex;
  padding: 5px 12px 7px 12px;
  border-top: solid 1px var(--popup-border-color);
}

/**
 * The footer holds the keyboard/assistive-technology reachable documentation
 * link. Pointer interaction switches the popup to the per-entry
 * `.djs-popup-entry-docs` affordance instead.
 */
.djs-popup--pointer .djs-popup-footer {
  display: none;
}

.djs-popup-entry-docs {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  visibility: hidden;
  padding: 2px 3px;
  color: var(--popup-description-color);
  background: var(--popup-button-background-color);
  border: 1px solid var(--popup-search-border-color);
  border-radius: 4px;
  cursor: pointer;
  transition: background-color .12s ease, border-color .12s ease, color .12s ease;
}

.djs-popup--pointer .djs-popup-body .entry:hover .djs-popup-entry-docs {
  visibility: visible;
}

.djs-popup-body .entry .djs-popup-entry-docs:hover {
  background: var(--popup-button-hover-background-color);
}

.djs-popup-entry-docs svg {
  vertical-align: middle;
}

.djs-popup-footer-docs {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: var(--popup-secondary-font-size);
  color: var(--popup-description-color);
  text-decoration: none;
}

.djs-popup-footer-docs:hover {
  text-decoration: underline;
}

.djs-popup-footer-docs svg {
  vertical-align: middle;
  margin: 2px;
}

/**
 *  palette styles
 */
.djs-palette {
  background: var(--palette-background-color);
  border: solid 1px var(--palette-border-color);
  border-radius: var(--surface-border-radius);
}

/**
 * bendpoints
 */
.djs-segment-dragger,
.djs-bendpoint {
  display: none;
}

.djs-segment-dragger .djs-visual {
  display: none;

  fill: var(--bendpoint-fill-color);
  stroke: var(--bendpoint-stroke-color);
  stroke-width: 1px;
  stroke-opacity: 1;
}

.djs-segment-dragger:hover .djs-visual {
  display: block;
}

.djs-bendpoint .djs-visual {
  fill: var(--bendpoint-fill-color);
  stroke: var(--bendpoint-stroke-color);
  stroke-width: 1px;
}

.djs-segment-dragger:hover,
.djs-bendpoints.hover .djs-segment-dragger,
.djs-bendpoints.selected .djs-segment-dragger,
.djs-bendpoint:hover,
.djs-bendpoints.hover .djs-bendpoint,
.djs-bendpoints.selected .djs-bendpoint {
  display: block;
}

.djs-drag-active .djs-bendpoints * {
  display: none;
}

.djs-bendpoints:not(.hover) .floating {
  display: none;
}

.djs-bendpoint.floating:not(.positioned) {
  display: none;
}

.djs-segment-dragger:hover .djs-visual,
.djs-segment-dragger.djs-dragging .djs-visual,
.djs-bendpoint:hover .djs-visual,
.djs-bendpoint.floating .djs-visual {
  fill: var(--bendpoint-fill-color);
  stroke: var(--bendpoint-stroke-color);
  stroke-opacity: 1;
}

.djs-bendpoint.floating .djs-hit {
  pointer-events: none;
}

.djs-segment-dragger .djs-hit,
.djs-bendpoint .djs-hit {
  fill: none;
  pointer-events: all;
}

.djs-segment-dragger.horizontal .djs-hit {
  cursor: ns-resize;
}

.djs-segment-dragger.vertical .djs-hit {
  cursor: ew-resize;
}

.djs-segment-dragger.djs-dragging .djs-hit {
  pointer-events: none;
}

.djs-updating,
.djs-updating > * {
  pointer-events: none !important;
}

.djs-updating .djs-context-pad,
.djs-updating .djs-outline,
.djs-updating .djs-bendpoint,
.djs-multi-select .djs-bendpoint,
.djs-multi-select .djs-segment-dragger,
.connect-ok .djs-bendpoint,
.connect-not-ok .djs-bendpoint,
.drop-ok .djs-bendpoint,
.drop-not-ok .djs-bendpoint {
  display: none !important;
}

.djs-segment-dragger.djs-dragging,
.djs-bendpoint.djs-dragging {
  display: block;
  opacity: 1.0;
}


/**
 * tooltips
 */
.djs-tooltip-error {
  width: 160px;
  padding: 6px;

  background: var(--tooltip-error-background-color);
  border: solid 1px var(--tooltip-error-border-color);
  border-radius: var(--surface-border-radius);
  color: var(--tooltip-error-color);
  font-size: 12px;
  line-height: 16px;

  opacity: 0.75;
}

.djs-tooltip-error:hover {
  opacity: 1;
}


/**
 * search pad
 */
.djs-search-open .djs-context-pad {
  display: none;
}

.djs-search-open .djs-connection.selected .djs-outline {
  display: block;
}

.djs-search-container {
  position: absolute;
  top: 20px;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;

  width: 25%;
  min-width: 300px;
  max-width: 400px;
  z-index: 10;

  font-family: var(--search-font-family);
  font-size: var(--search-font-size);
  border-radius: var(--surface-border-radius);
  box-shadow: 0px 2px 6px var(--search-shadow-color);
}

.djs-search-container:not(.open) {
  display: none;
}

.djs-search-input {
  position: relative;
}

.djs-search-input svg {
  position: absolute;
  left: 8px;
  top: 7px;
}

.djs-search-input input {
  font-size: var(--search-font-size);
  width: 100%;
  padding: 3px 6px 3px 28px;
  border: 1px solid var(--search-input-border-color);
  border-radius: var(--input-border-radius);
  box-sizing: border-box;
  line-height: 21px;
}

.djs-search-input input:focus {
  background-color: var(--search-input-focus-background-color);
  border: solid 1px var(--search-input-focus-border-color);
  outline: none;
}

.djs-search-results {
  position: relative;
  overflow-y: auto;
  max-height: 200px;
  background: var(--search-container-background-color);
}

.djs-search-result {
  padding: 6px 8px;
}

.djs-search-result-primary {
  margin: 0 0 3px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.djs-search-result-secondary {
  font-family: monospace;
  margin: 0;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  color: var(--search-result-secondary-color);
}

.djs-search-result:hover {
  background: var(--search-result-hover-background-color);
}

.djs-search-result-selected {
  background: var(--search-result-hover-background-color);
}

.djs-search-result-selected:hover {
  background: var(--search-result-hover-background-color);
}

.djs-search-open .djs-element .djs-outline {
  fill: var(--search-preselected-background-color) !important;
}

/**
 * hidden styles
 */
.djs-element-hidden,
.djs-element-hidden .djs-hit,
.djs-element-hidden .djs-outline,
.djs-label-hidden .djs-label {
  display: none !important;
}

.djs-element .djs-hit-stroke,
.djs-element .djs-hit-click-stroke,
.djs-element .djs-hit-all {
  cursor: move;
}

FILE:pyproject.toml
[project]
name = "specir"
version = "0.1.0"
description = "specIR: cross-layer domain types over an SLDB store, built on sldb.api, and its tools on the MCP server of sldb (sldb mcp --extension specir.mcp_extension:register)"
requires-python = ">=3.12"
dependencies = [
    "structuredLanguageDB",
    "pyyaml>=6.0",
    "click>=8.1",
]

[project.optional-dependencies]
# The extension (specir.mcp_extension) runs on the MCP server of sldb.
mcp = [
    "structuredLanguageDB[mcp]",
]
test = [
    "structuredLanguageDB[mcp]",
    "pytest>=8",
    "pyyaml>=6.0",
]

[project.scripts]
specir-install = "specir.install:main"
# The visual layer's render, lint and schema commands (IR12); IR13d gives `specir` its full taxonomy.
specir = "specir.visual.commands:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
specir = ["data/*.yaml", "visual/templates/*.html", "visual/templates/vendor/bpmn-js/*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "parity: compares specIR with spec2viz as the oracle; skipped when spec2viz is not installed",
]

FILE:docs/spec2viz/matriz-de-cobertura.md
# Matriz de cobertura de spec2viz

Plan de cobertura para retirar spec2viz (tarea IR07). Cada capacidad de spec2viz tiene una fila con su
**modo** y su **condición de retiro**. Esta matriz **no acredita nada**: no hay columna de evidencia y
ninguna fila se da por cumplida. La tarea final IR13 añade por fila la prueba que acredita la cobertura
(después de IR13a, IR13b, IR13c e IR13d) y es la única que puede marcar una fila como cumplida.

- Revisión inventariada de spec2viz: commit `2de1056` del repo `spec2viz` (versión 0.2.0 en su
  `pyproject.toml`). La ayuda del CLI instalado (`spec2viz --help` y la de cada subgrupo) coincide con
  `spec2viz/spec2viz/cli.py` de esa revisión.
- Revisión de sldb consultada: rama main de `sldb` en `641ecdfa`. Plan de sldb que absorbe lo genérico:
  `sldb/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/` (`alcance.md`, `brief.md`, `decisiones.md`).
- Decisión vigente (JP, 2026-11-15): lo genérico va a sldb; specIR es adaptador y mapeo de dominio y
  conserva la capa visual (compiladores en IR11, renderers en IR12).
- La decisión sobre el papel del YAML de spec frente al grafo está en
  `docs/decisiones/fuente-de-verdad-del-diagrama.md` y en el atom
  `atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`. Es una **propuesta pendiente de JP**;
  ninguna fila de esta matriz depende de que se acepte en un sentido u otro salvo las marcadas con †.
- El procedimiento del gate está en `docs/spec2viz/gate-de-retiro.md`; la lista comprobable está al final
  de este documento.

## Modos

| Modo | Qué significa | Qué debe citar la fila |
|---|---|---|
| migrar tal cual | El código pasa a specIR (capa visual) con sus pruebas de spec2viz portadas. | Tarea de specIR que lo migra y pruebas de spec2viz que se portan. |
| reemplazar | Otra arquitectura o experiencia con resultado equivalente. | Sustituto y prueba que demostrará la equivalencia. |
| usar sldb directamente | Ya vive en SLDB; se consume por su API, su CLI o `sldb serve`, sin envoltorio ni reexportación en specIR. | Operación pública de SLDB que la respalda. |
| migrado a sldb | Pieza no visual ni de dominio; su código pasa a sldb con sus pruebas portadas y specIR la consume desde allí. | Tarea de sldb que la migra y pruebas de spec2viz que se portan a sldb. |

Tareas citadas (ids completos):

| Abreviatura | Tarea | Desk |
|---|---|---|
| D1 | `task-migrar-specsync-de-spec2viz-a-sldb-api-notations-junto-a-notationsync-y-palettesync-d1-b1-cierra-lo` (espejo en IR: `task-espejo-sldb-specsync-en-sldb-api-notations-d1`) | sldb |
| D2 | `task-migrar-a-sldb-el-generador-de-spec-de-componentes-desde-un-grafo-y-desde-el-ast-de-python-d2-b4` (espejo: `task-espejo-sldb-generador-de-spec-desde-grafo-y-ast-d2`) | sldb |
| D3 | `task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp` (espejo: `task-espejo-sldb-modelos-de-spec-por-tipo-de-diagrama-d3`) | sldb |
| D4 | `task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4` (espejo: `task-espejo-sldb-emparejamiento-de-átomos-en-sldb-api-matching-d4`) | sldb |
| IR11 | `task-ir11-compiladores-y-proyecciones-de-spec2viz` | IR |
| IR12 | `task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz` | IR |
| IR13a | `task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs` | IR |
| IR13b | `task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos` | IR |
| IR13d | `task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual` | IR |
| IR13 | `task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz` | IR |

IR13c (notaciones y paletas) se retiró porque era un envoltorio de `sldb notations`: sus filas están en
modo «usar sldb directamente» y la prueba de paridad de esas filas la aporta IR13 (ver «Pendientes de
derivación»).

Rutas: las de spec2viz son relativas a la raíz del repo `spec2viz` (`spec2viz/<módulo>.py` es el paquete;
`tests/` sus pruebas). Las pruebas citadas son las de `spec2viz/tests/` en la revisión inventariada.

## Matriz

### A. Modelos de spec, carga, validación y JSON Schema

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-A01 | Modelo de spec de diagrama de clases (paquetes, herencia, sobrecargas) | `spec2viz/models/class_diagram.py` | migrado a sldb | D3: subpaquete de modelos de diagrama junto a SpecDoc en sldb | Pasan en sldb, portadas por D3: de `tests/test_class_diagram.py` test_semantic_errors_are_rejected, test_inheritance_cycle_is_rejected_but_dependency_cycles_are_allowed, test_overloads_with_distinct_parameter_types_are_allowed y test_invalid_schema_fails_at_load; de `tests/test_class_packages.py` test_typed_validation y test_package_id_cannot_be_a_class_id. specIR no define el modelo (prueba de imports y nombres de IR11). |
| SV-A02 | Modelo de spec de secuencia | `spec2viz/models/sequence.py` | migrado a sldb | D3 | `tests/test_models_sequence.py` (3) portado a sldb y en verde; specIR importa el modelo de sldb (IR11). |
| SV-A03 | Modelo de spec de estado | `spec2viz/models/state.py` | migrado a sldb | D3 | `tests/test_models_state.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A04 | Modelo de spec de componentes | `spec2viz/models/component.py` | migrado a sldb | D3 | `tests/test_models_component.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A05 | Modelo de spec de actividad (particiones, merge, notas) | `spec2viz/models/activity.py` | migrado a sldb | D3 | `tests/test_models_activity.py` (3) portado a sldb y en verde; ídem IR11. |
| SV-A06 | Modelo de spec de despliegue (nodos anidados, communication paths) | `spec2viz/models/deployment.py` | migrado a sldb | D3 | `tests/test_models_deployment.py` (4) portado a sldb y en verde; ídem IR11. |
| SV-A07 | Modelo de spec de matriz (component_view_matrix) | `spec2viz/models/matrix.py` | migrado a sldb | D3 | `tests/test_models_matrix.py` (4) portado a sldb y en verde; ídem IR11. |
| SV-A08 | Modelo de spec de reflexión (enforcement) | `spec2viz/models/reflection.py` | migrado a sldb | D3 | spec2viz no tiene prueba de modelo propia de reflexión: la condición es la comparación de errores de D3 (misma clase y mismo texto de error) sobre todos los ejemplos y fixtures de spec2viz, que incluye `examples/reflection/`; specIR importa el modelo de sldb (IR11). |
| SV-A09 | Modelo base común (`BaseDiagram`, metadata, `DiagramType`) | `spec2viz/models/base.py` | migrado a sldb | D3 (DiagramType se reutiliza de `sldb.notations.diagram_type`, no se migra) | `tests/test_base_model.py` (3) portado a sldb y en verde. |
| SV-A10 | Modelo de catálogo (`vistas.yml` y stores jerárquicos de diagramas) | `spec2viz/models/catalog.py` | migrado a sldb | D3 | El modelo valida en sldb los fixtures de catálogo de spec2viz (`examples/catalog/`, `docs/architecture/spec2viz/vistas.yml`) con los mismos errores (comparación de errores de D3). |
| SV-A11 | Carga de un spec desde YAML (`load`) | `spec2viz/loader.py` | migrado a sldb | D3: `sldb.api.notations.load_spec` | `tests/test_loader.py` (16) portado a sldb y en verde. |
| SV-A12 | Validación semántica de un spec (`validate`) | `spec2viz/validator.py` | migrado a sldb | D3: `sldb.api.notations.validate_spec` | `tests/test_validator.py` (19) portado a sldb y en verde. |
| SV-A13 | Errores de carga y validación (`ParseError`, `ValidationError` y su jerarquía) | `spec2viz/exceptions.py` | migrado a sldb | D3: `ParseError` nueva bajo `NotationError`; el resto se reutiliza de `sldb.notations.exceptions` | `tests/test_exceptions.py` (2), solo los asertos de ParseError y ValidationError, portado a sldb y en verde. |
| SV-A14 | Errores de la capa visual (`Spec2VizError`, `CompileError`, `RenderError`) | `spec2viz/exceptions.py` | migrar tal cual | IR11 (CompileError) e IR12 (RenderError, raíz visual) | Los asertos de `tests/test_exceptions.py` sobre esas tres clases pasan en specIR con sus nombres; las pruebas de compiladores y renderers portadas levantan las mismas clases. |
| SV-A15 | Export de JSON Schema de specs (por tipo o todos) | `spec2viz/schema.py` | migrar tal cual | IR12 (`src/specir/visual/schema.py`) | El schema que exporta specIR es igual al de spec2viz para cada tipo (prueba de schema de IR12); pasan portadas test_json_schema_for_all_types, test_json_schema_for_specific_type y test_write_json_schema de `tests/test_api.py`, test_schema_stdout, test_schema_outfile y test_schema_invalid_type_fails de `tests/test_cli.py`, y test_schema_examples_match_generated_output y test_every_model_field_has_a_description de `tests/test_packaging.py`. |
| SV-A16 | Export de JSON Schema de catálogos y stores jerárquicos | `spec2viz/schema.py`, `spec2viz/cli.py` (`catalog schema`) | migrar tal cual | IR12 | Igual a spec2viz; pasan portadas test_schema_diagram_store_stdout y test_catalog_schema_stdout de `tests/test_cli.py`. |
| SV-A17 | Modelos de store de spec2viz (`SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc`) | `spec2viz/sldb_models.py` | usar sldb directamente | Modelos públicos de sldb: `sldb.models.notation.spec_doc.SpecDoc`, `spec_node_doc.SpecNodeDoc`, `notation_doc.NotationDoc`, `glyph_doc.GlyphDoc`, `link_doc.LinkDoc`, `palette_doc.PaletteDoc`, `view_doc.ViewDoc` | Los casos de `tests/test_view_doc.py` (3) pasan importando `ViewDoc` de sldb; specIR no define ninguna clase con esos nombres (IR11); ningún store registra `spec2viz.sldb_models` (gate G5). |

### B. Representación intermedia y compiladores (IR11)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-B01 | Representación intermedia visual (una dataclass por tipo de diagrama, `EnforcementArtifact`) | `spec2viz/ir.py` | migrar tal cual | IR11 | `tests/test_ir.py` (3) portado a specIR y en verde. |
| SV-B02 | Despacho de compilación por tipo (`compile_ir`) | `spec2viz/compilers/__init__.py` | migrar tal cual | IR11 | test_compile_* de `tests/test_api.py` (6) y `tests/test_compilers.py` (17) portados y en verde con la normalización de IR11. |
| SV-B03 | Compilador de clases | `spec2viz/compilers/class_diagram.py` | migrar tal cual | IR11 | Pasan en specIR las pruebas de compilación y render de `tests/test_class_diagram.py` y `tests/test_class_packages.py` que no porta D3 (las que invocan compile_ir o render). |
| SV-B04 | Compilador de secuencia | `spec2viz/compilers/sequence.py` | migrar tal cual | IR11 | Casos de secuencia de `tests/test_compilers.py` portados; IR equivalente según la normalización de IR11. |
| SV-B05 | Compilador de estado | `spec2viz/compilers/state.py` | migrar tal cual | IR11 | Casos de estado de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B06 | Compilador de componentes | `spec2viz/compilers/component.py` | migrar tal cual | IR11 | Casos de componentes de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B07 | Compilador de actividad (particiones, merge, notas) | `spec2viz/compilers/activity.py` | migrar tal cual | IR11 | Casos de actividad de `tests/test_compilers.py` y `tests/test_activity_lanes.py` (10) portados; IR equivalente. |
| SV-B08 | Compilador de despliegue (anidado, communication paths, deploy/manifest) | `spec2viz/compilers/deployment.py` | migrar tal cual | IR11 | Casos de despliegue de `tests/test_compilers.py` y `tests/test_deployment_nested.py` (6) portados; IR equivalente. |
| SV-B09 | Compilador de matriz | `spec2viz/compilers/matrix.py` | migrar tal cual | IR11 | Casos de matriz de `tests/test_compilers.py` portados; IR equivalente. |
| SV-B10 | Compilador de reflexión (artefacto de enforcement) | `spec2viz/compilers/reflection.py` | migrar tal cual | IR11 | `tests/test_reflection_compiler.py` (1) portado y en verde. |

### C. Renderizadores (IR12)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-C01 | Despacho de render, selector `--renderer`/`--backend` (9 valores), extensiones y renderer por defecto por tipo | `spec2viz/renderers/__init__.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/__init__.py`) | Los 9 valores (plantuml, mermaid, vega, d2, antonia-html, tree, graph, bpmn, json) existen en specIR; test_render_str, test_render_dict y test_render_mermaid_override de `tests/test_api.py` y test_render_override y test_render_backend_alias de `tests/test_cli.py` portados y en verde. |
| SV-C02 | Mermaid | `spec2viz/renderers/mermaid.py` | migrar tal cual | IR12 | Casos mermaid de `tests/test_renderers.py` (golden idéntico o diferencia declarada aquí con su prueba), más los de `tests/test_activity_lanes.py` y `tests/test_deployment_nested.py`. |
| SV-C03 | PlantUML | `spec2viz/renderers/plantuml.py` | migrar tal cual | IR12 | Casos plantuml de `tests/test_renderers.py`, `tests/test_activity_lanes.py` y `tests/test_deployment_nested.py`. |
| SV-C04 | D2 | `spec2viz/renderers/d2.py` | migrar tal cual | IR12 | Casos d2 de `tests/test_renderers.py`, `tests/test_activity_lanes.py`, `tests/test_deployment_nested.py` y test_render_d2 de `tests/test_cli.py`. |
| SV-C05 | Vega (matriz) | `spec2viz/renderers/vega.py` | migrar tal cual | IR12 | Casos vega de `tests/test_renderers.py` y test_render_to_file_vega de `tests/test_api.py`. Diferencia declarada (IR12): spec2viz listaba el dominio de la escala `kindColor` en el orden de un set, que cambia con `PYTHONHASHSEED`; specIR lo lista en orden de primera aparición y el color de cada kind es el mismo. Prueba: test_vega_lists_the_kinds_in_order_of_first_appearance y la paridad de `tests/visual/test_render_parity.py`, que compara esa escala como correspondencia kind → color. |
| SV-C06 | BPMN (XML con DI) | `spec2viz/renderers/bpmn.py` | migrar tal cual | IR12 | `tests/test_bpmn.py` (26), parte XML y DI, portado y en verde. |
| SV-C07 | Visor BPMN offline (bpmn-js embebido, leyenda, metadata, panel) | `spec2viz/renderers/bpmn_viewer.py` | migrar tal cual | IR12 | Casos del visor de `tests/test_bpmn.py`; la prueba de recursos de IR12 abre el HTML sin recursos externos faltantes. |
| SV-C08 | Paleta BPMN in Color compartida por renderer y visor | `spec2viz/renderers/bpmn_palette.py` | migrar tal cual | IR12 | Mismos colores en XML y visor sobre los fixtures de `tests/test_bpmn.py`. |
| SV-C09 | Árbol (HTML colapsable) | `spec2viz/renderers/tree.py` | migrar tal cual | IR12 | Casos tree de `tests/test_renderers.py` portados. |
| SV-C10 | HTML de grafo (DOM puro, sin CDN) | `spec2viz/renderers/graph_html.py` | migrar tal cual | IR12 | Casos graph de `tests/test_renderers.py` y test_render_to_file_component de `tests/test_api.py`; abre desde file:// sin recursos externos (prueba de recursos de IR12). |
| SV-C11 | antonia-html | `spec2viz/renderers/antonia.py` | migrar tal cual | IR12 | Casos antonia de `tests/test_renderers.py` y test_render_antonia_html de `tests/test_cli.py`. |
| SV-C12 | Salida JSON (`JsonRenderer`, artefacto `.artifact.json`) | `spec2viz/renderers/__init__.py` | migrar tal cual | IR12 (`json_out`) | test_render_json_reflection_artifact de `tests/test_cli.py` portado y en verde. |
| SV-C13 | Backends UML de sintaxis para el ClassIR (mermaid y plantuml de clases) | `spec2viz/renderers/class_diagram.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/class_diagram.py`) | Casos de clases de `tests/test_renderers.py`, `tests/test_class_diagram.py` y `tests/test_class_packages.py` con render. |
| SV-C14 | Mermaid desde una vista resuelta (glifo, forma, keyword, compartimentos, estilo) | `spec2viz/renderers/view_mermaid.py` | migrar tal cual | IR12 (`src/specir/visual/renderers/view_mermaid.py`), consumiendo `sldb.api.notations.resolve_view` | `tests/test_catalog_resolved_views.py` (8) portado y en verde contra la vista resuelta de sldb. |
| SV-C15 | Prueba de regresión de render a archivo | `spec2viz/__init__.py` (`render_to_file`) | migrar tal cual | IR12 e IR13d | `tests/test_rendering_bug.py` (1) portado y en verde. |

### D. Linter

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-D01 | Linter de Mermaid (heurísticas y pasada real con mmdc si está) | `spec2viz/linters/mermaid.py` | migrar tal cual | IR12 (`src/specir/visual/lint_mermaid.py`; la variable `SPECIR_MMDC` sustituye a `SPEC2VIZ_MMDC`, que sigue valiendo) | `tests/test_mermaid_mmdc.py` (4) portado y en verde; los mismos hallazgos que spec2viz sobre los fixtures de lint (prueba de lint de IR12). |

### E. Sincronización al store (SpecSync)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-E01 | SpecSync: materializar un spec como SpecDoc, SpecNodeDoc y RelationDoc, crear el RelationTypeDoc que falte y borrar lo que salió del spec; informe (`format_report`) | `spec2viz/sldb_sync.py` | migrado a sldb | D1: `SpecSync`, `sync_spec` en `sldb.api.notations`; `sldb notations sync --spec`. Reutiliza `StoreWriter` y `SyncReport` de sldb | `tests/test_sldb_sync.py` (16) portado a sldb, contra store real y sin mocks, en verde; informe igual campo a campo al de spec2viz sobre los mismos specs (D1); specIR llama a la API de sldb (IR13a). |
| SV-E02 | Sincronización de notaciones y paletas al store (`NotationSync`, `PaletteSync`, `format_notation_report`) | `spec2viz/sldb_sync.py` | usar sldb directamente | `sldb.api.notations.NotationSync`, `PaletteSync`, `sync_notation`, `sync_palette`; CLI `sldb notations sync --notation/--palette` | Los casos de notación y paleta de `tests/test_sldb_sync.py` y `tests/test_style_palette.py` que sincronizan pasan llamando a la API de sldb, sin envoltorio en specIR. |

### F. Generación de specs

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-F01 | from-graph: compilar el grafo de un store (edge index) o un snapshot node-link en un spec de componentes | `spec2viz/graph_import.py` | migrado a sldb | D2: `component_spec_from_graph` en `sldb.api.notations`; `sldb notations from-graph --snapshot/--store` | `tests/test_graph_import.py` (21) portado a sldb y en verde; todo spec generado valida con el modelo de componentes de D3. |
| SV-F02 | Generar un spec de componentes desde el AST de Python | `spec2viz/generators/python_ast.py` | migrado a sldb | D2: `component_spec_from_python` sobre `sldb.code.scan_tree`, `write_component_spec`; `sldb notations from-graph --python` | spec2viz no tiene pruebas de este generador: la condición es la prueba nueva de D2 que compara con `generate_python_ast_spec` de spec2viz sobre un árbol pequeño (mismos módulos, clases y relaciones defines) y valida con el modelo de D3. |

### G. Catálogos

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-G01 | Construcción del catálogo HTML autocontenido desde un `vistas.yml` o un store de stores (marca, subtítulo, plantilla local, `project.yml`, secciones HTML, anchors únicos) | `spec2viz/orchestrator.py` | migrar tal cual | IR13b con los renderers de IR12 | test_build_command* (7), test_catalog_build_alias_matches_legacy_build y test_build_command_reports_errors de `tests/test_cli.py` portados y en verde; mismas vistas, categorías y navegación que spec2viz sobre el fixture (IR13b). |
| SV-G02 | Registro `vistas.yml` y stores jerárquicos de diagramas: regla de rutas de `src`, `mmd`, `specs` y `notation` | `spec2viz/catalog_paths.py` | migrar tal cual | IR13b | `tests/test_catalog_paths.py` (9) portado y en verde. |
| SV-G03 | Vistas del catálogo desde la vista resuelta (misma fuente que graph_ui) | `spec2viz/catalog_views.py` | migrar tal cual | IR13b, consumiendo `sldb.api.notations.resolve_view` | `tests/test_catalog_resolved_views.py` (8) portado y en verde (compartido con SV-C14). |
| SV-G04 | Sincronización del catálogo al store (`catalog sync`: cada spec del `vistas.yml` con su notación y metadata) | `spec2viz/sldb_sync.py` (`sync_catalog`) | migrado a sldb | D1: `sync_catalog`; `sldb notations sync --catalog` (con `--prune` para borrar los SpecDoc que salieron) | `tests/test_catalog_notation.py` (6) portado a sldb y en verde; no escribe nada si una vista falla (IR13b). |
| SV-G05 | Validación del catálogo (`catalog validate`: specs existen y validan, notaciones del tipo correcto) | `spec2viz/sldb_sync.py` (`check_catalog`) | migrado a sldb | D1: `check_catalog`; `sldb notations sync --catalog --check` | Casos de validación de `tests/test_catalog_notation.py` portados a sldb; mismos errores tipados que spec2viz (IR13b). |
| SV-G06 | Servir el catálogo en local con autoguardado de anotaciones (`catalog serve`) | `spec2viz/cli.py` (`catalog_serve`) | reemplazar | Sustituto: `sldb serve` (lectura de documento por id y escritura con guarda de hash, comprobado por D4 paso 7) más el JS del catálogo de specIR (IR13b) | Prueba de equivalencia: IR13b demuestra que una anotación hecha con el catálogo servido por `sldb serve` queda guardada y reaparece al recargar. Si D4 concluye que `sldb serve` no alcanza, la fila no se cumple hasta que sldb resuelva la nota `serve/annotation-autosave-gap`. |
| SV-G07 | Inyección de átomos en el HTML del catálogo (`render_deskops`, `build_deskops`, `split_shared_atoms`, adaptador `CatalogItem`) | `spec2viz/deskops.py` | migrar tal cual | IR13b (capa visual; D4 lo deja fuera de sldb) | `tests/test_deskops.py` (7) y, de `tests/test_atoms_matching.py`, test_split_shared_atoms_emits_repeated_payload_once y test_catalog_build_embeds_atoms_once_and_honors_atoms_tag, portados y en verde. |
| SV-G08 | Plantilla HTML del catálogo, incluido el emparejamiento difuso en el navegador (`findAtomData`, `normKey`) y las pestañas por átomo | `spec2viz/templates/default.html` | migrar tal cual | IR12 (`src/specir/visual/templates/default.html`) e IR13b | Los casos de `tests/test_atoms_matching.py` que ejecutan la plantilla con node y test_tabs_follow_the_target_atom portados y en verde; `label_key` de D4 sigue coincidiendo con `normKey`. |

### H. Notaciones, paletas y estilo (usar sldb directamente)

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-H01 | Modelo, carga y validación de notaciones (NotationDoc, GlyphDoc, LinkDoc en YAML; `where` en la gramática de `sldb find --where`) | `spec2viz/notation.py` | usar sldb directamente | `sldb.notations.load_notation`, `sldb.notations.NotationSpec` | Los casos de `tests/test_notation.py` (14) pasan contra `sldb.notations` sin envoltorio en specIR. |
| SV-H02 | Notaciones builtin (8) y notación por defecto por tipo | `spec2viz/notations/*.yml`, `DEFAULT_NOTATIONS` | usar sldb directamente | `sldb.notations.builtin_notations`, `sldb.notations.DEFAULT_NOTATIONS` | Las 8 notaciones de spec2viz (activity, component, component-view-matrix, deployment, reflection, statechart, uml-class, uml-sequence) aparecen en `sldb notations list` y su contenido valida igual. |
| SV-H03 | Vista resuelta de un spec (glifo por nodo, link por relación, leyenda) y de documentos sin SpecDoc | `spec2viz/notation_view.py` (`resolve_view`, `resolve_documents`) | usar sldb directamente | `sldb.api.notations.resolve_view`, `sldb.api.notations.resolve_documents`; CLI `sldb notations view` y `sldb notations resolve` | `tests/test_notation_view.py` (11) y `tests/test_view_contract_resolved.py` (2) pasan contra la API de sldb; graph_ui ya no importa `spec2viz.notation_view` (gate G4). |
| SV-H04 | Modelo, carga y validación de paletas, con contraste WCAG (trazo ≥ 3:1, texto ≥ 4.5:1, forma+icono distintos por kind) | `spec2viz/palette.py` | usar sldb directamente | `sldb.notations.load_palette`, `sldb.notations.PaletteSpec`, `sldb.notations.contrast` | Los casos de paleta y contraste de `tests/test_style_palette.py` pasan contra `sldb.notations`. |
| SV-H05 | Paleta builtin `default` | `spec2viz/palettes/default.yml` | usar sldb directamente | `sldb.notations.builtin_palettes` (`src/sldb/notations/palettes/default.yml`) | `sldb notations list` la lista y su contenido valida igual. |
| SV-H06 | Estilo con una sola precedencia (glifo > `style.kinds` del spec > paleta) | `spec2viz/styling.py` | usar sldb directamente | `sldb.notations.resolve_style`, `sldb.notations.resolve_line_color` | Los casos de precedencia de `tests/test_style_palette.py` pasan contra `sldb.notations`. |

### I. Emparejamiento de átomos con elementos de diagrama

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-I01 | Emparejamiento explícito (`atoms:` en el elemento), alias por título y etiquetas, filtro por tags, avisos y modo estricto (`UnknownAtomError`) | `spec2viz/deskops.py` | migrado a sldb | D4: `sldb.api.matching` (módulos de claves y alias, resolución explícita) | Portados a sldb y en verde: de `tests/test_atoms_matching.py` test_filter_atoms_payload_by_full_tag_or_value; de `tests/test_explicit_atoms.py` test_build_exposes_explicit_map_by_label_and_id, test_unknown_atom_is_warning_unless_strict, test_fully_explicit_view_embeds_no_fuzzy_payload, test_partially_explicit_view_keeps_fuzzy_payload y test_atoms_linked_from_explicit_are_embedded_one_level. |
| SV-I02 | Emparejamiento difuso de átomos con elementos | `spec2viz/templates/default.html` (en el navegador) | migrado a sldb | D4: `DocumentIndex.rank` sobre `Matcher`/`DifflibMatcher` con alias (sin matcher nuevo); el JS del navegador sigue en SV-G08 | Prueba nueva de D4 de emparejamiento difuso con alias en verde, y SV-G08 cumplida. |
| SV-I03 | Referencias `refs: [Model:name]` por elemento hacia documentos sldb y aristas de átomos (`collect_explicit_refs`, `build_explicit_refs`, `attach_atom_edges`) | `spec2viz/deskops.py` | migrado a sldb | D4 (resolución de refs) | `tests/test_refs.py` (14) en verde: los casos de resolución contra sldb (D4) y los de schema y CLI contra specIR (IR12, IR13d). D4 no lista hoy `tests/test_refs.py` entre sus pruebas portadas: ver pendientes. |
| SV-I04 | Cobertura de átomos por vista | `spec2viz/deskops.py` (`build_coverage_by_view`) | migrado a sldb | D4 (módulo de cobertura) | Prueba de cobertura de D4 en verde y los casos de cobertura de `tests/test_deskops.py` portados. |
| SV-I05 | Descubrimiento y carga del store de átomos (`SldbAtomResolver`) | `spec2viz/deskops.py` | usar sldb directamente | `sldb.api.stores.open_store` y lectura de documentos y del edge index de `sldb.api` | Las pruebas de SV-I01 a SV-I04 pasan sin `SldbAtomResolver`. |

### J. API Python pública, recursos empaquetados, about y habilidad

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-J01 | `spec2viz.load` y `spec2viz.validate` | `spec2viz/__init__.py` | migrado a sldb | D3: `sldb.api.notations.load_spec`, `validate_spec` | test_load_* (6), test_validate_passes y test_validate_fails de `tests/test_api.py` pasan contra la API de sldb. |
| SV-J02 | `compile_ir`, `render`, `json_schema`, `write_json_schema` | `spec2viz/__init__.py` | migrar tal cual | IR13d (API pública de la capa visual de specIR) | El resto de `tests/test_api.py` (27 en total) portado contra la API de specIR y en verde. |
| SV-J03 | `render_to_file` con cabecera de procedencia (`with_provenance`, `provenance_header`, `provenance_text`) y salida BPMN doble (`.bpmn` y `.bpmn.html`) | `spec2viz/__init__.py` | migrar tal cual | IR12 lo migra (`src/specir/visual/render_file.py`, lo necesita `diagram render`); IR13d lo expone en la API pública | test_render_to_file_* (7) de `tests/test_api.py` y test_rendered_text_projections_carry_a_provenance_header de `tests/test_cli.py` portados; la cabecera nombra el comando de specIR que valida. |
| SV-J04 | Recurso empaquetado: bpmn-js vendorizado | `spec2viz/templates/vendor/bpmn-js/` | migrar tal cual | IR12 (prueba de recursos) | El visor BPMN abre offline (SV-C07) y `tests/test_packaging.py` portado (incluido test_examples_render_successfully) en verde. |
| SV-J05 | Recurso empaquetado: plantilla HTML del catálogo | `spec2viz/templates/default.html` | migrar tal cual | IR12 | Ver SV-G08; la plantilla viaja en el paquete instalado de specIR (prueba de recursos de IR12). |
| SV-J06 | Recursos empaquetados: notaciones y paleta builtin | `spec2viz/notations/`, `spec2viz/palettes/` | usar sldb directamente | Builtins de sldb (`src/sldb/notations/builtin/`, `src/sldb/notations/palettes/`) vía `sldb.notations.builtin_notations` y `builtin_palettes` | specIR no empaqueta notaciones ni paletas; SV-H02 y SV-H05 cumplidas. |
| SV-J07 | Punto de entrada `spec2viz` y empaquetado (instala y arranca) | `pyproject.toml` (`[project.scripts]`), `spec2viz/cli.py` (`main`) | reemplazar | Sustituto: el comando de specIR (IR13d) | Prueba de IR13d: el paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado; test_primary_cli_still_exposes_commands de `tests/test_packaging.py` portado. |
| SV-J08 | Comando about (dónde viven los diagramas y cómo llega el flujo al HTML) | `spec2viz/cli.py` (`about`) | migrar tal cual | IR13d | El comando equivalente de specIR existe y lo invoca la prueba de CLI de IR13d; su texto nombra los comandos de specIR y de sldb que sustituyen a los de spec2viz. |
| SV-J09 | Habilidad de agente use-spec2viz | `.pi/skills/use-spec2viz/SKILL.md` (copia distinta en `deskops/.opencode/skills/use-spec2viz/SKILL.md`) | reemplazar | Sustituto: `skills/use-specir/SKILL.md` (IR13d) | Prueba de IR13d que extrae los comandos que nombra la habilidad y los invoca con ayuda; la habilidad no nombra comandos de spec2viz. |

### K. Comandos y subgrupos del CLI

Una fila por cada entrada que lista la ayuda (`spec2viz --help` y la de cada subgrupo). La correspondencia
detallada la escribe IR13d en `docs/spec2viz/correspondencia-cli.md`. Cuando la capacidad vive en sldb, el
equivalente es el comando de sldb y specIR no define subcomando propio.

| ID | Comando | Modo | Equivalente | Condición de retiro |
|---|---|---|---|---|
| SV-K01 | `spec2viz about` | migrar tal cual | Comando about de specIR (IR13d) | SV-J08. |
| SV-K02 | `spec2viz build` (alias de `catalog build`) | migrar tal cual | Alias en el comando de specIR (IR13d) | SV-G01; test_catalog_build_alias_matches_legacy_build portado. |
| SV-K03 | `spec2viz catalog` (subgrupo) | migrar tal cual | Subgrupo catalog de specIR con build y schema; sync, validate y serve remiten a sldb | SV-K04 a SV-K08 cumplidas. |
| SV-K04 | `spec2viz catalog build` | migrar tal cual | specIR (IR13b, IR13d) | SV-G01. |
| SV-K05 | `spec2viz catalog schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A16. |
| SV-K06 | `spec2viz catalog serve` | reemplazar | `sldb serve` sobre el store del catálogo (IR13b) | SV-G06. |
| SV-K07 | `spec2viz catalog sync` | migrado a sldb | `sldb notations sync --catalog` (D1) | SV-G04. |
| SV-K08 | `spec2viz catalog validate` | migrado a sldb | `sldb notations sync --catalog --check` (D1) | SV-G05. |
| SV-K09 | `spec2viz diagram` (subgrupo) | migrar tal cual | Subgrupo diagram de specIR con render, lint y schema (y validate, ver SV-K16); sync, from-graph y generate remiten a sldb | SV-K10 a SV-K16 cumplidas. |
| SV-K10 | `spec2viz diagram from-graph` | migrado a sldb | `sldb notations from-graph --snapshot/--store` (D2) | SV-F01; test_cli_from_graph_* (5) y test_cli_from_graph_module_prefix reescritos contra el comando de sldb (D2). |
| SV-K11 | `spec2viz diagram generate` | migrado a sldb | `sldb notations from-graph --python` (D2) | SV-F02. |
| SV-K12 | `spec2viz diagram lint` | migrar tal cual | specIR (IR12, IR13d) | SV-D01. |
| SV-K13 | `spec2viz diagram render` | migrar tal cual | specIR (IR12, IR13d) | test_render_* de `tests/test_cli.py` portados; SV-C01 a SV-C12. |
| SV-K14 | `spec2viz diagram schema` | migrar tal cual | specIR (IR12, IR13d) | SV-A15. |
| SV-K15 | `spec2viz diagram sync` | migrado a sldb | `sldb notations sync --spec` (D1) | SV-E01. |
| SV-K16 | `spec2viz diagram validate` | migrado a sldb | Lógica en sldb (`load_spec`, `validate_spec`, D3); hoy sldb no tiene comando que valide un spec: o sldb lo añade (pedido por su desk) o el comando de specIR lo invoca sin redefinir nada (IR13d) | test_validate_valid, test_validate_invalid y test_validate_all_types de `tests/test_cli.py` portados contra el comando elegido; SV-A11 y SV-A12. |
| SV-K17 | `spec2viz lint` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K12. |
| SV-K18 | `spec2viz notation` (subgrupo) | usar sldb directamente | `sldb notations` | SV-K19 a SV-K22 cumplidas. |
| SV-K19 | `spec2viz notation list` | usar sldb directamente | `sldb notations list` | SV-H02. |
| SV-K20 | `spec2viz notation sync` | usar sldb directamente | `sldb notations sync --notation` | SV-E02. |
| SV-K21 | `spec2viz notation validate` | usar sldb directamente | `sldb.notations.load_notation`; sldb no tiene hoy comando de validación de notaciones (ver pendientes) | SV-H01 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. |
| SV-K22 | `spec2viz notation view` | usar sldb directamente | `sldb notations view` | SV-H03. |
| SV-K23 | `spec2viz palette` (subgrupo) | usar sldb directamente | `sldb notations` (`list`, `sync --palette`) | SV-K24 a SV-K26 cumplidas. |
| SV-K24 | `spec2viz palette list` | usar sldb directamente | `sldb notations list` (incluye `builtin_palettes`) | SV-H05. |
| SV-K25 | `spec2viz palette sync` | usar sldb directamente | `sldb notations sync --palette` | SV-E02. |
| SV-K26 | `spec2viz palette validate` | usar sldb directamente | `sldb.notations.load_palette` (con contraste WCAG); sldb no tiene hoy comando de validación de paletas (ver pendientes) | SV-H04 y un comando de sldb que valide por nombre o ruta, pedido por el desk de sldb. |
| SV-K27 | `spec2viz render` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K13. |
| SV-K28 | `spec2viz schema` (alias) | migrar tal cual | Alias en specIR (IR13d) | SV-K14. |
| SV-K29 | `spec2viz validate` (alias) | migrado a sldb | Igual que SV-K16 | SV-K16. |
| SV-K30 | Ayuda raíz con taxonomía (diagram, catalog) y lista de renderers | migrar tal cual | Ayuda del comando de specIR (IR13d) | test_help_mentions_taxonomy_groups_and_renderers de `tests/test_cli.py` portado. |

### Pruebas de spec2viz por fila

Cada archivo de `spec2viz/tests/` y las filas que lo portan o reemplazan. El gate G2 exige que cada
archivo tenga todos sus casos cubiertos por alguna fila.

| Archivo | Filas |
|---|---|
| `tests/test_activity_lanes.py` | SV-A05, SV-B07, SV-C02, SV-C03, SV-C04 |
| `tests/test_api.py` | SV-A15, SV-B02, SV-C01, SV-C05, SV-C10, SV-J01, SV-J02, SV-J03 |
| `tests/test_atoms_matching.py` | SV-G07, SV-G08, SV-I01, SV-I02 |
| `tests/test_base_model.py` | SV-A09 |
| `tests/test_bpmn.py` | SV-C06, SV-C07, SV-C08, SV-J03 |
| `tests/test_catalog_notation.py` | SV-G04, SV-G05 |
| `tests/test_catalog_paths.py` | SV-G02 |
| `tests/test_catalog_resolved_views.py` | SV-C14, SV-G03 |
| `tests/test_class_diagram.py` | SV-A01, SV-B03, SV-C13 |
| `tests/test_class_packages.py` | SV-A01, SV-B03, SV-C13 |
| `tests/test_cli.py` | SV-A15, SV-A16, SV-C01, SV-C04, SV-C11, SV-C12, SV-G01, SV-J03, SV-K01 a SV-K30 |
| `tests/test_compilers.py` | SV-B02 a SV-B09 |
| `tests/test_deployment_nested.py` | SV-A06, SV-B08, SV-C02, SV-C03, SV-C04 |
| `tests/test_deskops.py` | SV-G07, SV-I04 |
| `tests/test_exceptions.py` | SV-A13, SV-A14 |
| `tests/test_explicit_atoms.py` | SV-I01 |
| `tests/test_graph_import.py` | SV-F01, SV-K10 |
| `tests/test_ir.py` | SV-B01 |
| `tests/test_loader.py` | SV-A11 |
| `tests/test_mermaid_mmdc.py` | SV-D01 |
| `tests/test_models_activity.py` | SV-A05 |
| `tests/test_models_component.py` | SV-A04 |
| `tests/test_models_deployment.py` | SV-A06 |
| `tests/test_models_matrix.py` | SV-A07 |
| `tests/test_models_sequence.py` | SV-A02 |
| `tests/test_models_state.py` | SV-A03 |
| `tests/test_notation.py` | SV-H01, SV-H02 |
| `tests/test_notation_view.py` | SV-H03 |
| `tests/test_packaging.py` | SV-A15, SV-J04, SV-J07 |
| `tests/test_reflection_compiler.py` | SV-B10 |
| `tests/test_refs.py` | SV-I03 |
| `tests/test_renderers.py` | SV-C02 a SV-C11, SV-C13 |
| `tests/test_rendering_bug.py` | SV-C15 |
| `tests/test_sldb_sync.py` | SV-E01, SV-E02 |
| `tests/test_style_palette.py` | SV-E02, SV-H04, SV-H06 |
| `tests/test_validator.py` | SV-A12 |
| `tests/test_view_contract_resolved.py` | SV-H03 |
| `tests/test_view_doc.py` | SV-A17 |

## Inventario de consumidores

Universo auditado por IR13 (y solo este; añadir uno exige actualizar primero esta sección). Búsqueda hecha
el 2026-11-15 sobre los repos con `.git` bajo `SLDB_1/` (`IR`, `deskops`, `pron`, `scion`, `sldb`,
`spec2viz`, `UIs/graph_ui`; `sldb-runtime` y `deskops-runtime` son checkouts de despliegue de `sldb` y
`deskops` y se auditan por su repo de origen) y sobre todo `store.yaml` y `store_index.yaml` bajo
`SLDB_1/`. `scion` no tiene dependencias de spec2viz. Clases de dependencia como las define IR13
(importación, dependencia declarada, invocación del comando, modelo registrado en un store).

| Consumidor | Archivo y línea | Clase | Sustituto previsto |
|---|---|---|---|
| graph_ui | `UIs/graph_ui/frontends/mindmap/sldb_adapter.py:245` (`from spec2viz.notation_view import ViewError, resolve_view`) | importación | `sldb.api.notations.resolve_view` y `ViewError` (SV-H03) |
| graph_ui | `UIs/graph_ui/frontends/mindmap/sldb_adapter.py:437` (`from spec2viz.notation_view import ViewError, resolve_documents`) | importación | `sldb.api.notations.resolve_documents` (SV-H03) |
| graph_ui | `UIs/graph_ui/pyproject.toml:19` (extra `notation = ["spec2viz>=0.1.0"]`) y `:24` (extra `test`) | dependencia declarada | quitar; sldb ya es dependencia |
| graph_ui | `UIs/graph_ui/.github/requirements-suite.txt:10` (`-e git+https://github.com/jpcosec/spec2viz@master#egg=spec2viz`, lo usa el CI para leer los specs piloto) | dependencia declarada (CI) | specs piloto copiados como fixtures o leídos desde specIR |
| graph_ui | `UIs/graph_ui/tests/test_projection_views.py:18` (importorskip), `:33` y `:82` (`spec2viz diagram sync`), `:167` (`spec2viz.sldb_models` ViewDoc) | importación e invocación | `sldb notations sync --spec` (SV-E01), `ViewDoc` de sldb (SV-A17) |
| graph_ui | `UIs/graph_ui/tests/test_mindmap_notation.py:20-21` (`from spec2viz.notation_view import resolve_view`) y `:45` (`spec2viz diagram sync`) | importación e invocación | SV-H03, SV-E01 |
| graph_ui | `UIs/graph_ui/tests/e2e_notation_class.py:58`, `e2e_notation_sequence.py:108`, `e2e_notation_deployment.py:92`, `e2e_notation_activity.py:128`, `e2e_notation_style.py:147`, `e2e_notation_legibility.py:38` y `:175`, `e2e_mindmap_notation.py:27` y `:48`, `e2e_review_workbench_views.py:40`, `:76` y `:96` (`spec2viz diagram sync` e importorskip) | importación e invocación | SV-E01 |
| deskops | `deskops/deskops/graph/desk_graph.py:75` (regla de rutas `FileRule(kind="spec", path_prefixes=("spec", "docs/architecture/spec2viz"))`) | regla de rutas del grafo del desk | decidir la ruta de specs según la decisión del YAML (†); pedido al desk de deskops |
| deskops | `deskops/desk/drawer/plans/workspace-documental/render_diagram.py:7` y `:9` (`spec2viz diagram validate` y `diagram render`) | invocación | comandos de specIR (SV-K13, SV-K16) |
| deskops | `deskops/docs/diagrams/README.md` y los `.md`/`.mmd` de `deskops/docs/diagrams/` que nombran a spec2viz | documentación de diagramas (no cuenta como dependencia para IR13; se regenera con specIR) | renderers de specIR |
| deskops | `deskops/.opencode/skills/use-spec2viz/SKILL.md`; `deskops/.claude/skills/deskops-workflow/SKILL.md` y `references/spec2viz-cli.md` (instruyen a agentes a invocar `spec2viz`) | habilidad de agente | `skills/use-specir/SKILL.md` (SV-J09) |
| pron | `pron/docs/spec2viz/build.py:22-24` (`spec2viz diagram validate`, `diagram render --backend mermaid`, `catalog build`) | invocación | comandos de specIR (SV-K13, SV-K16, SV-K04) |
| sldb | `sldb/docs/architecture/spec2viz/vistas.yml` y sus specs (`current-*.yml`, `python-ast.yml`) | registro de catálogo que construye `spec2viz catalog build` | catálogo de specIR (SV-G01) |
| sldb | `sldb/contracts/identity.toml:299` (`consumers = [..., "spec2viz", ...]`) | configuración de contrato | quitar spec2viz de la lista al retirarlo |
| IR (specIR) | `IR/tests/conftest.py:24` y `:80` (federa el store `spec2viz/.sldb`), `IR/tests/test_mcp_extension.py:24` (`SPEC_STORE = "spec2viz"`) | lectura del store de spec2viz en pruebas | store con modelos de sldb (G5) o fixture propio |
| store `spec2viz/.sldb` | `spec2viz/.sldb/store.yaml:44-57`, `spec2viz/.sldb/core/store_index.yaml:141-194`, `spec2viz/.sldb/core/models/{SpecDoc,SpecNodeDoc,NotationDoc,GlyphDoc,LinkDoc,PaletteDoc,ViewDoc}.yaml` | modelos `spec2viz.sldb_models` registrados | `sldb.models.notation.*` (SV-A17) |

Es el único store bajo `SLDB_1/` cuyo índice registra `spec2viz.sldb_models`.

Specs YAML existentes que afecta la decisión del YAML (†): `spec2viz` (44: `tests/fixtures/`,
`docs/architecture/spec2viz/`, `examples/`), `sldb` (46: `tests/fixtures/`, `docs/architecture/`),
`UIs/graph_ui` (24: `tests/fixtures/`, `docs/representacion/`), `pron` (4: `docs/spec2viz/specs/`),
`deskops` (1: `desk/drawer/plans/workspace-documental/`). Conteo de archivos con `type:` de uno de los
ocho tipos en la raíz, sin `.sldb/`, `build/` ni entornos.

## Pendientes de derivación

Lo que esta matriz deja abierto y debe convertirse en tarea o pedido (no lo resuelve IR07):

1. Filas «usar sldb directamente» (SV-A17, SV-E02, SV-H01 a SV-H06, SV-I05, SV-J06, SV-K18 a SV-K26):
   con IR13c retirada, ninguna tarea porta hoy `tests/test_notation.py`, `tests/test_notation_view.py`,
   `tests/test_view_contract_resolved.py`, `tests/test_style_palette.py` ni `tests/test_view_doc.py`
   contra sldb. La prueba de paridad la aporta IR13 (prueba en specIR que llama a sldb sin envoltorio) o
   una tarea nueva derivada de estas filas.
2. SV-K21 y SV-K26: sldb no tiene comando para validar una notación o una paleta por nombre o ruta.
   Pedido al desk de sldb (`deskops message send --to sldb`) pendiente.
3. SV-K16 y SV-K29: decidir si la validación de un spec por CLI la da sldb (pedido a su desk) o el comando
   de specIR sobre `load_spec`/`validate_spec`.
4. SV-I03: D4 no lista `tests/test_refs.py` entre sus pruebas portadas; pedir a sldb que lo incluya o
   asignar la parte de resolución a IR13b.
5. SV-C13 y SV-C14: resuelto por IR12, que incluyó en su lista de archivos los backends UML de clases y el
   mermaid desde vista resuelta.
6. Consumidores: pedidos de migración a los desks de graph_ui, deskops, pron y sldb (los emite IR13).

## Gate de retiro

Lista comprobable. spec2viz solo se retira cuando **todos** los ítems se cumplen; el procedimiento está en
`docs/spec2viz/gate-de-retiro.md` y lo evalúa IR13.

- [ ] **G1. Filas cumplidas.** Toda fila SV-* de esta matriz tiene su condición de retiro cumplida y la
  prueba que lo acredita citada por IR13 en la fila (ninguna fila sin prueba; ninguna dice descartado ni
  fuera de alcance).
- [ ] **G2. Suite de spec2viz.** Cada caso de cada archivo de `spec2viz/tests/` pasa contra specIR o
  contra sldb (portado), o pertenece a una fila en modo reemplazar cuya prueba equivalente está declarada y
  pasa. La tabla «Pruebas de spec2viz por fila» no deja archivo sin fila.
- [ ] **G3. CLI.** Cada comando y subgrupo de la ayuda de spec2viz (filas SV-K*) tiene equivalente que
  existe y una prueba lo invoca (`docs/spec2viz/correspondencia-cli.md` de IR13d).
- [ ] **G4. Consumidores.** Ningún consumidor del inventario importa ni invoca spec2viz: cero
  `import spec2viz`/`from spec2viz`, cero dependencias declaradas (pyproject, requirements, CI), cero
  invocaciones del comando `spec2viz` en código, scripts o configuración ejecutable, y ninguna habilidad de
  agente que instruya a invocarlo. El comprobador de IR13 sale con código distinto de cero si encuentra una.
- [ ] **G5. Stores.** Ningún store del universo registra modelos `spec2viz.sldb_models` en su
  `store.yaml`, su `store_index.yaml` ni sus `core/models/*.yaml`.
- [ ] **G6. specIR limpio.** Ningún módulo bajo `src/specir/` importa spec2viz (prueba de imports) y specIR
  no define envoltorios de lo que se usa de sldb directamente.
- [ ] **G7. Decisión del YAML.** La decisión sobre el YAML de spec frente al grafo
  (`docs/decisiones/fuente-de-verdad-del-diagrama.md`) está aceptada por JP y las filas marcadas con †
  están alineadas con ella.

FILE:tests/test_imports.py
"""specIR imports SLDB only through its public API (`sldb.api`), and never pron or spec2viz.

Until `sldb.api.notations` exports the diagram spec models of D3, `specir.visual.spec_models` is the
one module that imports them from `sldb.models.notation.diagram_specs` (and only from there). Until it
exports `resolve_style`, `load_palette` and `NotationError`, `specir.visual.notation_style` is the one
module that imports them from `sldb.notations` (and only from there).

The one exception is specIR's extension of the MCP server of sldb (`specir.mcp_extension`): it
is the only module that reaches `sldb.mcp` (the extension contract of `sldb mcp --extension`)
or `mcp`. specIR implements no MCP server of its own."""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "src" / "specir"
FORBIDDEN = ("pron", "spec2viz")
#: The only module allowed to reach the MCP server of sldb and the MCP SDK.
EXTENSION = PACKAGE / "mcp_extension.py"
#: The only module allowed to reach sldb's diagram spec models (D3), which `sldb.api.notations`
#: does not export yet (asked to sldb's desk); it imports them and nothing else of sldb's internals.
SPEC_MODELS = PACKAGE / "visual" / "spec_models.py"
SPEC_MODELS_PACKAGE = "sldb.models.notation.diagram_specs"
#: The only module allowed to reach sldb's notations package (style resolution, the default palette
#: and the notation error root), which `sldb.api` does not export yet (asked to sldb's desk).
NOTATION_STYLE = PACKAGE / "visual" / "notation_style.py"
NOTATIONS_PACKAGE = "sldb.notations"


def is_spec_models(module: str) -> bool:
    return module == SPEC_MODELS_PACKAGE or module.startswith(SPEC_MODELS_PACKAGE + ".")


def is_notations(module: str) -> bool:
    return module == NOTATIONS_PACKAGE or module.startswith(NOTATIONS_PACKAGE + ".")


def is_mcp(module: str) -> bool:
    return module.split(".")[0] == "mcp" or module == "sldb.mcp" or module.startswith("sldb.mcp.")


def imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.append(node.module)
        elif isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", None)) in ("__import__", "import_module"):
            names += [arg.value for arg in node.args if isinstance(arg, ast.Constant) and isinstance(arg.value, str)]
    return names


def test_package_imports_only_the_public_sldb_api() -> None:
    sources = sorted(PACKAGE.rglob("*.py"))
    assert sources, f"no source under {PACKAGE}"
    offending: list[str] = []
    for path in sources:
        for module in imported_modules(path):
            root = module.split(".")[0]
            if path == EXTENSION and is_mcp(module):
                continue
            if path == SPEC_MODELS and is_spec_models(module):
                continue
            if path == NOTATION_STYLE and module == NOTATIONS_PACKAGE:
                continue
            if root in FORBIDDEN or (root == "sldb" and module != "sldb.api" and not module.startswith("sldb.api.")):
                offending.append(f"{path.relative_to(PACKAGE.parent)}: {module}")
    assert not offending, offending


def test_sldb_is_reached_only_through_sldb_api() -> None:
    for path in sorted(PACKAGE.rglob("*.py")):
        assert "sldb" not in {m for m in imported_modules(path)}, f"{path}: bare `import sldb`"


def test_only_the_extension_reaches_mcp() -> None:
    reaching = {str(path.relative_to(PACKAGE.parent)) for path in sorted(PACKAGE.rglob("*.py")) if any(is_mcp(m) for m in imported_modules(path))}
    assert reaching == {str(EXTENSION.relative_to(PACKAGE.parent))}, reaching


def test_specir_has_no_mcp_server_of_its_own() -> None:
    assert not (PACKAGE / "mcp").exists(), "src/specir/mcp was migrated to sldb (sldb.mcp)"
    for path in sorted(PACKAGE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for server in ("MCPServer", "FastMCP", "build_server", ".run(\"stdio\")"):
            assert server not in text, f"{path}: {server}"
    pyproject = (PACKAGE.parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    assert "specir-mcp" not in pyproject and "specir.mcp." not in pyproject


def test_only_spec_models_reaches_the_diagram_spec_models() -> None:
    reaching = {str(path.relative_to(PACKAGE.parent)) for path in sorted(PACKAGE.rglob("*.py")) if any(is_spec_models(m) for m in imported_modules(path))}
    assert reaching == {str(SPEC_MODELS.relative_to(PACKAGE.parent))}, reaching


def test_only_notation_style_reaches_sldb_notations() -> None:
    reaching = {str(path.relative_to(PACKAGE.parent)) for path in sorted(PACKAGE.rglob("*.py")) if any(is_notations(m) for m in imported_modules(path))}
    assert reaching == {str(NOTATION_STYLE.relative_to(PACKAGE.parent))}, reaching

FILE:tests/visual/render_parity.py
"""The render parity corpus of IR12 and its oracle.

The corpus is every spec of IR11's parity corpus (`parity.CORPUS`) that loads and validates, drawn by
each of the nine renderers of spec2viz's selector. For each (spec, renderer) the outcome is the
rendered output (text, or the JSON-able value of `vega` and `json`) or the error's class name and
message; an activity spec also gets the SHA-256 of its offline BPMN viewer page (`bpmn.html`), which
inlines the vendored bpmn-js.

The oracle is spec2viz itself when it is installed (`spec2viz_renders`); `GOLDENS` keeps the outcomes
of its last run (`python tests/visual/render_parity.py` rewrites them), so the parity still holds
against them once spec2viz is retired. The same run saves spec2viz's lint findings on its lint fixtures
(`LINT_GOLDENS`) and the JSON Schema it exports for every type (`SCHEMA_GOLDENS`)."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import parity  # noqa: E402

REVISION = parity.REVISION
GOLDENS = HERE / "goldens" / f"spec2viz-{REVISION}-renders.json"
LINT_GOLDENS = HERE / "goldens" / f"spec2viz-{REVISION}-lint.json"
SCHEMA_GOLDENS = HERE / "goldens" / f"spec2viz-{REVISION}-schema.json"
#: Every value of `json_schema(diagram_type)` and of the CLI's `--type`: all types (`None`), each of the
#: seven types spec2viz exported and its three names of the diagram store envelope.
SCHEMA_TYPES = (None, "class", "sequence", "state", "component", "activity", "deployment",
                "component_view_matrix", "diagram-store", "catalog", "project")
#: The values of spec2viz's `--renderer` selector (`spec2viz.cli.DIAGRAM_RENDERERS`, revision `REVISION`).
RENDERERS = ("plantuml", "mermaid", "vega", "d2", "antonia-html", "tree", "graph", "bpmn", "json")
#: The specs of the corpus that load and validate (IR11's goldens say which).
VALID = sorted(rel for rel, outcome in parity.goldens().items() if outcome["error"] is None)


def _jsonable(value: Any) -> Any:
    """A render result as JSON: the `json` renderer returns an IR dataclass as is."""
    return json.loads(json.dumps(value, default=lambda o: dataclasses.asdict(o) if dataclasses.is_dataclass(o) else str(o)))


def outcomes(rel: str, load: Callable, compile_ir: Callable, render: Callable, bpmn_html: Callable) -> dict[str, Any]:
    diagram = load(parity.FIXTURES / rel)
    ir = compile_ir(diagram)
    result: dict[str, Any] = {}
    for renderer in RENDERERS:
        try:
            result[renderer] = {"out": _jsonable(render(ir, renderer))}
        except Exception as error:  # the class and the text are what is compared
            result[renderer] = {"error": [type(error).__name__, str(error)]}
    if "out" in result["bpmn"]:
        metadata = diagram.metadata.model_dump() if diagram.metadata else None
        page = bpmn_html(result["bpmn"]["out"], diagram.title, metadata)
        result["bpmn.html"] = hashlib.sha256(page.encode("utf-8")).hexdigest()
    return result


def specir_renders(rel: str) -> dict[str, Any]:
    from sldb.api.notations import load_spec

    from specir.visual.compilers import compile_ir
    from specir.visual.renderers import render
    from specir.visual.renderers.bpmn import render_bpmn_html

    return outcomes(rel, load_spec, compile_ir, render, render_bpmn_html)


def spec2viz_renders(rel: str) -> dict[str, Any]:
    from spec2viz.compilers import compile_ir
    from spec2viz.loader import load
    from spec2viz.renderers import render
    from spec2viz.renderers.bpmn import render_bpmn_html

    return outcomes(rel, load, compile_ir, render, render_bpmn_html)


# ── the rest of the oracle: every other use of spec2viz by the tests of IR12 goes through here ──


def spec2viz_selector() -> tuple[list[str], dict[str, str], dict[str, str]]:
    """spec2viz's `--renderer` values, its extensions and its default renderer per IR class name."""
    from spec2viz.cli import DIAGRAM_RENDERERS
    from spec2viz.renderers import DEFAULT_RENDERER, EXT_MAP

    return list(DIAGRAM_RENDERERS), dict(EXT_MAP), {k.__name__: v for k, v in DEFAULT_RENDERER.items()}


def spec2viz_view_to_mermaid(view: dict[str, Any], theme: str) -> str:
    from spec2viz.renderers.view_mermaid import view_to_mermaid

    return view_to_mermaid(view, theme=theme)


def spec2viz_lint() -> Callable:
    from spec2viz.linters.mermaid import lint_mermaid

    return lint_mermaid


def spec2viz_json_schema() -> Callable:
    from spec2viz.schema import json_schema

    return json_schema


def spec2viz_render_to_file(spec: str | Path, out: Path, renderer: str) -> Path:
    from spec2viz import render_to_file

    return render_to_file(spec, out=out, renderer=renderer)


def spec2viz_package_dir() -> Path:
    """Where the installed spec2viz package lives (its templates and vendored bpmn-js)."""
    import spec2viz

    return Path(spec2viz.__file__).parent


def comparable(outcome: dict[str, Any]) -> dict[str, Any]:
    """An outcome with the one order that spec2viz did not fix left out: its `vega` kind color scale
    listed the kinds of a set, so their order changed with `PYTHONHASHSEED`. The scale compares as
    the kind -> color mapping (specIR lists the kinds in order of first appearance)."""
    out = json.loads(json.dumps(outcome))
    vega = (out.get("vega") or {}).get("out")
    if isinstance(vega, dict):
        for scale in vega.get("scales", []):
            if scale.get("name") == "kindColor":
                scale["domain"], scale["range"] = sorted(zip(scale.pop("domain"), scale.pop("range"))), None
    return out


def goldens() -> dict[str, Any]:
    return json.loads(GOLDENS.read_text(encoding="utf-8"))


#: The lint fixtures of spec2viz: the texts of `tests/test_mermaid_mmdc.py` and the bad texts of
#: `tests/test_renderers.py`. `lint_cases` adds the mermaid that spec2viz rendered for the corpus.
LINT_TEXTS = {
    "paren-edge-label": "graph TD\n    a -->|ask (paso 2)| b\n",
    "brace-edge-label": "graph TD\n    a -->|fetch {id}| b\n",
    "nested-quotes": 'flowchart TD\n    e["mostrar "msg" fin"]\n',
    "html-entity-seq": "sequenceDiagram\n    A->>B: show &lt;name&gt;\n",
    "simple-graph": "graph TD\n    a --> b\n",
    "quoted-paren-edge": 'graph TD\n    a -->|"ask (paso 2)"| b\n',
    "sequence-ok": "sequenceDiagram\n    A->>B: hello\n",
    "invalid-return-arrow": "sequenceDiagram\n    A<<--B: reply",
    "raw-angle-brackets": "sequenceDiagram\n    A->>B: GET path?x=<id>",
    "bad-return-arrow": "sequenceDiagram\n    A<<--B: bad\n",
    "empty-decision": "flowchart TD\n    d{}\n",
}


def lint_cases() -> dict[str, str]:
    """Every lint fixture by name: `LINT_TEXTS` and the mermaid of each spec of the corpus that has one."""
    cases = dict(LINT_TEXTS)
    for rel, outcome in goldens().items():
        if "out" in outcome["mermaid"]:
            cases[f"mermaid:{rel}"] = outcome["mermaid"]["out"]
    return cases


def lint_findings(lint: Callable) -> dict[str, Any]:
    """The findings of `lint` on every lint fixture, with and without the raw-angle-bracket rule.
    The caller turns the mmdc pass off: the findings of the regex rules are what is compared."""
    return {name: {"check_html": lint(text, check_html=True), "no_html": lint(text, check_html=False)}
            for name, text in sorted(lint_cases().items())}


def lint_goldens() -> dict[str, Any]:
    return json.loads(LINT_GOLDENS.read_text(encoding="utf-8"))


def schemas(json_schema: Callable) -> dict[str, Any]:
    return {str(diagram_type or "all"): json_schema(diagram_type) for diagram_type in SCHEMA_TYPES}


def schema_goldens() -> dict[str, Any]:
    return json.loads(SCHEMA_GOLDENS.read_text(encoding="utf-8"))


def write_goldens() -> None:
    """The render outcomes of spec2viz over the valid corpus, and its lint findings, as the saved oracle."""
    import os

    from spec2viz.linters.mermaid import lint_mermaid
    from spec2viz.schema import json_schema

    data = {rel: spec2viz_renders(rel) for rel in VALID}
    GOLDENS.write_text(json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    os.environ["SPEC2VIZ_MMDC"] = "0"
    LINT_GOLDENS.write_text(json.dumps(lint_findings(lint_mermaid), indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    SCHEMA_GOLDENS.write_text(json.dumps(schemas(json_schema), indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE.parents[1] / "src"))
    write_goldens()
    print(f"{len(VALID)} specs x {len(RENDERERS)} renderers -> {GOLDENS}")

FILE:tests/visual/goldens/spec2viz-2de1056-lint.json
{
 "bad-return-arrow": {
  "check_html": [
   "line 2: invalid sequence arrow '<<--'. Mermaid return arrows are '-->>'. Use kind: return -> '-->>' (dashed, forward).\n    -> A<<--B: bad",
   "line 2: invalid sequence arrow '<<--'. Valid arrows: ->>, -->>, ->, -->, -x, --x, -), --)."
  ],
  "no_html": [
   "line 2: invalid sequence arrow '<<--'. Mermaid return arrows are '-->>'. Use kind: return -> '-->>' (dashed, forward).\n    -> A<<--B: bad",
   "line 2: invalid sequence arrow '<<--'. Valid arrows: ->>, -->>, ->, -->, -x, --x, -), --)."
  ]
 },
 "brace-edge-label": {
  "check_html": [],
  "no_html": []
 },
 "empty-decision": {
  "check_html": [
   "line 2: empty decision node label '{}' is not renderable.\n    -> d{}"
  ],
  "no_html": [
   "line 2: empty decision node label '{}' is not renderable.\n    -> d{}"
  ]
 },
 "html-entity-seq": {
  "check_html": [],
  "no_html": []
 },
 "invalid-return-arrow": {
  "check_html": [
   "line 2: invalid sequence arrow '<<--'. Mermaid return arrows are '-->>'. Use kind: return -> '-->>' (dashed, forward).\n    -> A<<--B: reply",
   "line 2: invalid sequence arrow '<<--'. Valid arrows: ->>, -->>, ->, -->, -x, --x, -), --)."
  ],
  "no_html": [
   "line 2: invalid sequence arrow '<<--'. Mermaid return arrows are '-->>'. Use kind: return -> '-->>' (dashed, forward).\n    -> A<<--B: reply",
   "line 2: invalid sequence arrow '<<--'. Valid arrows: ->>, -->>, ->, -->, -x, --x, -), --)."
  ]
 },
 "mermaid:docs/architecture/spec2viz/activity-render-error-handling.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/class-sldb-models.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/component-architecture.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/component-exception-hierarchy.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/component-type-system.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/sequence-build-pipeline.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/sequence-render-pipeline.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/sequence-sync-pipeline.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/state-diagram-sync-lifecycle.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:docs/architecture/spec2viz/state-diagram-type-lifecycle.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/activity/example.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/activity/validation.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/catalog/leaves/sample-component.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/class/runtime.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/component/example.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/deployment/example.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/fixtures/canonical.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/sequence/example.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:examples/state/example.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/activity.complex.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/activity.groups.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/activity.lanes.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/activity.mepu-decision.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/activity.validation.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/class.packages.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/component.kinds.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/component.quotation.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/component.styled.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/deployment.nested.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/deployment.runtime.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/sequence.create-quotation.yml": {
  "check_html": [],
  "no_html": []
 },
 "mermaid:tests/fixtures/state.quotation.yml": {
  "check_html": [],
  "no_html": []
 },
 "nested-quotes": {
  "check_html": [],
  "no_html": []
 },
 "paren-edge-label": {
  "check_html": [],
  "no_html": []
 },
 "quoted-paren-edge": {
  "check_html": [],
  "no_html": []
 },
 "raw-angle-brackets": {
  "check_html": [
   "line 2: raw '<...>' in a label/message is parsed as HTML by mermaid and breaks the diagram. Escape as '&lt;...&gt;' or drop the brackets.\n    -> A->>B: GET path?x=<id>"
  ],
  "no_html": []
 },
 "sequence-ok": {
  "check_html": [],
  "no_html": []
 },
 "simple-graph": {
  "check_html": [],
  "no_html": []
 }
}

FILE:tests/visual/fixtures/spec2viz/examples/schema/sequence.schema.json
{
  "$defs": {
    "MessageModel": {
      "additionalProperties": false,
      "properties": {
        "from": {
          "description": "Participant id that sends the message.",
          "title": "From",
          "type": "string"
        },
        "to": {
          "description": "Participant id that receives the message.",
          "title": "To",
          "type": "string"
        },
        "message": {
          "description": "Label displayed on the message arrow.",
          "title": "Message",
          "type": "string"
        },
        "kind": {
          "default": "sync",
          "description": "Message interaction type, such as sync or async.",
          "title": "Kind",
          "type": "string"
        },
        "condition": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Optional condition that qualifies when the message is sent.",
          "title": "Condition"
        },
        "group": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Optional group label for visually related messages.",
          "title": "Group"
        }
      },
      "required": [
        "from",
        "to",
        "message"
      ],
      "title": "MessageModel",
      "type": "object"
    },
    "Metadata": {
      "additionalProperties": false,
      "description": "Authorship and description, plus the project's own annotations as ``x-*`` keys.\n\n``metadata`` is the only place a project may add keys of its own, and only with the ``x-`` prefix\n(``x-fuentes``, ``x-estado``): they are kept as written under ``extensions``. Any other unknown key is\nan error with its path, like everywhere else in a spec (a typo there is caught, not silently kept).",
      "properties": {
        "author": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Name of the person or team responsible for the diagram spec.",
          "title": "Author"
        },
        "description": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Free-form summary that explains the intent of the diagram.",
          "title": "Description"
        },
        "preguntas_abiertas": {
          "anyOf": [
            {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Open questions about the diagram. A single string is taken as a one-item list. The bpmn viewer shows them under the description.",
          "title": "Preguntas Abiertas"
        },
        "legend": {
          "anyOf": [
            {
              "additionalProperties": {
                "type": "string"
              },
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Label per colour in the bpmn viewer legend, keyed by tone (`success`, `rule2`, `gateway`, ...); a tone without a label keeps its generic Spanish one.",
          "title": "Legend"
        },
        "extensions": {
          "additionalProperties": true,
          "description": "Project annotations: every `metadata` key that starts with `x-`, kept as written (renderers ignore them). Any other unknown key under `metadata` is an error.",
          "title": "Extensions",
          "type": "object"
        }
      },
      "title": "Metadata",
      "type": "object"
    },
    "ParticipantModel": {
      "additionalProperties": false,
      "properties": {
        "id": {
          "description": "Unique participant identifier referenced by messages.",
          "title": "Id",
          "type": "string"
        },
        "kind": {
          "default": "component",
          "description": "Semantic participant kind used for styling or grouping.",
          "title": "Kind",
          "type": "string"
        },
        "atoms": {
          "description": "Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
          "items": {
            "type": "string"
          },
          "title": "Atoms",
          "type": "array"
        },
        "refs": {
          "description": "Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
          "items": {
            "pattern": "^(?:[A-Za-z0-9][A-Za-z0-9._-]*:)?[A-Za-z_][A-Za-z0-9_]*:[^\\s:]+$",
            "type": "string"
          },
          "title": "Refs",
          "type": "array"
        }
      },
      "required": [
        "id"
      ],
      "title": "ParticipantModel",
      "type": "object"
    },
    "SequenceData": {
      "additionalProperties": false,
      "properties": {
        "participants": {
          "description": "Ordered participants that appear across the sequence diagram.",
          "items": {
            "$ref": "#/$defs/ParticipantModel"
          },
          "title": "Participants",
          "type": "array"
        },
        "messages": {
          "description": "Ordered interactions exchanged between participants.",
          "items": {
            "$ref": "#/$defs/MessageModel"
          },
          "title": "Messages",
          "type": "array"
        }
      },
      "required": [
        "participants",
        "messages"
      ],
      "title": "SequenceData",
      "type": "object"
    },
    "Style": {
      "additionalProperties": false,
      "properties": {
        "theme": {
          "default": "default",
          "description": "Renderer theme name used to style the generated output.",
          "title": "Theme",
          "type": "string"
        },
        "kinds": {
          "additionalProperties": {
            "additionalProperties": true,
            "type": "object"
          },
          "description": "Style per semantic kind. Neutral keys `fill`, `stroke` (a token of the default palette such as `database-fill`, a `#rrggbb` hex used in both themes, or a `{light, dark}` pair of hex or tokens) and `icon` (a name of the palette's Lucide icon set) apply to every renderer and to graph_ui, below the notation's glyph and above the default palette. A renderer-specific block (such as `plantuml: {background, border, font}`) is read only by that renderer.",
          "title": "Kinds",
          "type": "object"
        }
      },
      "title": "Style",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "id": {
      "description": "Stable identifier for the diagram specification.",
      "title": "Id",
      "type": "string"
    },
    "title": {
      "description": "Human-readable title shown in rendered output.",
      "title": "Title",
      "type": "string"
    },
    "type": {
      "const": "sequence",
      "default": "sequence",
      "description": "Discriminator for sequence diagram specs.",
      "title": "Type",
      "type": "string"
    },
    "version": {
      "description": "Schema or document version for the specification.",
      "title": "Version",
      "type": "string"
    },
    "metadata": {
      "anyOf": [
        {
          "$ref": "#/$defs/Metadata"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Optional authorship and descriptive metadata for the spec."
    },
    "style": {
      "anyOf": [
        {
          "$ref": "#/$defs/Style"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Optional presentation hints for renderers."
    },
    "data": {
      "$ref": "#/$defs/SequenceData",
      "description": "Sequence-specific participants and messages."
    }
  },
  "required": [
    "id",
    "title",
    "version",
    "data"
  ],
  "title": "SequenceDiagram",
  "type": "object"
}

FILE:tests/visual/fixtures/spec2viz/examples/schema/class.schema.json
{
  "$defs": {
    "ClassAttribute": {
      "additionalProperties": false,
      "properties": {
        "name": {
          "pattern": "^[A-Za-z_][A-Za-z0-9_?!-]*$",
          "title": "Name",
          "type": "string"
        },
        "type": {
          "pattern": "^[A-Za-z_][A-Za-z0-9_.\\[\\], ?|<>-]*$",
          "title": "Type",
          "type": "string"
        },
        "visibility": {
          "default": "public",
          "enum": [
            "public",
            "private",
            "protected",
            "package"
          ],
          "title": "Visibility",
          "type": "string"
        },
        "static": {
          "default": false,
          "title": "Static",
          "type": "boolean"
        }
      },
      "required": [
        "name",
        "type"
      ],
      "title": "ClassAttribute",
      "type": "object"
    },
    "ClassData": {
      "additionalProperties": false,
      "properties": {
        "direction": {
          "default": "TB",
          "enum": [
            "TB",
            "LR"
          ],
          "title": "Direction",
          "type": "string"
        },
        "classes": {
          "minProperties": 1,
          "patternProperties": {
            "^[A-Za-z_][A-Za-z0-9_]*$": {
              "$ref": "#/$defs/ClassDefinition"
            }
          },
          "title": "Classes",
          "type": "object"
        },
        "relations": {
          "items": {
            "$ref": "#/$defs/ClassRelation"
          },
          "title": "Relations",
          "type": "array"
        },
        "packages": {
          "description": "Optional UML packages. When a spec declares packages, every class belongs to exactly one package (an orphan class is an error); packages nest through `contains`.",
          "patternProperties": {
            "^[A-Za-z_][A-Za-z0-9_]*$": {
              "$ref": "#/$defs/ClassPackage"
            }
          },
          "title": "Packages",
          "type": "object"
        }
      },
      "required": [
        "classes"
      ],
      "title": "ClassData",
      "type": "object"
    },
    "ClassDefinition": {
      "additionalProperties": false,
      "properties": {
        "label": {
          "anyOf": [
            {
              "minLength": 1,
              "pattern": "^[^\\r\\n{}\\\\\"]+$",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Label"
        },
        "kind": {
          "default": "class",
          "enum": [
            "class",
            "interface",
            "abstract",
            "record",
            "protocol",
            "enum"
          ],
          "title": "Kind",
          "type": "string"
        },
        "attributes": {
          "items": {
            "$ref": "#/$defs/ClassAttribute"
          },
          "title": "Attributes",
          "type": "array"
        },
        "methods": {
          "items": {
            "$ref": "#/$defs/ClassMethod"
          },
          "title": "Methods",
          "type": "array"
        },
        "atoms": {
          "description": "Optional atom ids (desk/atoms) that explain this element; the catalog shows exactly these instead of fuzzy matching.",
          "items": {
            "type": "string"
          },
          "title": "Atoms",
          "type": "array"
        },
        "refs": {
          "description": "Optional sldb document refs `Model:name` (or `store:Model:name` for a linked store) this element points at; the catalog resolves and lists them.",
          "items": {
            "pattern": "^(?:[A-Za-z0-9][A-Za-z0-9._-]*:)?[A-Za-z_][A-Za-z0-9_]*:[^\\s:]+$",
            "type": "string"
          },
          "title": "Refs",
          "type": "array"
        }
      },
      "title": "ClassDefinition",
      "type": "object"
    },
    "ClassMethod": {
      "additionalProperties": false,
      "properties": {
        "name": {
          "pattern": "^[A-Za-z_][A-Za-z0-9_?!-]*$",
          "title": "Name",
          "type": "string"
        },
        "parameters": {
          "items": {
            "$ref": "#/$defs/ClassParameter"
          },
          "title": "Parameters",
          "type": "array"
        },
        "returns": {
          "default": "void",
          "pattern": "^[A-Za-z_][A-Za-z0-9_.\\[\\], ?|<>-]*$",
          "title": "Returns",
          "type": "string"
        },
        "visibility": {
          "default": "public",
          "enum": [
            "public",
            "private",
            "protected",
            "package"
          ],
          "title": "Visibility",
          "type": "string"
        },
        "abstract": {
          "default": false,
          "title": "Abstract",
          "type": "boolean"
        },
        "static": {
          "default": false,
          "title": "Static",
          "type": "boolean"
        }
      },
      "required": [
        "name"
      ],
      "title": "ClassMethod",
      "type": "object"
    },
    "ClassPackage": {
      "additionalProperties": false,
      "description": "A UML package: groups classes and other packages (nesting at any depth).",
      "properties": {
        "label": {
          "anyOf": [
            {
              "minLength": 1,
              "pattern": "^[^\\r\\n{}\\\\\"]+$",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Label"
        },
        "kind": {
          "default": "package",
          "description": "Semantic kind of the package (a domain, a layer...); `style.kinds` styles it by this kind, with the same precedence as any element.",
          "title": "Kind",
          "type": "string"
        },
        "contains": {
          "description": "Class and package identifiers inside this package. Each class and each package has at most one parent package, without cycles.",
          "items": {
            "pattern": "^[A-Za-z_][A-Za-z0-9_]*$",
            "type": "string"
          },
          "title": "Contains",
          "type": "array"
        },
        "description": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Description"
        },
        "atoms": {
          "description": "Optional atom ids that explain this package.",
          "items": {
            "type": "string"
          },
          "title": "Atoms",
          "type": "array"
        },
        "refs": {
          "description": "Optional sldb document refs this package points at.",
          "items": {
            "pattern": "^(?:[A-Za-z0-9][A-Za-z0-9._-]*:)?[A-Za-z_][A-Za-z0-9_]*:[^\\s:]+$",
            "type": "string"
          },
          "title": "Refs",
          "type": "array"
        }
      },
      "title": "ClassPackage",
      "type": "object"
    },
    "ClassParameter": {
      "additionalProperties": false,
      "properties": {
        "name": {
          "pattern": "^[A-Za-z_][A-Za-z0-9_?!-]*$",
          "title": "Name",
          "type": "string"
        },
        "type": {
          "pattern": "^[A-Za-z_][A-Za-z0-9_.\\[\\], ?|<>-]*$",
          "title": "Type",
          "type": "string"
        }
      },
      "required": [
        "name",
        "type"
      ],
      "title": "ClassParameter",
      "type": "object"
    },
    "ClassRelation": {
      "additionalProperties": false,
      "properties": {
        "from": {
          "pattern": "^[A-Za-z_][A-Za-z0-9_]*$",
          "title": "From",
          "type": "string"
        },
        "to": {
          "pattern": "^[A-Za-z_][A-Za-z0-9_]*$",
          "title": "To",
          "type": "string"
        },
        "relation": {
          "enum": [
            "inheritance",
            "realization",
            "composition",
            "aggregation",
            "association",
            "dependency"
          ],
          "title": "Relation",
          "type": "string"
        },
        "label": {
          "anyOf": [
            {
              "minLength": 1,
              "pattern": "^[^\\r\\n{}\\\\\"]+$",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Label"
        },
        "from_multiplicity": {
          "anyOf": [
            {
              "pattern": "^(?:\\*|[0-9]+(?:\\.\\.(?:[0-9]+|\\*))?)$",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "From Multiplicity"
        },
        "to_multiplicity": {
          "anyOf": [
            {
              "pattern": "^(?:\\*|[0-9]+(?:\\.\\.(?:[0-9]+|\\*))?)$",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "To Multiplicity"
        }
      },
      "required": [
        "from",
        "to",
        "relation"
      ],
      "title": "ClassRelation",
      "type": "object"
    },
    "Metadata": {
      "properties": {
        "author": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Name of the person or team responsible for the diagram spec.",
          "title": "Author"
        },
        "description": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Free-form summary that explains the intent of the diagram.",
          "title": "Description"
        }
      },
      "title": "Metadata",
      "type": "object"
    },
    "Style": {
      "properties": {
        "theme": {
          "default": "default",
          "description": "Renderer theme name used to style the generated output.",
          "title": "Theme",
          "type": "string"
        },
        "kinds": {
          "additionalProperties": {
            "additionalProperties": true,
            "type": "object"
          },
          "description": "Style per semantic kind. Neutral keys `fill`, `stroke` (a token of the default palette such as `database-fill`, a `#rrggbb` hex used in both themes, or a `{light, dark}` pair of hex or tokens) and `icon` (a name of the palette's Lucide icon set) apply to every renderer and to graph_ui, below the notation's glyph and above the default palette. A renderer-specific block (such as `plantuml: {background, border, font}`) is read only by that renderer.",
          "title": "Kinds",
          "type": "object"
        }
      },
      "title": "Style",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "id": {
      "description": "Stable identifier for the diagram specification.",
      "title": "Id",
      "type": "string"
    },
    "title": {
      "description": "Human-readable title shown in rendered output.",
      "title": "Title",
      "type": "string"
    },
    "type": {
      "const": "class",
      "default": "class",
      "title": "Type",
      "type": "string"
    },
    "version": {
      "description": "Schema or document version for the specification.",
      "title": "Version",
      "type": "string"
    },
    "metadata": {
      "anyOf": [
        {
          "$ref": "#/$defs/Metadata"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Optional authorship and descriptive metadata for the spec."
    },
    "style": {
      "anyOf": [
        {
          "$ref": "#/$defs/Style"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Optional presentation hints for renderers."
    },
    "data": {
      "$ref": "#/$defs/ClassData"
    }
  },
  "required": [
    "id",
    "title",
    "version",
    "data"
  ],
  "title": "ClassDiagram",
  "type": "object"
}

FILE:tests/visual/test_renderers.py
"""Renderers of specIR's visual layer: `tests/test_renderers.py` of spec2viz (revision 2de1056) ported
case by case, over the same fixtures (`fixtures/spec2viz/`), loading with sldb (`load_spec`, D3) and
compiling and rendering with specIR. The parity of every renderer over the whole corpus, and the
drawing of a transition without a source state, are in `test_render_parity.py`."""

import json
import pytest
from pathlib import Path

from sldb.api.notations import load_spec as load

from specir.visual.compilers import compile_ir
from specir.visual.renderers import render
from specir.visual.renderers.plantuml import PlantUMLRenderer
from specir.visual.renderers.vega import VegaRenderer
from specir.visual.renderers.mermaid import MermaidRenderer
from specir.visual.renderers.d2 import D2Renderer
from specir.visual.renderers.antonia_html import AntoniaHtmlRenderer
from specir.visual.renderers.graph_html import GraphRenderer
from specir.visual.renderers import JsonRenderer
from specir.visual.exceptions import RenderError
from specir.visual.ir import DeploymentArtifact, DeploymentConnection, DeploymentIR, DeploymentNode, SequenceIR, MatrixIR

CORPUS = Path(__file__).resolve().parent / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"


def _ir(name):
    return compile_ir(load(FIXTURES / name))


# ── PlantUML ──────────────────────────────────────────────────────────────────


def test_sequence_puml():
    out = PlantUMLRenderer().render(_ir("sequence.create-quotation.yml"))
    assert "@startuml" in out and "@enduml" in out
    assert "actor User" in out
    assert "User -> QuotationFlow" in out


def test_state_puml():
    out = PlantUMLRenderer().render(_ir("state.quotation.yml"))
    assert "[*] --> browsing" in out
    assert "select_client" in out
    assert "all validations passed" in out


def test_component_puml():
    out = PlantUMLRenderer().render(_ir("component.quotation.yml"))
    assert "@startuml" in out
    assert "QuotationFlow" in out
    assert "skinparam component<<core>> BackgroundColor" in out
    assert 'rectangle "Store" as Store <<boundary>>' in out


def test_component_puml_uses_yaml_style_overrides():
    out = PlantUMLRenderer().render(_ir("component.styled.yml"))
    assert "skinparam component<<core>> BackgroundColor #112233" in out
    assert "skinparam component<<core>> BorderColor #445566" in out
    assert "skinparam component<<core>> FontColor #778899" in out


def test_component_puml_nests_children_without_redefining_them():
    out = PlantUMLRenderer().render(_ir("component.quotation.yml"))
    assert out.count('rectangle "Store" as Store <<boundary>>') == 1
    assert out.count('package "QuotationFlow" as QuotationFlow <<core>> {') == 1


def test_activity_puml():
    out = PlantUMLRenderer().render(_ir("activity.validation.yml"))
    assert "start" in out and "stop" in out
    assert "Load basket" in out
    assert "if (" in out


def test_activity_complex_puml():
    out = PlantUMLRenderer().render(_ir("activity.complex.yml"))
    assert out.count("if (") == 2
    assert "Load data" in out
    assert "Save result" in out
    assert "Show auth error" in out
    assert "Show data error" in out


def test_activity_complex_mermaid():
    out = MermaidRenderer().render(_ir("activity.complex.yml"))
    assert out.count("{") == 2
    assert "Load data" in out
    assert "Save result" in out
    assert "Show auth error" in out
    assert "Show data error" in out


def test_deployment_puml():
    out = PlantUMLRenderer().render(_ir("deployment.runtime.yml"))
    assert "Browser" in out
    assert "HTTPS" in out


# ── Vega ──────────────────────────────────────────────────────────────────────


def test_vega_schema():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    assert spec["$schema"].startswith("https://vega.github.io/schema/vega/")


def test_vega_data_sections():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    names = {d["name"] for d in spec["data"]}
    assert {"stages", "rows", "spans", "stageBoundaries"} <= names


def test_vega_stages():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    stages = next(d for d in spec["data"] if d["name"] == "stages")["values"]
    assert [s["id"] for s in stages] == [
        "browse",
        "client",
        "basket",
        "validation",
        "completed",
    ]


def test_vega_spans():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    spans = next(d for d in spec["data"] if d["name"] == "spans")["values"]
    qf = next(s for s in spans if s["component"] == "QuotationFlow")
    assert qf["start"] == 0 and qf["end"] == 5


def test_vega_rows():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    rows = next(d for d in spec["data"] if d["name"] == "rows")["values"]
    ids = [r["id"] for r in rows]
    assert "QuotationFlow" in ids
    depths = {r["id"]: r["depth"] for r in rows}
    assert depths["QuotationFlow"] == 0
    assert depths["BasketItem"] > depths["Basket"]


def test_vega_signals():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    names = {s["name"] for s in spec["signals"]}
    assert {"left", "top", "cellWidth", "rowHeight", "barPadding"} <= names


def test_vega_scales():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    assert any(s["name"] == "kindColor" for s in spec["scales"])


def test_vega_marks_types():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    types = {m["type"] for m in spec["marks"]}
    assert {"text", "rect", "rule"} <= types


def test_vega_rejects_wrong_ir():
    ir = _ir("sequence.create-quotation.yml")
    with pytest.raises(RenderError):
        VegaRenderer().render(ir)


def test_plantuml_rejects_matrix():
    ir = _ir("matrix.quotation-view.yml")
    with pytest.raises(RenderError):
        PlantUMLRenderer().render(ir)


def test_mermaid_rejects_matrix():
    ir = _ir("matrix.quotation-view.yml")
    with pytest.raises(RenderError):
        MermaidRenderer().render(ir)


# ── Mermaid ───────────────────────────────────────────────────────────────────


def test_mermaid_sequence():
    out = MermaidRenderer().render(_ir("sequence.create-quotation.yml"))
    assert "sequenceDiagram" in out
    assert "User" in out


def test_mermaid_state():
    out = MermaidRenderer().render(_ir("state.quotation.yml"))
    assert "stateDiagram-v2" in out
    assert "[*] --> browsing" in out


def test_mermaid_component():
    out = MermaidRenderer().render(_ir("component.quotation.yml"))
    assert "flowchart TD" in out and "layout: elk" in out
    assert "QuotationFlow" in out


def test_mermaid_activity():
    out = MermaidRenderer().render(_ir("activity.validation.yml"))
    assert "flowchart TD" in out
    assert "Load basket" in out


def test_mermaid_deployment():
    out = MermaidRenderer().render(_ir("deployment.runtime.yml"))
    assert "flowchart TD" in out and "layout: elk" in out
    assert "Browser" in out
    assert "HTTPS" in out


# ── D2 / HTML / JSON ──────────────────────────────────────────────────────────


def test_d2_sequence():
    out = D2Renderer().render(_ir("sequence.create-quotation.yml"))
    assert "direction: right" in out
    assert "User -> QuotationFlow: open quotation flow" in out


def test_d2_state():
    out = D2Renderer().render(_ir("state.quotation.yml"))
    assert "browsing -> client_selected: select_client" in out


def test_d2_component():
    out = D2Renderer().render(_ir("component.quotation.yml"))
    assert 'QuotationFlow: "QuotationFlow"' in out
    assert 'QuotationFlow.ClientSelection: "ClientSelection"' in out


def test_d2_activity():
    out = D2Renderer().render(_ir("activity.validation.yml"))
    assert "__start: Start" in out
    assert "check_validity.shape: diamond" in out
    assert "__end: End" in out


def test_d2_deployment():
    out = D2Renderer().render(_ir("deployment.runtime.yml"))
    assert 'browser.quotation_ui: "Quotation UI"' in out
    # las aristas usan la ruta del contenedor; un id suelto haria que d2 creara otro elemento
    assert 'browser.quotation_ui -> app_server.quotation_api: "HTTPS"' in out


def test_d2_and_mermaid_deployment_without_protocol():
    ir = DeploymentIR(
        title="runtime",
        nodes=[DeploymentNode(id="n1", label="N1", kind="server")],
        artifacts=[],
        connections=[DeploymentConnection(from_="a", to="b")],
    )
    assert "a -> b" in D2Renderer().render(ir)
    assert "a --> b" in MermaidRenderer().render(ir)


def test_d2_rejects_matrix():
    with pytest.raises(RenderError):
        D2Renderer().render(_ir("matrix.quotation-view.yml"))


def test_plantuml_sequence_message_condition_and_group():
    from specir.visual.ir import SequenceIR, Participant, Message
    ir = SequenceIR(
        title="Test",
        participants=[Participant(id="A"), Participant(id="B")],
        messages=[
            Message(from_="A", to="B", message="hello", condition="cond1", group="g1"),
            Message(from_="B", to="A", message="world", condition="cond2", group=None),
        ],
    )
    out = PlantUMLRenderer().render(ir)
    assert "[cond1]" in out
    assert "group g1" in out
    assert "end" in out  # group close
    assert "[cond2]" in out
    assert out.count("group g1") == 1  # group appears only once for first message


def test_plantuml_state_transition_with_action():
    from specir.visual.ir import StateIR, StateNode, Transition
    ir = StateIR(
        title="Test",
        entity="Order",
        initial="open",
        states=[StateNode(id="open", label="Open"), StateNode(id="closed", label="Closed")],
        transitions=[Transition(from_="open", to="closed", on="finish", action="doSomething")],
    )
    out = PlantUMLRenderer().render(ir)
    assert " / doSomething" in out


def test_plantuml_component_style_kinds_non_dict_plantuml():
    from specir.visual.ir import ComponentIR, ComponentNode, ComponentEdge
    ir = ComponentIR(
        title="Test",
        nodes=[ComponentNode(id="A", label="A", kind="core")],
        edges=[],
        style_kinds={"core": {"plantuml": "not a dict"}},
    )
    out = PlantUMLRenderer().render(ir)
    # Should not crash and should produce valid output
    assert "@startuml" in out


def test_plantuml_activity_broken_chain():
    from specir.visual.ir import ActivityIR, ActivityStep
    ir = ActivityIR(
        title="Test",
        start="step1",
        steps=[
            ActivityStep(id="step1", label="Step 1", kind="action", next="missing"),
        ],
        end="end",
    )
    out = PlantUMLRenderer().render(ir)
    assert "@startuml" in out
    assert "start" in out
    assert "stop" in out
    # Should not crash on missing step


def test_plantuml_activity_decision_branches():
    from specir.visual.ir import ActivityIR, ActivityStep
    ir = ActivityIR(
        title="Test",
        start="decide",
        steps=[
            ActivityStep(id="decide", label="Decide?", kind="decision", branches={"yes": "yes_step", "no": "no_step"}),
            ActivityStep(id="yes_step", label="Yes", next="end"),
            ActivityStep(id="no_step", label="No", next="end"),
        ],
        end="end",
    )
    out = PlantUMLRenderer().render(ir)
    assert "if (Decide??) then (yes)" in out or "if (Decide?) then (yes)" in out
    assert "else (no)" in out
    assert "endif" in out


def test_json_renderer_handles_model_and_plain_dict():
    model_payload = JsonRenderer().render(compile_ir(load(EXAMPLES / "reflection" / "canonical.yml")))
    plain_payload = JsonRenderer().render({"ok": True})
    assert isinstance(model_payload, dict)
    assert plain_payload == {"ok": True}


def test_graph_html_renderer_is_standalone_and_depth_aware():
    out = GraphRenderer().render(_ir("component.quotation.yml"))
    assert "Hierarchical Tree" in out
    assert "https://d3js.org" not in out
    assert 'data-depth="${depth}"' in out
    assert "const totalNodes = Object.keys(NODES).length;" in out
    assert "const DEFAULT_EXPANDED_DEPTH = 2;" in out


def test_graph_html_renderer_rejects_wrong_ir():
    with pytest.raises(RenderError):
        GraphRenderer().render(_ir("sequence.create-quotation.yml"))


# ── Mermaid linter ─────────────────────────────────────────────────


def test_mermaid_return_arrow_is_valid_and_lints_clean():
    from specir.visual.lint_mermaid import lint_mermaid

    out = MermaidRenderer().render(_ir("sequence.create-quotation.yml"))
    assert "<<--" not in out  # invalid mermaid must never be emitted
    assert lint_mermaid(out) == []


def test_linter_flags_invalid_return_arrow():
    from specir.visual.lint_mermaid import lint_mermaid

    bad = "sequenceDiagram\n    A<<--B: reply"
    problems = lint_mermaid(bad)
    assert any("<<--" in p or "invalid sequence arrow" in p for p in problems)


def test_linter_flags_raw_angle_brackets():
    from specir.visual.lint_mermaid import lint_mermaid

    bad = "sequenceDiagram\n    A->>B: GET path?x=<id>"
    assert lint_mermaid(bad, check_html=True)
    assert lint_mermaid(bad, check_html=False) == []


def test_render_to_file_sanitizes_mermaid_messages(tmp_path):
    from specir.visual.render_file import render_to_file

    spec = tmp_path / "s.yml"
    spec.write_text(
        'id: s\ntitle: S\ntype: sequence\nversion: "0.1"\n'
        "data:\n  participants:\n    - id: A\n      kind: actor\n"
        "    - id: B\n      kind: component\n"
        "  messages:\n    - from: A\n      to: B\n      message: get <id> now\n"
    )
    out = render_to_file(spec, out=tmp_path, renderer="mermaid")
    text = out.read_text(encoding="utf-8")
    assert "#lt;id#gt;" in text


# ── Dispatch ──────────────────────────────────────────────────────────────────


def test_render_dispatch_plantuml():
    out = render(_ir("sequence.create-quotation.yml"))
    assert isinstance(out, str) and "@startuml" in out


def test_render_dispatch_vega():
    out = render(_ir("matrix.quotation-view.yml"))
    assert isinstance(out, dict) and "$schema" in out


def test_render_dispatch_override():
    out = render(_ir("sequence.create-quotation.yml"), renderer="mermaid")
    assert "sequenceDiagram" in out


def test_render_dispatch_unknown_renderer():
    with pytest.raises(RenderError):
        render(_ir("sequence.create-quotation.yml"), renderer="nope")


def test_render_dispatch_without_default_renderer():
    class UnknownIR:
        pass

    with pytest.raises(RenderError):
        render(UnknownIR())


def test_antonia_html_escapes_mermaid_source():
    """Stereotypes like <<record>> must survive the HTML parser.

    Unescaped, the browser reads `<<record>>` as a bogus tag and drops it,
    so mermaid receives `<>` from the DOM and renders a syntax error.
    """
    ir = compile_ir(load(EXAMPLES / "class" / "runtime.yml"))
    raw = MermaidRenderer().render(ir)
    assert "<<record>>" in raw

    html_out = AntoniaHtmlRenderer().render(ir)
    assert "&lt;&lt;record&gt;&gt;" in html_out
    assert "<<record>>" not in html_out


def test_antonia_html_source_survives_the_dom():
    """What the browser exposes as textContent must equal the mermaid source."""
    from html.parser import HTMLParser

    class PreText(HTMLParser):
        def __init__(self):
            super().__init__()
            self.inside = False
            self.text = []

        def handle_starttag(self, tag, attrs):
            if tag == "pre" and dict(attrs).get("class") == "mermaid":
                self.inside = True

        def handle_endtag(self, tag):
            if tag == "pre":
                self.inside = False

        def handle_data(self, data):
            if self.inside:
                self.text.append(data)

    ir = compile_ir(load(EXAMPLES / "class" / "runtime.yml"))
    expected = MermaidRenderer().render(ir)

    parser = PreText()
    parser.feed(AntoniaHtmlRenderer().render(ir))
    assert "".join(parser.text).strip() == expected.strip()


def test_sequence_consecutive_group_renders_as_one_block():
    from specir.visual.ir import Participant, Message
    ir = SequenceIR(
        title="Test",
        participants=[Participant(id="A"), Participant(id="B"), Participant(id="C")],
        messages=[
            Message(from_="A", to="B", message="one", group="g"),
            Message(from_="A", to="C", message="two", group="g"),
            Message(from_="B", to="C", message="three", condition="c"),
        ],
    )
    puml = PlantUMLRenderer().render(ir)
    assert puml.count("group g") == 1
    assert puml.count("\nend") == 1
    mmd = MermaidRenderer().render(ir)
    assert mmd.count("rect ") == 1
    assert "Note over A,B: g" in mmd
    assert mmd.count("    end") == 1
    assert "three [c]" in mmd


def test_mermaid_sequence_escapes_semicolon():
    from specir.visual.ir import Participant, Message
    ir = SequenceIR(
        title="Test",
        participants=[Participant(id="A"), Participant(id="B")],
        messages=[Message(from_="A", to="B", message="uno; dos")],
    )
    out = MermaidRenderer().render(ir)
    assert "uno#59; dos" in out


def test_mermaid_flowcharts_select_elk_with_orthogonal_curves():
    out = MermaidRenderer().render(_ir("deployment.runtime.yml"))
    assert out.startswith("---\nconfig:\n  layout: elk\n  flowchart:\n    curve: linear\n---\nflowchart TD\n")


def test_catalog_template_registers_the_elk_layout():
    from importlib.resources import files

    html = files("specir.visual").joinpath("templates", "default.html").read_text(encoding="utf-8")
    assert "mermaid.registerLayoutLoaders(elkLayouts)" in html and "layout-elk@0.2.3" in html
    assert "layout: 'elk'" in html and "curve: 'linear'" in html and "curve: 'basis'" not in html
    # el inicializador corre en DOMContentLoaded, despues de los modulos que cargan mermaid
    assert html.index("function initMermaid()") < html.index("initMermaid();\n      await mermaid.run")


def test_component_mermaid_click_desde_href(tmp_path):
    spec = tmp_path / "links.yml"
    spec.write_text(
        "id: component.links\ntitle: Links\ntype: component\nversion: '1'\n"
        "metadata: {author: t, description: d}\n"
        "data:\n  nodes:\n    a: {label: A, href: /wiki/a/}\n    b: {label: B}\n"
    )
    out = MermaidRenderer().render(compile_ir(load(spec)))
    assert 'click a href "/wiki/a/"' in out
    assert "click b" not in out

FILE:tests/visual/test_render_parity.py
"""Parity of specIR's renderers with spec2viz's (IR12), and how they draw what spec2viz never drew.

- Every spec of the corpus that validates, drawn by each of the nine values of spec2viz's renderer
  selector, gives what spec2viz gave (`render_parity`): the same text, the same JSON or the same
  error class and message, and the same offline BPMN viewer page. Against the saved goldens always,
  and against spec2viz live when it is installed (`parity` marker). The only order compared as a
  mapping is the kind color scale of `vega`, which spec2viz listed in set order (declared in the
  coverage matrix, SV-C05).
- The selector of specIR has the nine values of spec2viz, with the same extensions and the same
  default renderer per intermediate representation.
- A transition whose source state is not named (`ANY_STATE`, the state projection of IR11) leaves one
  dashed pseudostate labelled `*` in mermaid, plantuml and d2; it is never the initial state, and a
  state IR without an initial state draws no initial arrow."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "models"))  # blog.py, for conftest's blog fixtures

import render_parity  # noqa: E402

from specir.visual.ir import ANY_STATE, StateIR, StateNode, Transition  # noqa: E402
from specir.visual.lint_mermaid import lint_mermaid  # noqa: E402
from specir.visual.renderers import DEFAULT_RENDERER, EXT_MAP, RENDERER_MAP, render  # noqa: E402
from specir.visual.renderers.mermaid import ANY_STATE_ID  # noqa: E402

GOLDENS = render_parity.goldens()


def test_goldens_cover_every_valid_spec_and_every_renderer():
    assert sorted(GOLDENS) == render_parity.VALID and len(GOLDENS) == 36
    for rel, outcome in GOLDENS.items():
        assert set(render_parity.RENDERERS) <= set(outcome), rel
    drawn = {r for outcome in GOLDENS.values() for r in render_parity.RENDERERS if "out" in outcome[r]}
    assert drawn == set(render_parity.RENDERERS), "every renderer draws some spec of the corpus"
    assert any("bpmn.html" in outcome for outcome in GOLDENS.values())


@pytest.mark.parametrize("rel", render_parity.VALID)
def test_specir_renders_what_the_goldens_say(rel):
    assert render_parity.comparable(render_parity.specir_renders(rel)) == render_parity.comparable(GOLDENS[rel])


@pytest.mark.parity
@pytest.mark.parametrize("rel", render_parity.VALID)
def test_specir_renders_what_spec2viz_renders(rel):
    pytest.importorskip("spec2viz")
    assert render_parity.comparable(render_parity.specir_renders(rel)) == render_parity.comparable(render_parity.spec2viz_renders(rel))


@pytest.mark.parity
def test_goldens_are_spec2viz_last_run():
    pytest.importorskip("spec2viz")
    for rel in render_parity.VALID:
        assert render_parity.comparable(render_parity.spec2viz_renders(rel)) == render_parity.comparable(GOLDENS[rel]), rel


def test_vega_lists_the_kinds_in_order_of_first_appearance():
    from sldb.api.notations import load_spec

    from specir.visual.compilers import compile_ir

    ir = compile_ir(load_spec(render_parity.parity.FIXTURES / "examples" / "matrix" / "example.yml"))
    scale = next(s for s in render(ir, "vega")["scales"] if s["name"] == "kindColor")
    assert scale["domain"] == list(dict.fromkeys(span.kind for span in ir.spans))


def test_the_selector_has_the_nine_values_of_spec2viz():
    from specir.visual.commands import DIAGRAM_RENDERERS

    assert tuple(DIAGRAM_RENDERERS) == render_parity.RENDERERS
    assert set(RENDERER_MAP) == set(EXT_MAP) == set(render_parity.RENDERERS)


@pytest.mark.parity
def test_selector_extensions_and_defaults_are_spec2viz():
    pytest.importorskip("spec2viz")
    values, extensions, defaults = render_parity.spec2viz_selector()
    assert values == list(render_parity.RENDERERS)
    assert EXT_MAP == extensions
    assert {k.__name__: v for k, v in DEFAULT_RENDERER.items()} == defaults


# ── a transition without a source state (ANY_STATE) ──────────────────────────────────────────────


def _any_state_ir(initial: str = "draft") -> StateIR:
    return StateIR(
        title="Post", entity="Post", initial=initial,
        states=[StateNode(id="draft", label="Draft"), StateNode(id="published", label="Published")],
        transitions=[Transition(from_=ANY_STATE, to="published", on="PublishPost"), Transition(from_="published", to="draft", on="Unpublish")],
    )


def test_mermaid_draws_any_state_as_one_dashed_pseudostate():
    out = render(_any_state_ir(), "mermaid")
    lines = [l.strip() for l in out.splitlines()]
    assert f'state "*" as {ANY_STATE_ID}' in lines and f"class {ANY_STATE_ID} anyState" in lines
    assert any(l.startswith("classDef anyState") and "stroke-dasharray" in l for l in lines)
    assert f"{ANY_STATE_ID} --> published : PublishPost" in lines and "published --> draft : Unpublish" in lines
    assert "[*] --> draft" in lines and not any(l.startswith("* ") for l in lines)
    assert lint_mermaid(out) == []


def test_plantuml_and_d2_draw_any_state_as_one_dashed_pseudostate():
    puml = render(_any_state_ir(), "plantuml").splitlines()
    assert f'state "*" as {ANY_STATE_ID} ##[dashed]' in puml and f"{ANY_STATE_ID} --> published : PublishPost" in puml
    assert "[*] --> draft" in puml and "published --> draft : Unpublish" in puml
    d2 = render(_any_state_ir(), "d2").splitlines()
    assert f'{ANY_STATE_ID}: "*" {{style.stroke-dash: 3}}' in d2 and f"{ANY_STATE_ID} -> published: PublishPost" in d2


def test_without_any_state_or_initial_nothing_extra_is_drawn():
    ir = _any_state_ir(initial="")
    ir.transitions = [Transition(from_="draft", to="published", on="PublishPost")]
    for name in ("mermaid", "plantuml", "d2"):
        out = render(ir, name)
        assert ANY_STATE_ID not in out and "[*]" not in out, name


def test_the_projected_states_of_the_blog_render(blog, blog_root: Path):
    """The state projection of IR11 over the blog of IR06 (ViewDoc:post-states) draws in every state
    renderer, with PublishPost leaving the `*` pseudostate."""
    from specir.visual import state_from_view

    ir = state_from_view(blog_root / ".sldb", "ViewDoc:post-states")
    assert [t.from_ for t in ir.transitions] == [ANY_STATE]
    mermaid = render(ir, "mermaid")
    assert f"{ANY_STATE_ID} --> post-published : PublishPost" in mermaid and "[*] --> post-draft" in mermaid
    assert lint_mermaid(mermaid) == []
    assert f"{ANY_STATE_ID} --> post-published : PublishPost" in render(ir, "plantuml")
    assert f"{ANY_STATE_ID} -> post-published: PublishPost" in render(ir, "d2")
    assert "PublishPost" in render(ir, "antonia-html")

FILE:tests/visual/test_render_cases.py
"""The render cases of spec2viz (revision 2de1056) that live outside `tests/test_renderers.py`, ported to
specIR over the same fixtures (`fixtures/spec2viz/`):

- `tests/test_class_diagram.py` and `tests/test_class_packages.py`: the cases that render (SV-B03,
  SV-C13). Their validation cases are D3's (sldb) and their sync case is D1's.
- `tests/test_activity_lanes.py` and `tests/test_deployment_nested.py`: the cases that render
  (SV-C02 to SV-C04, SV-C11). Their validation and sync cases are sldb's (D3, D1).
- `tests/test_catalog_resolved_views.py`: the four `view_to_mermaid` cases (SV-C14), over the view
  that sldb resolves (`sldb.api.notations.resolve_view`) from a spec synced with sldb's `SpecSync`
  into a fresh store. Its `catalog build` cases are IR13b's.
- `tests/test_exceptions.py`: the asserts on `Spec2VizError`, `CompileError` and `RenderError`
  (SV-A14). Those on `ParseError` and `ValidationError` are D3's.

The cases that need the real mermaid engine (mmdc) skip when it is not installed, as in spec2viz."""

from __future__ import annotations

import html as _html
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from sldb.api.notations import load_spec as load
from sldb.api.notations import validate_spec as validate

from specir.visual.compilers import compile_ir
from specir.visual.exceptions import CompileError, RenderError, Spec2VizError
from specir.visual.ir import ClassIR
from specir.visual.lint_mermaid import MermaidLintError, lint_mermaid, mmdc_path
from specir.visual.renderers import render
from specir.visual.renderers.antonia_html import AntoniaHtmlRenderer
from specir.visual.renderers.class_diagram import render_mermaid_class, render_plantuml_class
from specir.visual.renderers.d2 import D2Renderer
from specir.visual.renderers.mermaid import MermaidRenderer
from specir.visual.renderers.plantuml import PlantUMLRenderer
from specir.visual.renderers.view_mermaid import view_to_mermaid
from specir.visual.spec_models import ClassDiagram

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_parity  # noqa: E402

CORPUS = Path(__file__).resolve().parent / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLE = CORPUS / "examples" / "class" / "runtime.yml"
PACKAGES = FIXTURES / "class.packages.yml"
LANES = FIXTURES / "activity.lanes.yml"
NESTED = FIXTURES / "deployment.nested.yml"
requires_mmdc = pytest.mark.skipif(mmdc_path() is None, reason="mmdc (mermaid-cli) not installed")


def _valid_ir(path: Path):
    diagram = load(path)
    validate(diagram)
    return compile_ir(diagram)


# ── tests/test_class_diagram.py ─────────────────────────────────────────────────────────────────


def test_schema_and_compiler_preserve_structured_signatures():
    from specir.visual.schema import json_schema

    ir = _valid_ir(EXAMPLE)
    assert isinstance(ir, ClassIR)
    method = ir.classes[0].methods[0]
    assert method.name == "execute"
    assert [(p.name, p.type) for p in method.parameters] == [("context", "ExecutionContext"), ("input", "PortValues")]
    assert method.returns == "ExecutionResult"
    assert ir.classes[1].attributes[0].visibility == "private"
    assert ir.relations[1].to_multiplicity == "1"
    schema = json_schema("class")
    assert schema["properties"]["type"]["const"] == "class"
    assert schema["$defs"]["ClassMethod"]["additionalProperties"] is False
    assert "class" in json_schema()["discriminator"]["mapping"]


def test_backends_preserve_realization_direction_and_generic_types():
    ir = compile_ir(load(EXAMPLE))
    mermaid = render(ir)
    plantuml = render(ir, "plantuml")
    assert mermaid.startswith("classDiagram")
    assert "DataNode ..|> ExecutableNode" in mermaid
    assert "DataNode ..|> ExecutableNode" in plantuml
    assert "+List~InputPort~ inputs" in mermaid
    assert "+inputs: List<InputPort>" in plantuml
    assert "+execute(context: ExecutionContext, input: PortValues)* ExecutionResult" in mermaid
    assert "{abstract} +execute(context: ExecutionContext, input: PortValues): ExecutionResult" in plantuml


def test_cli_schema_validate_and_render(tmp_path, monkeypatch):
    """`test_cli_schema_validate_render_and_catalog` without its `catalog build` step (IR13b)."""
    from click.testing import CliRunner

    from specir.visual.commands import main

    monkeypatch.setenv("SPECIR_MMDC", "0")
    runner = CliRunner()
    for args in [
        ["diagram", "schema", "--type", "class", "--out", str(tmp_path / "class.schema.json")],
        ["diagram", "validate", str(EXAMPLE)],
        ["diagram", "render", str(EXAMPLE), "--out", str(tmp_path)],
        ["diagram", "render", str(EXAMPLE), "--backend", "plantuml", "--out", str(tmp_path)],
    ]:
        result = runner.invoke(main, args)
        assert result.exit_code == 0, result.output
    assert (tmp_path / "runtime.mmd").exists()
    assert (tmp_path / "runtime.puml").exists()


@requires_mmdc
def test_real_mermaid_engine_accepts_members_kinds_and_all_relations():
    data = yaml.safe_load(EXAMPLE.read_text())
    data["data"]["classes"]["DataNode"]["attributes"].append(
        {"name": "instances", "type": "Integer", "static": True, "visibility": "protected"})
    data["data"]["classes"]["DataNode"]["methods"].append(
        {"name": "create", "static": True, "returns": "DataNode", "visibility": "package"})
    for kind in ["class", "interface", "abstract", "record", "protocol", "enum"]:
        data["data"]["classes"][f"Kind_{kind}"] = {"kind": kind}
    for relation in ["inheritance", "composition", "aggregation", "association", "dependency"]:
        edge = {"from": "DataNode", "to": "NodeSpec", "relation": relation, "label": "contract & data"}
        if relation != "inheritance":
            edge.update(from_multiplicity="1", to_multiplicity="0..*")
        data["data"]["relations"].append(edge)
    diagram = ClassDiagram.model_validate(data)
    validate(diagram)
    assert lint_mermaid(render(compile_ir(diagram))) == []


# ── tests/test_class_packages.py ────────────────────────────────────────────────────────────────


def test_mermaid_namespaces_by_path_and_colors_classes_by_package_kind():
    out = render_mermaid_class(_valid_ir(PACKAGES))
    lines = [l.strip() for l in out.splitlines()]
    assert "namespace Core.Billing {" in lines and "namespace Core.Identity {" in lines and "namespace Shared {" in lines
    assert "namespace Core {" not in lines  # sin clases propias, el paquete raiz no abre namespace vacio
    assert "classDef pkg0 fill:#fff1c2,stroke:#7a5c00" in lines and 'cssClass "Invoice,Payment" pkg0' in lines
    assert "classDef pkg1 fill:#dbebf4,stroke:#0072b2" in lines and 'cssClass "User" pkg1' in lines
    assert not any("AuditLog" in l for l in lines if l.startswith("cssClass"))


def test_plantuml_nests_packages_with_their_fill():
    out = render_plantuml_class(_valid_ir(PACKAGES))
    assert 'package "Core" as core {\n    package "Billing" as billing #fff1c2 {\n        class "Invoice" as Invoice {' in out
    assert 'package "Shared" as shared {' in out


def test_without_packages_the_output_is_unchanged():
    diagram = load(PACKAGES)
    diagram.data.packages = {}
    diagram.style = None
    out = render_mermaid_class(compile_ir(diagram))
    assert "namespace" not in out and "classDef" not in out


@pytest.mark.skipif(shutil.which("mmdc") is None, reason="mmdc not installed")
def test_real_mermaid_engine_accepts_the_packages(tmp_path):
    source = tmp_path / "p.mmd"
    source.write_text(render_mermaid_class(_valid_ir(PACKAGES)), encoding="utf-8")
    result = subprocess.run(["mmdc", "-i", str(source), "-o", str(tmp_path / "p.svg"), "-q"], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr[-400:]


# ── tests/test_activity_lanes.py ────────────────────────────────────────────────────────────────


def test_mermaid_draws_one_lane_per_partition_merge_as_diamond_and_notes():
    out = MermaidRenderer().render(_valid_ir(LANES))
    lanes = [l.strip() for l in out.splitlines() if l.strip().startswith("subgraph")]
    assert lanes == ['subgraph __lane0 ["Dev"]', 'subgraph __lane1 ["Approver"]', 'subgraph __lane2 ["Script"]', 'subgraph __lane3 ["AWS"]']
    assert 'joined{" "}' in out and 'review{"Approve?"}' in out
    assert 'review__note["Two approvals for production"]:::note' in out and "review -.- review__note" in out
    assert "classDef note" in out


def test_mermaid_without_the_new_fields_is_unchanged():
    out = MermaidRenderer().render(_valid_ir(FIXTURES / "activity.validation.yml"))
    assert "subgraph" not in out and "note" not in out
    assert out.splitlines()[:8] == ["---", "config:", "  layout: elk", "  flowchart:", "    curve: linear", "---", "flowchart TD", "    __start([Start])"]


def test_plantuml_swimlanes_and_note():
    out = PlantUMLRenderer().render(_valid_ir(LANES))
    lines = out.splitlines()
    assert lines[:3] == ["@startuml", "|Dev|", "start"]
    assert "|Approver|" in lines and "note right: Two approvals for production" not in lines  # la nota es de una decision
    assert "|Script|" in lines


def test_plantuml_note_on_an_action():
    diagram = load(LANES)
    diagram.data.steps["deploy"].notes = "Blue/green"
    out = PlantUMLRenderer().render(compile_ir(diagram))
    assert ":Deploy;\nnote right: Blue/green" in out


def test_d2_lanes_are_containers_and_edges_use_qualified_ids():
    out = D2Renderer().render(_valid_ir(LANES))
    assert '__lane0: "Dev"' in out and '__lane0.open_pr: "Open pull request"' in out
    assert "__lane2.joined.shape: diamond" in out and "__lane0.open_pr -> __lane1.review" in out
    assert "__lane1.review__note.shape: page" in out


# ── tests/test_deployment_nested.py ─────────────────────────────────────────────────────────────


def test_mermaid_nests_subgraphs_and_marks_deploy_and_manifest():
    out = MermaidRenderer().render(_valid_ir(NESTED))
    lines = out.splitlines()
    order = [l.strip() for l in lines if l.strip().startswith("subgraph")]
    assert order == ['subgraph vpc ["VPC"]', 'subgraph subnet ["Private subnet"]', 'subgraph cluster ["ECS cluster"]', 'subgraph db ["Postgres"]', 'subgraph edge ["CDN"]']
    assert '            subgraph cluster ["ECS cluster"]' in lines and '                api_service["api service"]' in lines
    assert '    cluster -->|"queries · :5432"| db' in lines and '    edge -->|"HTTPS"| cluster' in lines
    assert '    api_image -.->|"«deploy»"| cluster' in lines and '    api_image -.->|"«manifest»"| api_service' in lines


def test_plantuml_and_d2_nest_and_d2_edges_use_container_paths():
    puml = PlantUMLRenderer().render(_valid_ir(NESTED))
    assert 'node "VPC" as vpc {\n  node "Private subnet" as subnet {\n    node "ECS cluster" as cluster {' in puml
    assert "api_image ..> cluster : «deploy»" in puml
    d2 = D2Renderer().render(_valid_ir(NESTED))
    assert 'vpc.subnet.cluster.api_service: "api service"' in d2
    assert 'edge -> vpc.subnet.cluster: "HTTPS"' in d2 and "api_image -> vpc.subnet.cluster: \"«deploy»\" {style.stroke-dash: 3}" in d2


def test_antonia_html_draws_every_connection_of_a_deployment():
    ir = _valid_ir(NESTED)
    page = AntoniaHtmlRenderer().render(ir)
    source = _html.unescape(re.search(r'<pre class="mermaid">(.*?)</pre>', page, re.S).group(1))
    expected = MermaidRenderer().render(ir)
    assert source.strip() == expected.strip()
    arrows = [l for l in source.splitlines() if re.search(r"\s(-->|-\.->)", l)]
    connections = yaml.safe_load(NESTED.read_text(encoding="utf-8"))["data"]["connections"]
    assert len(arrows) == len(connections) > 0


# ── tests/test_catalog_resolved_views.py (view_to_mermaid) ──────────────────────────────────────

NOTATION = {
    "name": "infra-own", "title": "Infra", "diagram_type": "deployment", "layout": {"kind": "graph", "direction": "LR"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "keyword": "«{kind}»", "fill": {"light": "#fff1c2", "dark": "#3d3200"}},
        {"id": "node", "model": "SpecNodeDoc", "where": 'collection = "nodes"', "shape": "node-box", "keyword": "«node»"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [
        {"id": "contains", "relation": "contains", "draw": "nest"},
        {"id": "deploy", "relation": "deploy", "line": "dashed", "label": "«deploy»"},
        {"id": "any", "relation": "*", "color": "#0072b2", "target_end": "none", "label": "{data.protocol}"},
    ],
}


def resolved_view(tmp_path: Path, spec: Path = NESTED, notation: Path | None = None) -> dict:
    """The view sldb resolves for `spec` once sldb's SpecSync wrote it into a fresh store."""
    import sldb.api as sldb_api
    from sldb.api.notations import SpecSync, resolve_view

    root = tmp_path / "scratch"
    sldb_api.init_store(root)
    (root / "docs").mkdir()
    copy = Path(shutil.copy(spec, root / "docs" / spec.name))
    report = SpecSync(root / ".sldb").sync(copy, notation=notation)
    return resolve_view(root / ".sldb", report.spec_id)


def _notation(tmp_path: Path) -> Path:
    path = tmp_path / "infra-own.yml"
    path.write_text(yaml.safe_dump(NOTATION, allow_unicode=True), encoding="utf-8")
    return path


def test_view_to_mermaid_uses_glyph_shape_keyword_style_nesting_and_links(tmp_path):
    out = view_to_mermaid(resolved_view(tmp_path, notation=_notation(tmp_path)), theme="dark")
    lines = [l.strip() for l in out.splitlines()]
    assert out.startswith("---\nconfig:\n  layout: elk\n") and "flowchart LR" in lines
    assert any(l.startswith("subgraph ") and "«node»<br/>VPC" in l for l in lines)
    assert any('[("«database»<br/>Postgres")]' in l for l in lines)
    assert any(l.startswith("style ") and "fill:#3d3200" in l and "color:#e6edf3" in l for l in lines)
    assert any(l.startswith("linkStyle ") and "stroke:#0072b2" in l for l in lines)
    assert any("-.->|\"«deploy»\"|" in l for l in lines) and any("---|\"HTTPS\"|" in l for l in lines)


def test_view_to_mermaid_compartments_and_pseudonodes(tmp_path):
    klass = view_to_mermaid(resolved_view(tmp_path, PACKAGES))
    assert "<hr/>id: int<br/>total: Decimal" in klass and "@{ shape: notch-rect" not in klass
    act = view_to_mermaid(resolved_view(tmp_path / "a", LANES))
    assert "@{ shape: sm-circ }" in act and "@{ shape: fr-circ }" in act and '{" "}' in act


def test_view_to_mermaid_refuses_non_graph_layouts(tmp_path):
    view = resolved_view(tmp_path, CORPUS / "docs" / "architecture" / "spec2viz" / "sequence-sync-pipeline.yml")
    with pytest.raises(ValueError, match="not a graph"):
        view_to_mermaid(view)


@requires_mmdc
def test_view_to_mermaid_is_accepted_by_the_real_engine(tmp_path):
    for name, spec in (("dep", NESTED), ("cls", PACKAGES), ("act", LANES)):
        source = tmp_path / f"{name}.mmd"
        source.write_text(view_to_mermaid(resolved_view(tmp_path / name, spec, _notation(tmp_path) if name == "dep" else None)), encoding="utf-8")
        result = subprocess.run(["mmdc", "-i", str(source), "-o", str(tmp_path / f"{name}.svg"), "-q"], capture_output=True, text=True, timeout=120)
        assert result.returncode == 0, (name, result.stderr[-300:])


@pytest.mark.parity
@pytest.mark.parametrize("spec, own_notation", [(NESTED, True), (NESTED, False), (PACKAGES, False), (LANES, False)])
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_view_to_mermaid_matches_spec2viz_on_the_same_resolved_view(tmp_path, spec, own_notation, theme):
    pytest.importorskip("spec2viz")
    view = resolved_view(tmp_path, spec, _notation(tmp_path) if own_notation else None)
    assert view_to_mermaid(view, theme=theme) == render_parity.spec2viz_view_to_mermaid(view, theme)


# ── tests/test_exceptions.py (the visual layer's errors) ────────────────────────────────────────


def test_exception_hierarchy():
    assert issubclass(CompileError, Spec2VizError)
    assert issubclass(RenderError, Spec2VizError)
    assert issubclass(MermaidLintError, RenderError)


def test_exceptions_are_catchable_as_base():
    with pytest.raises(Spec2VizError):
        raise RenderError("cannot render")

FILE:tests/visual/test_render_commands.py
"""Rendering through the API and the commands (SV-C01, SV-C04, SV-C05, SV-C10 to SV-C12, SV-C15).

Ported from spec2viz (revision 2de1056), over the same fixtures (`fixtures/spec2viz/`):

- `tests/test_api.py`: `test_render_str`, `test_render_dict`, `test_render_mermaid_override` and the
  seven `test_render_to_file_*` (on `specir.visual.render_file.render_to_file`).
- `tests/test_cli.py`: every `test_render_*` (on `diagram render`, the command the top-level alias of
  IR13d calls) and `test_rendered_text_projections_carry_a_provenance_header`, whose header now names
  specIR's command (`specir diagram validate`).
- `tests/test_rendering_bug.py`: `test_direct_render_to_file`."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner
from sldb.api.notations import load_spec as load

from specir.visual.commands import main
from specir.visual.compilers import compile_ir
from specir.visual.render_file import provenance_header, render_to_file
from specir.visual.renderers import render

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_parity  # noqa: E402

CORPUS = Path(__file__).resolve().parent / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"
runner = CliRunner()


# ── tests/test_api.py ───────────────────────────────────────────────────────────────────────────


def test_render_str():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert "@startuml" in render(ir)


def test_render_dict():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    assert isinstance(render(ir), dict)


def test_render_mermaid_override():
    ir = compile_ir(load(FIXTURES / "state.quotation.yml"))
    assert "stateDiagram-v2" in render(ir, renderer="mermaid")


def test_render_to_file_puml(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "@startuml" in p.read_text()


def test_render_to_file_vega(tmp_path):
    p = render_to_file(FIXTURES / "matrix.quotation-view.yml", out=tmp_path)
    assert p.name.endswith(".vega.json")
    assert "$schema" in json.loads(p.read_text())


def test_render_to_file_state(tmp_path):
    p = render_to_file(FIXTURES / "state.quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "[*] --> browsing" in p.read_text()


def test_render_to_file_activity(tmp_path):
    p = render_to_file(FIXTURES / "activity.validation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "start" in p.read_text()


def test_render_to_file_deployment(tmp_path):
    p = render_to_file(FIXTURES / "deployment.runtime.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "Browser" in p.read_text()


def test_render_to_file_component(tmp_path):
    p = render_to_file(FIXTURES / "component.quotation.yml", out=tmp_path)
    assert p.name.endswith(".graph.html")
    assert "QuotationFlow" in p.read_text()


def test_render_to_file_override(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path, renderer="mermaid")
    assert p.suffix == ".mmd"
    assert "sequenceDiagram" in p.read_text()


# ── tests/test_cli.py ───────────────────────────────────────────────────────────────────────────


def _render(*args: str):
    return runner.invoke(main, ["diagram", "render", *args])


def test_render_sequence(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()


def test_render_matrix(tmp_path):
    r = _render(str(FIXTURES / "matrix.quotation-view.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "matrix.quotation-view.vega.json").exists()


def test_render_state(tmp_path):
    r = _render(str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_activity(tmp_path):
    r = _render(str(FIXTURES / "activity.validation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "activity.validation.puml").exists()


def test_render_deployment(tmp_path):
    r = _render(str(FIXTURES / "deployment.runtime.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "deployment.runtime.puml").exists()


def test_render_component(tmp_path):
    r = _render(str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.graph.html").exists()


def test_render_override(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.mmd").exists()


def test_render_backend_alias(tmp_path):
    r = _render(str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path), "--backend", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.mmd").exists()


def test_render_multiple(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_invalid_fails(tmp_path):
    r = _render(str(FIXTURES / "invalid" / "unknown_node.yml"), "--out", str(tmp_path))
    assert r.exit_code != 0
    assert r.output.startswith("Error: ")


def test_render_help_lists_the_renderers():
    """The renderer part of `test_help_mentions_taxonomy_groups_and_renderers` (the rest is IR13d's)."""
    r = runner.invoke(main, ["diagram", "render", "--help"])
    assert r.exit_code == 0
    for name in ["plantuml", "mermaid", "vega", "d2", "antonia-html", "json"]:
        assert name in r.output
    r = runner.invoke(main, ["diagram", "--help"])
    assert r.exit_code == 0
    assert "render" in r.output and "validate" in r.output and "schema" in r.output and "lint" in r.output


def test_render_d2(tmp_path):
    r = _render(str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path), "--renderer", "d2")
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.d2").exists()


def test_render_antonia_html(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "antonia-html")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.html").exists()


def test_render_json_reflection_artifact(tmp_path):
    r = _render(str(EXAMPLES / "reflection" / "canonical.yml"), "--out", str(tmp_path), "--renderer", "json")
    assert r.exit_code == 0
    assert (tmp_path / "canonical.artifact.json").exists()


def test_rendered_text_projections_carry_a_provenance_header(tmp_path, monkeypatch):
    """Una proyeccion generada dice de que spec sale y como se valida; el JSON no lleva cabecera."""
    monkeypatch.chdir(CORPUS)
    spec = Path("examples/component/example.yml")
    for renderer, prefix in (("mermaid", "%%"), ("plantuml", "'"), ("d2", "#")):
        text = render_to_file(spec, out=tmp_path, renderer=renderer).read_text(encoding="utf-8")
        lines = text.splitlines()
        # en mermaid el frontmatter de config (ELK) va primero; la cabecera, justo despues
        first = lines[lines.index("---", 1) + 1] if renderer == "mermaid" else lines[0]
        assert first.startswith(f"{prefix} specir: generated from examples/component/example.yml;")
        assert "`specir diagram validate examples/component/example.yml`" in first
    assert provenance_header("vega", spec) == "" and provenance_header("json", spec) == ""
    matrix = render_to_file(Path("tests/fixtures/matrix.quotation-view.yml"), out=tmp_path, renderer="vega").read_text(encoding="utf-8")
    assert matrix.lstrip().startswith("{")


def test_the_header_names_a_command_that_validates(tmp_path, monkeypatch):
    """The command the provenance header names exists and validates the spec."""
    monkeypatch.chdir(CORPUS)
    r = runner.invoke(main, ["diagram", "validate", "examples/component/example.yml"])
    assert r.exit_code == 0 and r.output == "example.yml: OK\n"
    r = runner.invoke(main, ["diagram", "validate", "tests/fixtures/invalid/unknown_node.yml"])
    assert r.exit_code == 1 and "unknown_node.yml: ERROR: " in r.output


# ── tests/test_rendering_bug.py ─────────────────────────────────────────────────────────────────


def test_direct_render_to_file(tmp_path):
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    fixture_path = fixture_dir / "canonical.yml"
    fixture_path.write_text("""
id: canonical-arch
title: Canonical Architecture
type: component
version: "1.0"
data:
  nodes:
    core: {label: Core, kind: internal}
    api: {label: API, kind: boundary}
  edges:
    - {from: api, to: core, relation: uses}
""")
    out_dir = tmp_path / "out"
    output_path = render_to_file(fixture_path, out=out_dir, renderer="mermaid")
    assert output_path.exists()
    assert "flowchart TD" in output_path.read_text()
    assert "core" in output_path.read_text()
    assert "api" in output_path.read_text()


@pytest.mark.parity
@pytest.mark.parametrize("renderer", ["plantuml", "mermaid", "d2", "vega", "graph", "bpmn"])
def test_render_to_file_writes_what_spec2viz_writes_but_the_command_it_names(tmp_path, monkeypatch, renderer):
    """Every file spec2viz's `render_to_file` writes for a spec, specIR writes with the same bytes,
    except that the provenance header names `specir` where spec2viz named `spec2viz`."""
    pytest.importorskip("spec2viz")
    monkeypatch.chdir(CORPUS)
    monkeypatch.setenv("SPECIR_MMDC", "0")
    monkeypatch.setenv("SPEC2VIZ_MMDC", "0")
    spec = {
        "vega": "tests/fixtures/matrix.quotation-view.yml", "graph": "tests/fixtures/component.quotation.yml",
        "bpmn": "tests/fixtures/activity.mepu-decision.yml",
    }.get(renderer, "tests/fixtures/deployment.nested.yml")
    ours, theirs = tmp_path / "specir", tmp_path / "spec2viz"
    render_to_file(spec, out=ours, renderer=renderer)
    render_parity.spec2viz_render_to_file(spec, theirs, renderer)
    assert sorted(os.listdir(ours)) == sorted(os.listdir(theirs))
    for name in os.listdir(theirs):
        expected = (theirs / name).read_text(encoding="utf-8").replace("spec2viz: generated from", "specir: generated from")
        expected = expected.replace("`spec2viz diagram validate", "`specir diagram validate")
        assert (ours / name).read_text(encoding="utf-8") == expected, name

FILE:tests/visual/test_bpmn.py
"""BPMN renderer: XML structure, DI coverage and the offline bpmn-js viewer page.

`tests/test_bpmn.py` of spec2viz (revision 2de1056) ported case by case to specIR (SV-C06 to SV-C08),
over the same fixtures (`fixtures/spec2viz/`), loading with sldb (`load_spec`, D3). The two cases
that checked the activity model (`tone`, groups and detail) go through sldb's `load_spec` on a spec
file, since the model is sldb's; the CLI cases run specIR's `diagram render`."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner
from sldb.api.notations import load_spec as load

from specir.visual.commands import main
from specir.visual.compilers import compile_ir
from specir.visual.exceptions import RenderError
from specir.visual.ir import ActivityGroup, ActivityIR, ActivityStep, ComponentIR
from specir.visual.render_file import render_to_file
from specir.visual.renderers import render
from specir.visual.renderers.bpmn import BpmnRenderer, render_bpmn_html

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "spec2viz" / "tests" / "fixtures"
NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}
NODE_TAGS = ("startEvent", "endEvent", "task", "exclusiveGateway")


def _parse(xml: str) -> ET.Element:
    return ET.fromstring(xml.encode("utf-8"))


def _check_structure(root: ET.Element) -> dict[str, int]:
    """Common invariants; returns the element counts."""
    assert root.tag == f"{{{NS['bpmn']}}}definitions"
    processes = root.findall("bpmn:process", NS)
    assert len(processes) == 1
    proc = processes[0]
    nodes = {el.get("id"): el for tag in NODE_TAGS for el in proc.findall(f"bpmn:{tag}", NS)}
    flows = proc.findall("bpmn:sequenceFlow", NS)
    ids = [el.get("id") for el in proc] + [proc.get("id")]
    assert len(ids) == len(set(ids)), "ids must be unique"
    for f in flows:
        assert f.get("sourceRef") in nodes and f.get("targetRef") in nodes
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    assert plane.get("bpmnElement") == proc.get("id")
    shapes = {s.get("bpmnElement"): s for s in plane.findall("bpmndi:BPMNShape", NS)}
    edges = {e.get("bpmnElement"): e for e in plane.findall("bpmndi:BPMNEdge", NS)}
    assert set(shapes) == set(nodes), "every node has exactly one DI shape"
    assert set(edges) == {f.get("id") for f in flows}, "every flow has exactly one DI edge"
    for s in shapes.values():
        b = s.find("dc:Bounds", NS)
        assert int(b.get("width")) > 0 and int(b.get("height")) > 0
    for e in edges.values():
        pts = [(int(w.get("x")), int(w.get("y"))) for w in e.findall("di:waypoint", NS)]
        assert len(pts) >= 2
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            assert x0 == x1 or y0 == y1, "waypoints are orthogonal"
    # no two shapes overlap
    boxes = [tuple(int(s.find("dc:Bounds", NS).get(k)) for k in ("x", "y", "width", "height")) for s in shapes.values()]
    for i, (x, y, w, h) in enumerate(boxes):
        for (x2, y2, w2, h2) in boxes[i + 1:]:
            assert x + w <= x2 or x2 + w2 <= x or y + h <= y2 or y2 + h2 <= y
    return {
        **{tag: len(proc.findall(f"bpmn:{tag}", NS)) for tag in NODE_TAGS},
        "sequenceFlow": len(flows),
    }


def test_small_activity_counts():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 4, "exclusiveGateway": 1, "sequenceFlow": 7}
    proc = root.find("bpmn:process", NS)
    gw = proc.find("bpmn:exclusiveGateway", NS)
    assert gw.get("id") == "Gateway_check_validity"
    assert gw.get("name") == "Is quotation valid?"
    names = {f.get("name") for f in proc.findall("bpmn:sequenceFlow", NS) if f.get("sourceRef") == gw.get("id")}
    assert names == {"yes", "no"}


def test_mepu_decision_example_counts():
    xml = render(compile_ir(load(FIXTURES / "activity.mepu-decision.yml")), "bpmn")
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 12, "exclusiveGateway": 5, "sequenceFlow": 28}
    proc = root.find("bpmn:process", NS)
    # two branches of r5 go to the same step: two distinct flows with distinct paths
    to_peor = [f for f in proc.findall("bpmn:sequenceFlow", NS)
               if (f.get("sourceRef"), f.get("targetRef")) == ("Gateway_r5", "Task_peor")]
    assert len(to_peor) == 2
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    paths = [
        [(w.get("x"), w.get("y")) for w in plane.find(f"bpmndi:BPMNEdge[@bpmnElement='{f.get('id')}']", NS)
         .findall("di:waypoint", NS)]
        for f in to_peor
    ]
    assert paths[0] != paths[1]


def test_layout_is_deterministic_and_left_to_right():
    ir = compile_ir(load(FIXTURES / "activity.mepu-decision.yml"))
    a, b = render(ir, "bpmn"), render(ir, "bpmn")
    assert a == b
    root = _parse(a)
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    x = {s.get("bpmnElement"): int(s.find("dc:Bounds", NS).get("x")) for s in plane.findall("bpmndi:BPMNShape", NS)}
    for f in root.find("bpmn:process", NS).findall("bpmn:sequenceFlow", NS):
        assert x[f.get("sourceRef")] < x[f.get("targetRef")]


def _ir(steps, start="a", end="end"):
    return ActivityIR(title="T", start=start, steps=steps, end=end)


def test_cycles_terminal_steps_and_escaping():
    steps = [
        ActivityStep(id="a", label='Load <data> & "quote"', next="b?"),
        ActivityStep(id="b?", label="Valid?", kind="decision", branches={"retry <x>": "a", "ok": "done", "drop": "dead"}),
        ActivityStep(id="done", label="Done", next="end"),
        ActivityStep(id="dead", label="Dead end, no next"),  # terminal: flows to the end event
    ]
    xml = BpmnRenderer().render(_ir(steps))
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 3, "exclusiveGateway": 1, "sequenceFlow": 7}
    proc = root.find("bpmn:process", NS)
    assert proc.find("bpmn:task[@id='Task_a']", NS).get("name") == 'Load <data> & "quote"'
    assert proc.find("bpmn:exclusiveGateway", NS).get("id") == "Gateway_b_"
    assert "&lt;data&gt; &amp;" in xml
    ends = [f for f in proc.findall("bpmn:sequenceFlow", NS) if f.get("targetRef").startswith("EndEvent_")]
    assert {f.get("sourceRef") for f in ends} == {"Task_done", "Task_dead"}


def test_end_that_is_also_a_step_and_id_collisions():
    steps = [
        ActivityStep(id="a b", label="A", next="a_b"),
        ActivityStep(id="a_b", label="A2", next="fin"),
        ActivityStep(id="fin", label="Finish"),
    ]
    root = _parse(BpmnRenderer().render(_ir(steps, start="a b", end="fin")))
    counts = _check_structure(root)
    assert counts["task"] == 3 and counts["endEvent"] == 1


def test_rejects_other_ir():
    with pytest.raises(RenderError):
        BpmnRenderer().render(ComponentIR(title="x", nodes=[], edges=[]))


def test_viewer_html_inlines_bpmn_js_and_the_xml():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T <1>", {"description": "Desc & more", "preguntas_abiertas": ["¿Q1 <b>?"]})
    assert "bpmn-js - bpmn-navigated-viewer v" in page
    assert ".djs-container" in page  # diagram-js.css
    assert "new BpmnJS(" in page and "fit-viewport" in page
    # nothing is loaded from outside the file
    assert "<script src=" not in page and "<link" not in page
    assert not re.search(r"url\(['\"]?https?:|@import", page)
    assert "T &lt;1&gt;" in page and "Desc &amp; more" in page and "¿Q1 &lt;b&gt;?" in page
    literal = re.search(r"var xml = (\".*?\");\n", page, re.S).group(1)
    assert json.loads(literal) == xml
    assert "</bpmn:" not in page  # the XML is inside a JSON string with `<` escaped


def test_cli_render_writes_bpmn_and_html(tmp_path):
    result = CliRunner().invoke(
        main,
        ["diagram", "render", str(FIXTURES / "activity.mepu-decision.yml"), "--out", str(tmp_path), "--renderer", "bpmn"],
    )
    assert result.exit_code == 0, result.output
    bpmn = tmp_path / "activity.mepu-decision.bpmn"
    page = tmp_path / "activity.mepu-decision.bpmn.html"
    assert bpmn.exists() and page.exists()
    text = bpmn.read_text(encoding="utf-8")
    assert text.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<!-- specir: generated from')
    _check_structure(_parse(text))
    html = page.read_text(encoding="utf-8")
    assert "Preguntas abiertas" in html and "R2 parcial" in html
    assert "MEPU · Cómo se decide una línea" in html
    assert str(page) in result.output


def test_render_to_file_returns_the_bpmn_path(tmp_path):
    out = render_to_file(FIXTURES / "activity.complex.yml", out=tmp_path, renderer="bpmn")
    assert out.name == "activity.complex.bpmn"
    assert (tmp_path / "activity.complex.bpmn.html").exists()


COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
COLOR = {"color": COLOR_NS}


def _shapes(xml: str) -> dict[str, ET.Element]:
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    return {s.get("bpmnElement"): s for s in plane.findall("bpmndi:BPMNShape", NS)}


def _edges(xml: str) -> dict[str, ET.Element]:
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    return {e.get("bpmnElement"): e for e in plane.findall("bpmndi:BPMNEdge", NS)}


def test_tones_emit_bpmn_in_color_attributes_and_namespace():
    steps = [
        ActivityStep(id="a", label="Prepare", tone="info", next="ok"),
        ActivityStep(id="ok", label="Accepted", tone="success", next="gate"),
        ActivityStep(id="gate", label="Decide", kind="decision", tone="rule2",
                     branches={"yes": "warn", "no": "bad"}),
        ActivityStep(id="warn", label="Review", tone="warning", next="end"),
        ActivityStep(id="bad", label="Rejected", tone="danger"),
        ActivityStep(id="plain", label="Neutral task", tone="neutral", next="end"),
    ]
    xml = BpmnRenderer().render(_ir(steps, start="a", end="end"))
    assert f'xmlns:color="{COLOR_NS}"' in xml
    shapes = _shapes(xml)
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}background-color") == "#E1EEFB"
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}border-color") == "#1D4ED8"
    assert shapes["Task_ok"].get(f"{{{COLOR_NS}}}background-color") == "#E3F4E6"
    assert shapes["Task_warn"].get(f"{{{COLOR_NS}}}border-color") == "#B26A00"
    assert shapes["Task_bad"].get(f"{{{COLOR_NS}}}border-color") == "#B42318"
    assert shapes["Task_plain"].get(f"{{{COLOR_NS}}}border-color") == "#6B7280"
    # the gateway carries its own tone; its outgoing flows take that border colour
    assert shapes["Gateway_gate"].get(f"{{{COLOR_NS}}}border-color") == "#C2410C"
    edges = _edges(xml)
    gw_flows = [e for name, e in edges.items() if name.startswith("Flow_gate__")]
    assert len(gw_flows) == 2
    assert all(e.get(f"{{{COLOR_NS}}}border-color") == "#C2410C" for e in gw_flows)
    # flows that do not leave a gateway stay unstyled
    assert edges["Flow_start__a"].get(f"{{{COLOR_NS}}}border-color") is None


def test_events_and_untinted_gateway_get_default_colors():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="Decide", kind="decision", branches={"x": "end"}),
    ], start="a"))
    shapes = _shapes(xml)
    start = next(v for k, v in shapes.items() if k.startswith("StartEvent_"))
    end = next(v for k, v in shapes.items() if k.startswith("EndEvent_"))
    assert start.get(f"{{{COLOR_NS}}}background-color") == "#E3F4E6"
    assert end.get(f"{{{COLOR_NS}}}border-color") == "#8B1A1A"
    assert shapes["Gateway_d"].get(f"{{{COLOR_NS}}}background-color") == "#F4F0FB"
    # a task without tone stays at the default BPMN white, no colour attributes
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}background-color") is None


def test_rule_tones_are_five_distinct_soft_colors():
    from specir.visual.renderers.bpmn import TONE_PALETTE

    rules = [TONE_PALETTE[f"rule{i}"] for i in range(1, 6)]
    assert len(set(rules)) == 5
    assert len({bg for bg, _ in TONE_PALETTE.values()}) == len(TONE_PALETTE)


def test_tasks_are_wrapped_and_sized_to_their_text():
    long_label = "Una línea de una OC abierta de Laboratorio Chile con un texto bastante largo que debe envolverse"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="short", label="Do it", next="long"),
        ActivityStep(id="long", label=long_label, next="end"),
    ], start="short"))
    shapes = _shapes(xml)

    def bounds(nid):
        b = shapes[nid].find("dc:Bounds", NS)
        return int(b.get("width")), int(b.get("height"))

    w_short, h_short = bounds("Task_short")
    w_long, h_long = bounds("Task_long")
    assert w_long <= 240 and w_long >= 120
    assert h_long > h_short, "a long label grows the box in height instead of overflowing"
    assert w_short <= w_long
    assert h_short >= 60


def _column_gaps(xml: str) -> list[int]:
    """Horizontal space between consecutive columns: shapes plus their gateway labels."""
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    spans: list[tuple[int, int]] = []
    for shape in plane.findall("bpmndi:BPMNShape", NS):
        for bounds in shape.iter(f"{{{NS['dc']}}}Bounds"):
            x, w = int(bounds.get("x")), int(bounds.get("width"))
            spans.append((x, x + w))
    spans.sort()
    merged: list[list[int]] = []
    for a, b in spans:
        if merged and a < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    ends = [m[1] for m in merged]
    starts = [m[0] for m in merged[1:]]
    return [start - end for end, start in zip(ends, starts)]


def test_text_width_is_estimated_per_character_class():
    from specir.visual.renderers.bpmn import TASK_PAD, _task_box, _text_w, _wrap

    # uppercase, '_' and 'm'/'w' are wider than the old flat 7.7px, narrow signs are thinner
    assert _text_w("PARTIAL_STOCK") > len("PARTIAL_STOCK") * 7.7
    assert _text_w("mmmm") > _text_w("iiii")
    assert _text_w("...") < _text_w("III")
    # PARTIAL_STOCK (the label that used to break in two) fits on a single line
    w, _h = _task_box("PARTIAL_STOCK")
    assert w - TASK_PAD + 4 >= _text_w("PARTIAL_STOCK")
    assert _wrap("PARTIAL_STOCK", w - TASK_PAD + 4) == 1
    # even the widest label of the real specs stays whole inside its box
    w2, _h2 = _task_box("Revisar + RESERVA_INSTITUCIONAL · Customer Service")
    assert _wrap("RESERVA_INSTITUCIONAL", w2 - TASK_PAD + 4) == 1
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="Aceptar + PARTIAL_STOCK", next="end"),
    ], start="a"))
    bounds = _shapes(xml)["Task_a"].find("dc:Bounds", NS)
    assert int(bounds.get("width")) - TASK_PAD + 4 >= _text_w("PARTIAL_STOCK")


def test_column_gaps_shrink_without_labels_and_grow_with_the_longest_one():
    from specir.visual.renderers.bpmn import COL_GAP, MIN_COL_GAP, _text_w

    # a linear plan with no edge labels only pays the minimum gap at every column
    steps = [ActivityStep(id=f"s{i}", label=f"Paso {i}", next=f"s{i + 1}") for i in range(5)]
    steps.append(ActivityStep(id="s5", label="Fin del camino"))
    linear = _column_gaps(BpmnRenderer().render(_ir(steps, start="s0")))
    assert linear and all(gap == MIN_COL_GAP for gap in linear)

    # a labelled flow widens only the gap it crosses, up to the old COL_GAP ceiling
    label = "etiqueta de rama"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="¿Sigue?", kind="decision", branches={label: "b", "no": "end"}),
        ActivityStep(id="b", label="B", next="end"),
    ], start="a"))
    gaps = _column_gaps(xml)
    assert int(min(COL_GAP, max(MIN_COL_GAP, _text_w(label) + 40))) in gaps
    assert MIN_COL_GAP in gaps and max(gaps) < COL_GAP
    long_label = "una etiqueta considerablemente mas larga que el hueco maximo permitido"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="¿Sigue?", kind="decision", branches={long_label: "b", "no": "end"}),
        ActivityStep(id="b", label="B", next="end"),
    ], start="a"))
    assert max(_column_gaps(xml)) == COL_GAP


def _activity_spec(tmp_path: Path, data: dict) -> Path:
    spec = tmp_path / "activity.yml"
    spec.write_text(yaml.safe_dump({"id": "a", "title": "A", "type": "activity", "version": "1", "data": data}), encoding="utf-8")
    return spec


def test_tone_field_is_validated_by_the_model(tmp_path):
    """The step model is sldb's (D3): a step's `tone` is one of the palette's tones or nothing."""
    from sldb.api.notations import validate_spec

    steps = {"a": {"label": "x", "tone": "rule5", "next": "b"}, "b": {"label": "y", "next": "end"}}
    diagram = load(_activity_spec(tmp_path, {"start": "a", "end": "end", "steps": steps}))
    validate_spec(diagram)
    assert diagram.data.steps["a"].tone == "rule5" and diagram.data.steps["b"].tone is None
    steps["a"]["tone"] = "chartreuse"
    with pytest.raises(Exception, match="tone"):
        load(_activity_spec(tmp_path, {"start": "a", "end": "end", "steps": steps}))


def test_viewer_has_a_compact_header_full_height_canvas_and_collapsed_meta():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T", {"description": "Desc", "preguntas_abiertas": ["¿Q?"]})
    # title, buttons and legend stay in the bar; description and questions are collapsed
    assert "<details class=\"meta\">" in page and "<summary>Descripción y preguntas abiertas</summary>" in page
    assert " open" not in page.split("<details")[1].split(">")[0]
    assert 'class="legend"' in page and "white-space: nowrap" in page
    # the canvas takes whatever the bar leaves, on a full-viewport flex column
    assert "height: 100vh" in page and "flex-direction: column" in page
    assert "#canvas { flex: 1 1 auto" in page
    assert "<header>" in page


def test_viewer_font_size_and_initial_zoom():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T", None)
    assert "textRenderer" in page and "defaultStyle" in page and "externalStyle" in page
    assert "fontSize: 14" in page
    assert "MIN_ZOOM = 0.6" in page and "canvas.zoom(MIN_ZOOM)" in page
    # Fit really fits, it does not re-apply the minimum-zoom initial view
    assert "function fitViewport()" in page
    assert "document.getElementById('fit').addEventListener('click', fitViewport)" in page
    assert ".zoom('fit-viewport', 'auto')" in page
    assert "getAbsoluteBBox(start)" in page  # the initial view is anchored on the start event
    # entering a subprocess applies the same rule as the initial view
    assert "viewer.on('root.set', function () { try { initialView(); }" in page


def test_legend_shows_only_used_tones_with_generic_spanish_labels():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", tone="success", next="bad"),
        ActivityStep(id="bad", label="Bad", tone="danger", next="d"),
        ActivityStep(id="d", label="Decide", kind="decision", branches={"x": "end"}),
    ], start="a"))
    page = render_bpmn_html(xml, "T", None)
    assert ">favorable</span>" in page and ">rechazo</span>" in page
    assert ">gateway por defecto</span>" in page
    # start/end events never take a legend colour
    assert ">inicio</span>" not in page and ">fin</span>" not in page
    # unused tones are not in the legend
    for unused in ("atención", "informativo", "neutro", "regla 1", "regla 5"):
        assert f">{unused}</span>" not in page


def test_legend_reads_custom_labels_from_metadata():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", tone="rule2", next="ok"),
        ActivityStep(id="ok", label="OK", tone="success", next="end"),
    ], start="a"))
    page = render_bpmn_html(xml, "T", {"legend": {"rule2": "R2 · Stock", "success": "Aceptar"}})
    assert ">R2 · Stock</span>" in page and ">Aceptar</span>" in page
    assert ">regla 2</span>" not in page


def test_cli_render_takes_legend_and_questions_from_the_metadata_model(tmp_path):
    spec = tmp_path / "leyenda.yml"
    raw = yaml.safe_load((FIXTURES / "activity.mepu-decision.yml").read_text(encoding="utf-8"))
    raw["metadata"]["preguntas_abiertas"] = "¿Una sola pregunta?"
    raw["metadata"]["legend"] = {"gateway": "Decisión de negocio"}
    spec.write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
    result = CliRunner().invoke(main, ["diagram", "render", str(spec), "--out", str(tmp_path), "--renderer", "bpmn"])
    assert result.exit_code == 0, result.output
    page = (tmp_path / "leyenda.bpmn.html").read_text(encoding="utf-8")
    assert "<li>¿Una sola pregunta?</li>" in page and ">Decisión de negocio</span>" in page


def _group_ir() -> ActivityIR:
    return ActivityIR(
        title="Grupos", start="a", end="e",
        steps=[
            ActivityStep(id="a", label="Entrada", group="g1", detail="Texto largo de a.", next="b"),
            ActivityStep(id="b", label="¿Sigue?", kind="decision", group="g1",
                         branches={"ok": "c", "no": "x"}),
            ActivityStep(id="c", label="Cierre interno", group="g1", next="d"),
            ActivityStep(id="x", label="Afuera", next="d"),
            ActivityStep(id="d", label="Evaluar", group="g2", next="e"),
            ActivityStep(id="e", label="Fin del grupo", group="g2"),
        ],
        groups={
            "g1": ActivityGroup(id="g1", label="Grupo uno", tone="info", detail="Detalle del grupo uno."),
            "g2": ActivityGroup(id="g2", label="Grupo dos", tone="warning", detail="Detalle del grupo dos."),
        },
    )


def test_groups_are_collapsed_subprocesses_with_their_own_planes():
    from specir.visual.renderers.bpmn import TONE_PALETTE

    root = _parse(BpmnRenderer().render(_group_ir()))
    proc = root.find("bpmn:process", NS)
    subs = {el.get("id"): el for el in proc.findall("bpmn:subProcess", NS)}
    assert set(subs) == {"SubProcess_g1", "SubProcess_g2"}
    assert subs["SubProcess_g1"].get("name") == "Grupo uno"
    planes = {p.get("bpmnElement"): p for p in root.findall("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)}
    assert set(planes) == {"Process_1", "SubProcess_g1", "SubProcess_g2"}
    top_shapes = {s.get("bpmnElement"): s for s in planes["Process_1"].findall("bpmndi:BPMNShape", NS)}
    for sid in subs:
        assert top_shapes[sid].get("isExpanded") == "false"
        assert top_shapes[sid].get(f"{{{COLOR_NS}}}background-color") in {
            background for background, _ in TONE_PALETTE.values()
        }
    # ids are unique across every plane
    ids = [el.get("id") for el in root.iter() if el.get("id")]
    assert len(ids) == len(set(ids))
    # each subprocess plane has its own start, its steps and its external end events
    g1 = planes["SubProcess_g1"]
    g1_nodes = [el.get("bpmnElement") for el in g1.findall("bpmndi:BPMNShape", NS)]
    assert {"StartEvent_g1__in", "Task_a", "Gateway_b", "Task_c"} <= set(g1_nodes)
    g1_ends = {el.get("bpmnElement") for el in g1.findall("bpmndi:BPMNShape", NS)
               if el.get("bpmnElement", "").startswith("EndEvent_g1__")}
    assert len(g1_ends) == 2  # one per distinct external destination (step x, group g2)
    g1_flows = g1.findall("bpmndi:BPMNEdge", NS)
    assert len(g1_flows) == 5
    g2 = planes["SubProcess_g2"]
    g2_ends = [el.get("bpmnElement") for el in g2.findall("bpmndi:BPMNShape", NS)
               if el.get("bpmnElement", "").startswith("EndEvent_g2__")]
    assert len(g2_ends) == 1  # terminal step e exits to the process end
    # top level: flows enter the subprocess and leave it toward the real destinations
    top_flows = proc.findall("bpmn:sequenceFlow", NS)
    assert {(f.get("sourceRef"), f.get("targetRef")) for f in top_flows} == {
        ("StartEvent_a", "SubProcess_g1"),
        ("SubProcess_g1", "Task_x"),
        ("SubProcess_g1", "SubProcess_g2"),
        ("Task_x", "SubProcess_g2"),
        ("SubProcess_g2", "EndEvent_e"),
    }
    labels = {f.get("name") for f in top_flows if f.get("sourceRef") == "SubProcess_g1"}
    assert labels == {"Afuera", "Grupo dos"}
    # the inner flows reach those end events
    inner = {(f.get("sourceRef"), f.get("targetRef")) for f in subs["SubProcess_g1"].findall("bpmn:sequenceFlow", NS)}
    assert ("Gateway_b", "Task_c") in inner and ("Task_c", "EndEvent_g1__g2") in inner


def test_group_and_step_detail_reach_the_viewer_json():
    xml = BpmnRenderer().render(_group_ir())
    page = render_bpmn_html(xml, "T", None)
    literal = re.search(r"var info = (\{.*?\});\n", page, re.S).group(1)
    info = json.loads(literal)
    assert info["Task_a"]["detail"] == "Texto largo de a."
    assert info["SubProcess_g1"]["detail"] == "Detalle del grupo uno."
    assert info["SubProcess_g1"]["label"] == "Grupo uno"
    assert info["SubProcess_g1"]["subprocess"] is True
    assert info["Gateway_b"]["branches"] == [
        {"label": "ok", "target": "Cierre interno"},
        {"label": "no", "target": "Afuera"},
    ]
    assert "id=\"panel\"" in page and "340px" in page and "toggle-panel" in page


def test_spec_without_groups_produces_one_plane_and_no_subprocess():
    xml = render(compile_ir(load(FIXTURES / "activity.mepu-decision.yml")), "bpmn")
    root = _parse(xml)
    assert root.findall(".//bpmn:subProcess", NS) == []
    assert len(root.findall("bpmndi:BPMNDiagram", NS)) == 1
    _check_structure(root)


def test_other_renderers_accept_groups_and_detail():
    ir = compile_ir(load(FIXTURES / "activity.groups.yml"))
    for name in ("mermaid", "plantuml", "d2"):
        assert render(ir, name)


def test_model_validates_groups_and_detail(tmp_path):
    """The step and group models are sldb's (D3)."""
    from sldb.api.notations import validate_spec

    groups = {"g": {"label": "G", "tone": "info", "detail": "GD"}}
    data = {"start": "a", "end": "end", "steps": {"a": {"label": "A", "detail": "D", "group": "g", "next": "end"}}, "groups": groups}
    diagram = load(_activity_spec(tmp_path, data))
    validate_spec(diagram)
    step = diagram.data.steps["a"]
    assert step.detail == "D" and step.group == "g"
    assert diagram.data.groups["g"].label == "G"
    data["steps"]["a"]["group"] = "missing"
    with pytest.raises(Exception, match="unknown group 'missing'"):
        validate_spec(load(_activity_spec(tmp_path, data)))

FILE:tests/visual/test_lint_mermaid.py
"""The mermaid linter of specIR (SV-D01), migrated from `spec2viz.linters.mermaid`.

- `tests/test_mermaid_mmdc.py` of spec2viz (revision 2de1056) ported case by case: the real-engine
  (mmdc) cases skip when mermaid-cli is not installed, as in spec2viz; the regex cases force the
  engine off (`SPECIR_MMDC=0`, and spec2viz's `SPEC2VIZ_MMDC=0` still works).
- The same findings as spec2viz on the lint fixtures (`render_parity.lint_cases`: spec2viz's lint
  texts and the mermaid of every spec of the corpus), with and without the raw-angle-bracket rule:
  against the saved goldens always, against spec2viz live when it is installed.
- `diagram lint` reports a clean spec, a clean `.mmd` and a broken `.mmd` as spec2viz's did."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render_parity  # noqa: E402

from specir.visual.commands import main  # noqa: E402
from specir.visual.exceptions import RenderError  # noqa: E402
from specir.visual.lint_mermaid import MermaidLintError, assert_mermaid_ok, lint_mermaid, mmdc_path  # noqa: E402

_MMDC = mmdc_path() is not None
requires_mmdc = pytest.mark.skipif(not _MMDC, reason="mmdc (mermaid-cli) not installed")

BROKEN = {name: render_parity.LINT_TEXTS[name] for name in ("paren-edge-label", "brace-edge-label", "nested-quotes", "html-entity-seq")}
CLEAN = {name: render_parity.LINT_TEXTS[name] for name in ("simple-graph", "quoted-paren-edge", "sequence-ok")}


# ── tests/test_mermaid_mmdc.py ──────────────────────────────────────────────────────────────────


@requires_mmdc
@pytest.mark.parametrize("case", BROKEN)
def test_mmdc_catches_broken(case):
    problems = lint_mermaid(BROKEN[case])
    assert problems, f"{case}: expected mmdc to reject but lint was clean"
    assert any("mmdc" in p for p in problems)


@requires_mmdc
@pytest.mark.parametrize("case", CLEAN)
def test_mmdc_passes_clean(case):
    assert lint_mermaid(CLEAN[case]) == []


@pytest.mark.parametrize("variable", ["SPECIR_MMDC", "SPEC2VIZ_MMDC"])
def test_mmdc_disabled_skips_engine(monkeypatch, variable):
    # With the engine forced off, a paren edge label passes the regex-only pass.
    monkeypatch.delenv("SPECIR_MMDC", raising=False)
    monkeypatch.setenv(variable, "0")
    assert mmdc_path() is None
    assert lint_mermaid(BROKEN["paren-edge-label"]) == []


def test_regex_rules_still_fire_without_engine(monkeypatch):
    # The pre-existing heuristics must keep working when the engine is off.
    monkeypatch.setenv("SPECIR_MMDC", "0")
    problems = lint_mermaid("sequenceDiagram\n    A<<--B: bad\n")
    assert any("<<--" in p for p in problems)


# ── same findings as spec2viz ───────────────────────────────────────────────────────────────────


def test_lint_goldens_cover_the_fixtures_and_flag_the_bad_ones():
    goldens = render_parity.lint_goldens()
    assert sorted(goldens) == sorted(render_parity.lint_cases())
    flagged = {name for name, found in goldens.items() if found["check_html"]}
    assert {"invalid-return-arrow", "raw-angle-brackets", "bad-return-arrow", "empty-decision"} <= flagged
    assert any(name.startswith("mermaid:") for name in goldens)


def test_specir_finds_what_the_goldens_say(monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    assert render_parity.lint_findings(lint_mermaid) == render_parity.lint_goldens()


@pytest.mark.parity
def test_specir_finds_what_spec2viz_finds(monkeypatch):
    pytest.importorskip("spec2viz")
    monkeypatch.setenv("SPECIR_MMDC", "0")
    monkeypatch.setenv("SPEC2VIZ_MMDC", "0")
    assert render_parity.lint_findings(lint_mermaid) == render_parity.lint_findings(render_parity.spec2viz_lint())


def test_assert_mermaid_ok_raises_a_render_error(monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    assert_mermaid_ok(CLEAN["sequence-ok"])
    with pytest.raises(MermaidLintError, match=r"Mermaid lint failed in x\.mmd \(2 issue\(s\)\)") as caught:
        assert_mermaid_ok(render_parity.LINT_TEXTS["invalid-return-arrow"], source="x.mmd")
    assert isinstance(caught.value, RenderError)


# ── diagram lint ────────────────────────────────────────────────────────────────────────────────


def test_diagram_lint_command(tmp_path, monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    runner = CliRunner()
    spec = render_parity.parity.FIXTURES / "tests" / "fixtures" / "sequence.create-quotation.yml"
    ok = runner.invoke(main, ["diagram", "lint", str(spec)])
    assert ok.exit_code == 0 and "sequence.create-quotation.yml: OK" in ok.output
    good = tmp_path / "good.mmd"
    good.write_text(CLEAN["simple-graph"], encoding="utf-8")
    bad = tmp_path / "bad.mmd"
    bad.write_text(render_parity.LINT_TEXTS["invalid-return-arrow"], encoding="utf-8")
    result = runner.invoke(main, ["diagram", "lint", str(good), str(bad)])
    assert result.exit_code == 1
    assert "good.mmd: OK" in result.output and "bad.mmd: 2 issue(s)" in result.output and "<<--" in result.output

FILE:tests/visual/test_schema.py
"""JSON Schema export of specs and catalogs (SV-A15, SV-A16), migrated from `spec2viz.schema`.

The models are sldb's (D3); specIR only exports their schema. The export equals spec2viz's for all
types, each type and the diagram store envelope: against the saved goldens and spec2viz's checked-in
schemas (`examples/schema/`) always, against spec2viz live when it is installed. Ported from spec2viz
(revision 2de1056): `test_json_schema_for_all_types`, `test_json_schema_for_specific_type` and
`test_write_json_schema` of `tests/test_api.py`; `test_schema_stdout`, `test_schema_outfile`,
`test_schema_diagram_store_stdout`, `test_schema_invalid_type_fails` and `test_catalog_schema_stdout`
of `tests/test_cli.py` (on `diagram schema`, the command the top-level alias of IR13d calls); and
`test_schema_examples_match_generated_output` and `test_every_model_field_has_a_description` of
`tests/test_packaging.py` (the second over the exported schema, since the model classes are sldb's)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render_parity  # noqa: E402

from specir.visual.commands import main  # noqa: E402
from specir.visual.schema import json_schema, write_json_schema  # noqa: E402

SCHEMAS = HERE / "fixtures" / "spec2viz" / "examples" / "schema"
runner = CliRunner()


def test_schema_goldens_cover_every_type():
    assert set(render_parity.schema_goldens()) == {str(t or "all") for t in render_parity.SCHEMA_TYPES}


def test_specir_exports_what_the_goldens_say():
    assert render_parity.schemas(json_schema) == render_parity.schema_goldens()


@pytest.mark.parity
def test_specir_exports_what_spec2viz_exports():
    pytest.importorskip("spec2viz")
    assert render_parity.schemas(json_schema) == render_parity.schemas(render_parity.spec2viz_json_schema())


# ── tests/test_api.py ───────────────────────────────────────────────────────────────────────────


def test_json_schema_for_all_types():
    schema = json_schema()

    assert "$defs" in schema
    assert "SequenceDiagram" in schema["$defs"]


def test_json_schema_for_specific_type():
    schema = json_schema("sequence")

    assert schema["title"] == "SequenceDiagram"
    assert schema["properties"]["data"]["description"] == "Sequence-specific participants and messages."


def test_write_json_schema(tmp_path):
    path = write_json_schema(tmp_path / "sequence.schema.json", diagram_type="sequence")

    assert path.exists()
    assert json.loads(path.read_text())["title"] == "SequenceDiagram"


# ── tests/test_cli.py ───────────────────────────────────────────────────────────────────────────


def test_schema_stdout():
    r = runner.invoke(main, ["diagram", "schema", "--type", "sequence"])
    assert r.exit_code == 0
    assert '"title": "SequenceDiagram"' in r.output


def test_schema_outfile(tmp_path):
    out = tmp_path / "schema.json"
    r = runner.invoke(main, ["diagram", "schema", "--type", "state", "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()


def test_schema_diagram_store_stdout():
    r = runner.invoke(main, ["diagram", "schema", "--type", "diagram-store"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert '"diagram_store"' in r.output


def test_schema_invalid_type_fails():
    r = runner.invoke(main, ["diagram", "schema", "--type", "unknown"])
    assert r.exit_code != 0


def test_catalog_schema_stdout():
    r = runner.invoke(main, ["catalog", "schema"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert json.loads(r.output) == json_schema("diagram-store")


# ── tests/test_packaging.py ─────────────────────────────────────────────────────────────────────


def test_schema_examples_match_generated_output():
    assert json.loads((SCHEMAS / "spec2viz.schema.json").read_text()) == json_schema()
    assert json.loads((SCHEMAS / "sequence.schema.json").read_text()) == json_schema("sequence")


#: The models spec2viz's test checked, by the name of their schema definition. `BaseDiagram` has no
#: definition of its own: its fields are in each `*Diagram`.
DESCRIBED_MODELS = (
    "Metadata", "Style", "ParticipantModel", "MessageModel", "SequenceData", "SequenceDiagram",
    "StateModel", "TransitionModel", "StateData", "StateDiagram", "NodeModel", "EdgeModel", "ComponentData",
    "ComponentDiagram", "StepModel", "ActivityData", "ActivityDiagram", "DeploymentNodeModel", "ArtifactModel",
    "ConnectionModel", "DeploymentData", "DeploymentDiagram", "MatrixStageModel", "MatrixViewModel",
    "MatrixComponentModel", "MatrixData", "MatrixDiagram",
)


def test_every_model_field_has_a_description():
    """Every field of the models spec2viz checked has a description in the exported schema."""
    definitions = json_schema()["$defs"]
    missing = [
        f"{name}.{field}"
        for name in DESCRIBED_MODELS
        for field, prop in definitions[name]["properties"].items()
        if not prop.get("description")
    ]
    assert not missing, missing

FILE:tests/visual/test_resources.py
"""Resources that specIR's visual layer packages (SV-C07, SV-C10, SV-J04, SV-J05, SV-G08 for the template).

- The catalog template (`templates/default.html`) and the vendored bpmn-js
  (`templates/vendor/bpmn-js/`) are package data of specIR: the installed package reads them, a wheel
  built from the project carries them, and they are spec2viz's own bytes (live, when installed).
- The pages that must open from `file://` with nothing from outside (the offline BPMN viewer and the
  graph HTML; the tree HTML too) reference no external script, stylesheet, font or import; the
  viewer inlines the vendored bpmn-js and its two stylesheets.
- `test_examples_render_successfully` of spec2viz's `tests/test_packaging.py`, over the same
  examples (`fixtures/spec2viz/examples/`)."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import zipfile
from importlib.resources import files
from pathlib import Path

import pytest

from specir.visual.render_file import render_to_file
from specir.visual.renderers.bpmn_viewer import VENDOR_DIR

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_parity  # noqa: E402

PROJECT = HERE.parents[1]
CORPUS = HERE / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"
VENDOR = ("LICENSE", "README.md", "bpmn-js.css", "bpmn-navigated-viewer.production.min.js", "diagram-js.css")
RESOURCES = ("templates/default.html", *(f"templates/vendor/bpmn-js/{name}" for name in VENDOR))
#: What would make a page fetch something to open: a script by URL, a stylesheet or font link, a CSS
#: import, a CSS url() to the network, or any `src` (image, frame) to the network. A link the reader
#: may follow (`<a href>`, like bpmn.io's watermark inside bpmn-js) fetches nothing.
EXTERNAL = re.compile(r"<script[^>]*\bsrc=|<link\b|@import|url\(\s*['\"]?(?:https?:)?//|\bsrc=['\"]?(?:https?:)?//", re.I)


def _resource(rel: str):
    return files("specir.visual").joinpath(*rel.split("/"))


def test_the_installed_package_reads_its_resources():
    for rel in RESOURCES:
        assert _resource(rel).is_file(), rel
        assert _resource(rel).read_bytes(), rel
    assert Path(str(_resource("templates/vendor/bpmn-js"))) == VENDOR_DIR
    readme = _resource("templates/vendor/bpmn-js/README.md").read_text(encoding="utf-8")
    js = _resource("templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js").read_text(encoding="utf-8")
    version = re.search(r"`bpmn-js` (\d+\.\d+\.\d+)", readme).group(1)
    assert f"bpmn-navigated-viewer v{version}" in js


@pytest.mark.parity
def test_resources_are_spec2viz_bytes():
    pytest.importorskip("spec2viz")
    origin = render_parity.spec2viz_package_dir()
    for rel in RESOURCES:
        assert _resource(rel).read_bytes() == (origin / rel).read_bytes(), rel


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is not installed: no backend to build the wheel")
def test_a_wheel_of_the_project_carries_the_resources(tmp_path):
    """The package data is declared (pyproject.toml), not only present in the source tree."""
    project = tmp_path / "project"
    project.mkdir()
    shutil.copy(PROJECT / "pyproject.toml", project / "pyproject.toml")
    shutil.copytree(PROJECT / "src" / "specir", project / "src" / "specir", ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
    result = subprocess.run(
        ["uv", "build", "--wheel", "--offline", "--out-dir", str(tmp_path / "dist"), str(project)],
        capture_output=True, text=True, timeout=300,
    )
    assert result.returncode == 0, result.stderr[-800:]
    wheel = next((tmp_path / "dist").glob("specir-*.whl"))
    names = set(zipfile.ZipFile(wheel).namelist())
    for rel in RESOURCES:
        assert f"specir/visual/{rel}" in names, rel


def test_bpmn_viewer_opens_without_external_resources(tmp_path):
    out = render_to_file(FIXTURES / "activity.mepu-decision.yml", out=tmp_path, renderer="bpmn")
    page = out.with_name(out.name + ".html").read_text(encoding="utf-8")
    assert not EXTERNAL.search(page), EXTERNAL.search(page)
    for name in ("bpmn-js.css", "diagram-js.css"):
        css = (VENDOR_DIR / name).read_text(encoding="utf-8")
        assert css.strip()[:200] in page, name
    js = (VENDOR_DIR / "bpmn-navigated-viewer.production.min.js").read_text(encoding="utf-8")
    assert js[:200] in page and len(page) > len(js)


@pytest.mark.parametrize("renderer, spec", [("graph", "component.quotation.yml"), ("tree", "component.quotation.yml")])
def test_component_html_opens_without_external_resources(tmp_path, renderer, spec):
    page = render_to_file(FIXTURES / spec, out=tmp_path, renderer=renderer).read_text(encoding="utf-8")
    assert page.lstrip().lower().startswith("<!doctype html")
    assert not EXTERNAL.search(page), EXTERNAL.search(page)
    assert "QuotationFlow" in page


# ── tests/test_packaging.py ─────────────────────────────────────────────────────────────────────


def test_examples_render_successfully(tmp_path):
    example_paths = [
        path
        for path in sorted(EXAMPLES.glob("**/*.yml"))
        if "/catalog/" not in path.as_posix() and path.name not in {"project.yml", "vistas.yml"}
    ]

    assert example_paths

    for example_path in example_paths:
        output_path = render_to_file(example_path, out=tmp_path)
        assert output_path.exists(), f"missing output for {example_path}"

FILE:tests/visual/test_visual_names.py
"""specIR's visual layer takes from sldb what is sldb's and does not redefine it.

- No class of specIR has the name of a visual vocabulary model of SLDB (the notation documents
  `sldb.api` exports and the notation and palette specs of `sldb.notations`).
- No class of specIR has the name of a diagram spec model: the eight models (and every model they
  are made of) are sldb's (D3) and `compile_ir` dispatches sldb's classes.
- spec2viz is imported, under tests/, only by the parity oracles (tests/visual/parity.py of IR11
  and tests/visual/render_parity.py of IR12); under src/specir/ never (tests/test_imports.py)."""

from __future__ import annotations

import ast
import inspect
import typing
from pathlib import Path

import sldb.api as api
import sldb.notations as notations
from pydantic import BaseModel
from sldb.api.notations import load_spec

from specir.visual import compile_ir
from specir.visual.spec_models import SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "src" / "specir"
TESTS = REPO / "tests"
ORACLES = {TESTS / "visual" / "parity.py", TESTS / "visual" / "render_parity.py"}
EIGHT = {"ClassDiagram", "SequenceDiagram", "StateDiagram", "ComponentDiagram", "ActivityDiagram",
         "DeploymentDiagram", "MatrixDiagram", "ReflectionDiagram"}


def specir_classes() -> dict[str, str]:
    found = {}
    for path in sorted(PACKAGE.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ClassDef):
                found[node.name] = str(path.relative_to(REPO))
    return found


def vocabulary() -> set[str]:
    docs = {n for n in dir(api) if inspect.isclass(getattr(api, n)) and getattr(api, n).__module__.startswith("sldb.models.notation")}
    specs = {n for n in notations.__all__ if inspect.isclass(getattr(notations, n)) and not issubclass(getattr(notations, n), Exception)}
    return docs | specs


def models_of(model: type, seen: set[type]) -> None:
    """`model` and every pydantic model its fields are made of."""
    if model in seen:
        return
    seen.add(model)
    for field in model.model_fields.values():
        for part in _types(field.annotation):
            if inspect.isclass(part) and issubclass(part, BaseModel):
                models_of(part, seen)


def _types(annotation) -> list:
    args = typing.get_args(annotation)
    return [annotation] if not args else [t for a in args for t in _types(a)]


def spec_model_names() -> set[str]:
    seen: set[type] = set()
    for model in (*SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact):
        models_of(model, seen)
    return {m.__name__ for m in seen}


def test_no_class_has_the_name_of_a_visual_vocabulary_model_of_sldb() -> None:
    names = vocabulary()
    assert {"SpecDoc", "SpecNodeDoc", "NotationDoc", "GlyphDoc", "LinkDoc", "PaletteDoc", "ViewDoc", "NotationSpec", "PaletteSpec"} <= names
    clashes = {name: where for name, where in specir_classes().items() if name in names}
    assert not clashes, clashes


def test_no_class_has_the_name_of_a_diagram_spec_model() -> None:
    names = spec_model_names()
    assert EIGHT <= names and {"NodeModel", "EdgeModel", "EnforcementArtifact"} <= names
    clashes = {name: where for name, where in specir_classes().items() if name in names}
    assert not clashes, clashes


def test_the_eight_spec_models_are_sldb_classes_and_compile() -> None:
    assert {m.__name__ for m in SPEC_MODELS} == EIGHT
    assert all(m.__module__.startswith("sldb.") for m in (*SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact))
    examples = REPO / "tests" / "visual" / "fixtures" / "spec2viz" / "examples"
    diagrams = [load_spec(path) for path in sorted(examples.rglob("*.yml"))]
    assert {type(d) for d in diagrams} == set(SPEC_MODELS)
    for diagram in diagrams:
        assert compile_ir(diagram) is not None, diagram.id


def test_spec2viz_is_imported_only_by_the_parity_oracle() -> None:
    importing = set()
    for path in sorted([*TESTS.rglob("*.py"), *PACKAGE.rglob("*.py")]):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
            if any(n.split(".")[0] == "spec2viz" for n in names):
                importing.add(path)
    assert importing == ORACLES, importing

FILE:instruccion
Cold-bundle de la tarea task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Por cada renderizador, los fixtures de spec2viz producen en specIR una salida idéntica a su golden, o la diferencia está declarada en la matriz de cobertura con su prueba equivalente.
- El linter de Mermaid reporta en specIR los mismos hallazgos que en spec2viz sobre los fixtures de lint.
- El JSON Schema exportado por specIR para specs y catálogos es igual al de spec2viz, o la diferencia está declarada.
- El HTML del visor BPMN y el HTML de grafo generados abren sin recursos externos faltantes (prueba de empaquetado).
- Todos los valores del selector de renderizador de spec2viz existen en specIR.
- El paquete no importa spec2viz.

