FILE:desk/tasks/task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs.md
---
sldb:
  by: agent
  at: '2026-11-15T23:37:44Z'
  authority: generated
  via: save_document_payload
id: task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs
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
- task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
- task-ir11-compiladores-y-proyecciones-de-spec2viz
- task-espejo-sldb-specsync-en-sldb-api-notations-d1
- task-espejo-sldb-generador-de-spec-desde-grafo-y-ast-d2
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- tests/visual/test_sync_generation_parity.py
- tests/test_imports.py
- tests/visual/test_visual_names.py
- src/specir/visual/__init__.py
- docs/spec2viz/matriz-de-cobertura.md
- pyproject.toml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13a Sincronización de specs al store y generación de specs

## Rationale

_Explain why this task exists or the business driver behind it._

Parte de la migración final de spec2viz, separada de IR13 para que cada tarea tenga un solo entregable. La sincronización es lo que conecta un diagrama autorado con el grafo de SLDB, y las dos formas de generar un spec (desde el grafo y desde el AST de Python) son las que usan hoy los repos para documentar su arquitectura.

## Goal

_Describe the concrete result this task must produce._

specIR sincroniza un spec al store y genera specs de componentes usando lo que migra a sldb: SpecSync (D1), el generador desde un grafo o un snapshot y desde el AST de Python (D2, que cubre B4). specIR queda como adaptador de dominio y verifica la paridad con spec2viz; no reimplementa nada de eso.

## Scope

_State what is in scope and what is out of scope._

Dentro: la entrada de specIR a SpecSync de sldb (D1) y al generador de spec de componentes de sldb (D2, desde grafo, snapshot y AST de Python); la prueba de paridad con spec2viz sobre los fixtures de sincronización, importación de grafo y generación desde AST, portando a specIR solo lo que sldb no traiga ya con sus propias pruebas; la actualización de las filas de la matriz de cobertura con el modo migrado a sldb. Fuera: escribir SpecSync o el generador en specIR (se migran a sldb, tareas espejo D1 y D2); catálogos; notaciones y paletas; CLI; migración de consumidores; retirar spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Sin capa propia en specIR (regla de JP: lo genérico es de sldb y specIR no lo envuelve): los flujos de specIR y sus usuarios llaman directamente a sldb.api.notations (SpecSync, sync_spec, component_spec_from_graph, component_spec_from_python, write_component_spec) o a la CLI sldb notations sync --spec y sldb notations from-graph; specir.visual solo documenta ese uso, como ya hace con load_spec y validate_spec. La paridad se mide con pruebas de specIR en tests/visual/test_sync_generation_parity.py que comparan la salida de sldb con la de spec2viz como oráculo de desarrollo (marca parity, omitidas si spec2viz no está instalado): el store de prueba es un store sldb real creado con sldb.api.init_store en tmp_path; los fixtures de sincronización son los specs válidos del corpus de IR11 (tests/visual/fixtures/spec2viz, copia de tests/fixtures de spec2viz en 2de1056) más los specs ARQ y FLOW de tests/test_sldb_sync.py de spec2viz; el snapshot es el node-link de tests/test_graph_import.py de spec2viz; el paquete Python de fixture es el propio src/specir (código real, sin datos fabricados). tests/test_imports.py prueba que specIR no importa spec2viz y no define SpecSync ni generador de spec. Si el resultado de sldb difiere de spec2viz, la diferencia se declara en la matriz (docs/spec2viz/matriz-de-cobertura.md, filas SV-E01, SV-F01 y SV-F02) o se pide el arreglo por el desk de sldb. D1 y D2 son las tareas espejo task-espejo-sldb-specsync-en-sldb-api-notations-d1 y task-espejo-sldb-generador-de-spec-desde-grafo-y-ast-d2 (B4 es la fila del generador AST en el plan de migración).

## Validation

_List the checks required before this task can close._

- Sincronizar un spec con specIR deja en un store de prueba los mismos SpecDoc, SpecNodeDoc y RelationDoc que spec2viz sobre los fixtures de sincronización.
- Volver a sincronizar tras quitar un elemento del spec borra su SpecNodeDoc y sus RelationDoc.
- Una relación de tipo no builtin crea su RelationTypeDoc y el índice de aristas valida después de sincronizar.
- La compilación desde grafo produce, sobre el fixture de snapshot de spec2viz, un spec de componentes que valida y es equivalente al de spec2viz, o su reemplazo por proyección tiene la prueba equivalente declarada en la matriz.
- La generación desde AST produce, sobre un paquete Python de fixture, un spec de componentes equivalente al de spec2viz.
- El paquete no importa spec2viz.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan, specIR no define su propio SpecSync ni su propio generador de spec y las filas de sincronización, importación de grafo y generación de la matriz de cobertura tienen su condición de retiro cumplida con el modo migrado a sldb.

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

FILE:desk/atoms/atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:36Z'
  authority: generated
  via: create_document
id: atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
title: El vocabulario visual y el resolvedor de vistas ya viven en SLDB
five_wh_one_plus: where
tags:
- system:specir
- system:sldb
- system:spec2viz
- topic:vistas
- layer:modelo
provenance: ../sldb-astryx/desk/drawer/plans/absorber-spec2viz-y-modelos-ui/dag.yaml
---

# El vocabulario visual y el resolvedor de vistas ya viven en SLDB

## Answer

Desde el plan absorber-spec2viz-y-modelos-ui de SLDB (entregado el 2026-11-07), los modelos SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc viven en sldb/src/sldb/models/notation/, las notaciones y paletas builtin en sldb/src/sldb/notations/, y el resolvedor de vistas y proyecciones en sldb/src/sldb/api/notations/. Un alias en sldb/src/sldb/api/model_registry/model_reference.py resuelve las referencias antiguas spec2viz.sldb_models. specIR usa esas piezas desde SLDB y no las redefine. En spec2viz quedan, sin equivalente en SLDB, la autoría de specs YAML, los compiladores, los renderizadores, el catálogo y la sincronización de specs al store.

FILE:desk/atoms/atom-specir-depende-solo-de-la-api-pública-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-11T22:25:34Z'
  authority: generated
  via: create_document
id: atom-specir-depende-solo-de-la-api-pública-de-sldb
title: specIR depende solo de la API pública de SLDB
five_wh_one_plus: how
tags:
- system:specir
- system:sldb
- topic:dependencias
- layer:arquitectura
---

# specIR depende solo de la API pública de SLDB

## Answer

specIR se construye directamente sobre la API pública de SLDB (sldb.api), como hace deskops. Una capacidad general que falte (por ejemplo una operación de grafo o de store) se pide o se agrega en SLDB; no se reimplementa dentro de specIR ni se alcanza por módulos internos de SLDB. En specIR vive lo específico: el servidor MCP, los tipos y reglas del modelado de sistemas de software, y más adelante la capa visual.

FILE:tests/visual/test_sync_generation_parity.py
"""Spec synchronization to the store and component spec generation (IR13a): specIR uses sldb's.

specIR defines no SpecSync and no spec generator: syncing a spec is `sldb.api.notations.SpecSync`
(or `sync_spec`, or `sldb notations sync --spec`, D1) and generating a component spec is
`component_spec_from_graph` / `component_spec_from_python` / `write_component_spec` (or
`sldb notations from-graph`, D2), called directly. sldb carries its own ported tests for both; these
are the checks it does not have:

- on a real sldb store (always): resyncing after removing an element deletes its SpecNodeDoc and
  RelationDoc; a non-builtin relation creates its RelationTypeDoc and the edge index validates;
  a component spec compiled from a store's edge index and one generated from specIR's own package
  validate with the spec models of D3.
- parity with spec2viz as the development oracle (`parity` marker, skipped without spec2viz):
  the same SpecDoc, SpecNodeDoc, RelationDoc, RelationTypeDoc and notation documents and the same
  sync reports over spec2viz's sync fixtures (its `tests/fixtures/*.yml`, copied in IR11's corpus,
  and the ARQ/FLOW specs of its `tests/test_sldb_sync.py`); the same component spec from its
  graph-import snapshots (`tests/test_graph_import.py`) and from a store's edge index; and from the
  Python AST of specIR's package, the same spec up to the differences the coverage matrix declares
  for SV-F02.

Declared differences (docs/spec2viz/matriz-de-cobertura.md, SV-E01 and SV-F02):
- SV-E01: the description of a RelationTypeDoc created by the sync no longer ends in " de spec2viz".
- SV-F02: sldb reads imports from `sldb.code.scan_tree`, so `imports` edges count plain `import x`
  statements, resolve relative imports against the module's package and are not repeated per
  statement; `from x import y` statements nested below the module's top level (inside functions,
  `if`, `try`) are not read (asked to sldb's desk). Modules, classes and `defines` are identical."""

from __future__ import annotations

import ast
import importlib.util
import json
import shutil
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml
import sldb.api as sldb_api
from sldb.api.notations import (
    SpecSync,
    component_spec_from_graph,
    component_spec_from_python,
    index_graph,
    load_node_link,
    load_node_link_graph,
    load_spec,
    validate_spec,
    write_component_spec,
)

from parity import CORPUS, FIXTURES, goldens

PACKAGE = Path(__file__).resolve().parents[2] / "src" / "specir"
#: spec2viz's sync fixtures: its `tests/fixtures/*.yml` that validate (IR11's corpus keeps them).
SYNC_FIXTURES = [rel for rel in CORPUS if rel.startswith("tests/fixtures/") and goldens()[rel]["error"] is None]
#: The documents a spec sync writes (the spec, its elements and edges, relation types, notation).
MODELS = ("SpecDoc", "SpecNodeDoc", "RelationDoc", "RelationTypeDoc", "NotationDoc", "GlyphDoc", "LinkDoc")
REPORT_FIELDS = ("spec_id", "created", "updated", "deleted", "relation_types_added", "unresolved", "edge_errors")
#: SV-E01's declared difference: spec2viz signs the RelationTypeDoc descriptions it writes.
SPEC2VIZ_SIGNATURE = " de spec2viz."
KINDS = "tests/fixtures/component.kinds.yml"


# --- helpers ------------------------------------------------------------------------------------

def _project(root: Path, rels: list[str]) -> Path:
    """A real sldb store at `root` with the given corpus specs copied under `specs/`."""
    root.mkdir(parents=True)
    sldb_api.init_store(root)
    for rel in rels:
        target = root / "specs" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES / rel, target)
    return root


def _documents(root: Path) -> dict[str, tuple[str, dict[str, Any]]]:
    """Every synced document of the store, by export id: its path and its payload (no provenance)."""
    store = root / ".sldb"
    found: dict[str, tuple[str, dict[str, Any]]] = {}
    for model in MODELS:
        for row in sldb_api.select_documents(store, {"model": model}):
            found[row["export_id"]] = (row["path"], sldb_api.extract_document_payload(store, None, f"{model}/{row['name']}"))
    return found


def _report(report: Any) -> dict[str, Any]:
    return {field: getattr(report, field) if isinstance(getattr(report, field), str) else sorted(getattr(report, field)) for field in REPORT_FIELDS}


def _unsigned(documents: dict[str, tuple[str, dict[str, Any]]]) -> dict[str, tuple[str, dict[str, Any]]]:
    """spec2viz's documents with SV-E01's declared difference taken out."""
    out = {}
    for ref, (path, payload) in documents.items():
        if ref.startswith("RelationTypeDoc:") and payload.get("description", "").endswith(SPEC2VIZ_SIGNATURE):
            payload = {**payload, "description": payload["description"].removesuffix(SPEC2VIZ_SIGNATURE) + "."}
        out[ref] = (path, payload)
    return out


def _spec2viz_tests(name: str) -> ModuleType:
    """A test module of spec2viz's own suite (its fixtures are the oracle's), loaded from its checkout."""
    spec2viz = pytest.importorskip("spec2viz")
    path = Path(spec2viz.__file__).resolve().parents[1] / "tests" / f"{name}.py"
    if not path.is_file():
        pytest.skip(f"spec2viz's tests not found at {path}")
    spec = importlib.util.spec_from_file_location(f"spec2viz_oracle_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sync_both(tmp_path: Path, rels: list[str], write=None) -> tuple[list, list, Path, Path]:
    """Sync `rels` in order with sldb and with spec2viz, each into its own fresh store."""
    from spec2viz.sldb_sync import SpecSync as Spec2VizSync

    roots = []
    reports = []
    for name, sync_class in (("sldb", SpecSync), ("spec2viz", Spec2VizSync)):
        root = _project(tmp_path / name, [] if write else rels)
        if write:
            write(root)
        sync = sync_class(root / ".sldb")
        reports.append([_report(sync.sync(root / "specs" / rel)) for rel in rels])
        roots.append(root)
    return reports[0], reports[1], roots[0], roots[1]


def _assert_same_store(ours: Path, oracle: Path) -> None:
    found, expected = _documents(ours), _unsigned(_documents(oracle))
    assert sorted(found) == sorted(expected)
    differing = {ref: (found[ref], expected[ref]) for ref in found if found[ref] != expected[ref]}
    assert not differing, differing


def _validated(spec: dict, path: Path) -> None:
    write_component_spec(spec, path)
    validate_spec(load_spec(path))


# --- on a real sldb store -----------------------------------------------------------------------

def test_resync_deletes_the_spec_node_and_relations_of_a_removed_element(tmp_path: Path) -> None:
    root = _project(tmp_path / "p", [KINDS])
    spec_path = root / "specs" / KINDS
    sync = SpecSync(root / ".sldb")
    sync.sync(spec_path)
    store = root / ".sldb"
    assert sldb_api.doc_exists(store, "SpecNodeDoc/component.kinds.db")
    assert sldb_api.doc_exists(store, "RelationDoc/component.kinds.02-api__reads__db")

    data = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    del data["data"]["nodes"]["db"]
    data["data"]["edges"] = [edge for edge in data["data"]["edges"] if "db" not in (edge["from"], edge["to"])]
    spec_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    report = sync.sync(spec_path)

    assert sorted(report.deleted) == ["RelationDoc:component.kinds.02-api__reads__db", "SpecNodeDoc:component.kinds.db"]
    assert not sldb_api.doc_exists(store, "SpecNodeDoc/component.kinds.db")
    assert not sldb_api.doc_exists(store, "RelationDoc/component.kinds.02-api__reads__db")
    assert sldb_api.doc_exists(store, "RelationDoc/component.kinds.01-web__calls__api")


def test_a_non_builtin_relation_creates_its_type_and_the_edge_index_validates(tmp_path: Path) -> None:
    root = _project(tmp_path / "p", [KINDS])
    report = SpecSync(root / ".sldb").sync(root / "specs" / KINDS)
    assert report.relation_types_added == ["calls", "reads"]
    assert sldb_api.doc_exists(root / ".sldb", "RelationTypeDoc/reltype-calls")
    check = sldb_api.check_edges(root / ".sldb")
    assert (check.errors, check.stale) == ([], []), check
    relations = {(r.source.rsplit(":", 1)[-1], r.relation, r.target.rsplit(":", 1)[-1]) for r in sldb_api.load_edge_index(root / ".sldb").edges}
    assert ("component.kinds.web", "calls", "component.kinds.api") in relations


def test_a_component_spec_from_a_store_graph_validates(tmp_path: Path) -> None:
    root = _project(tmp_path / "p", [KINDS])
    SpecSync(root / ".sldb").sync(root / "specs" / KINDS)
    nodes, edges = index_graph(sldb_api.load_edge_index(root / ".sldb"))
    spec = component_spec_from_graph(nodes, edges, node_types=("document",), models=("SpecNodeDoc",), relations=("calls", "reads"), source="store")
    labels = {key: node["label"].removeprefix("component.kinds.") for key, node in spec["data"]["nodes"].items()}
    assert sorted(labels.values()) == ["api", "db", "web"]
    assert [(labels[e["from"]], e["relation"], labels[e["to"]]) for e in spec["data"]["edges"]] == [("web", "calls", "api"), ("api", "reads", "db")]
    _validated(spec, tmp_path / "graph.yml")


def test_a_component_spec_from_specir_python_ast_validates(tmp_path: Path) -> None:
    spec, findings = component_spec_from_python(PACKAGE, project_id="specir", title="specIR")
    assert findings == [] and spec is not None
    modules = {node["label"] for node in spec["data"]["nodes"].values() if node["kind"] == "module"}
    assert {"install", "mcp_extension", "visual.commands", "visual.compilers.component"} <= modules
    _validated(spec, tmp_path / "specir.yml")


# --- parity with spec2viz -----------------------------------------------------------------------

@pytest.mark.parity
@pytest.mark.parametrize("rel", SYNC_FIXTURES)
def test_sync_of_a_spec2viz_fixture_matches_spec2viz(tmp_path: Path, rel: str) -> None:
    pytest.importorskip("spec2viz")
    ours, oracle, our_root, oracle_root = _sync_both(tmp_path, [rel])
    assert ours == oracle
    _assert_same_store(our_root, oracle_root)


@pytest.mark.parity
def test_sync_and_resync_of_the_spec2viz_sync_specs_match_spec2viz(tmp_path: Path) -> None:
    oracle_tests = _spec2viz_tests("test_sldb_sync")
    reduced = json.loads(json.dumps(oracle_tests.ARQ))
    del reduced["data"]["nodes"]["renderers"]
    reduced["data"]["edges"] = [edge for edge in reduced["data"]["edges"] if edge["to"] != "renderers"]

    def write(root: Path) -> None:
        (root / "specs").mkdir()
        for spec in (oracle_tests.ARQ, oracle_tests.FLOW):
            (root / "specs" / f"{spec['id']}.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
        (root / "specs" / "arq-reduced.yml").write_text(yaml.safe_dump(reduced), encoding="utf-8")

    ours, oracle, our_root, oracle_root = _sync_both(tmp_path, ["arq.yml", "flow.yml", "arq-reduced.yml"], write)
    assert ours == oracle
    assert sorted(ours[2]["deleted"]) == ["RelationDoc:arq.02-core__loads_path__renderers", "SpecNodeDoc:arq.renderers"]
    _assert_same_store(our_root, oracle_root)


@pytest.mark.parity
def test_graph_import_of_the_spec2viz_snapshots_matches_spec2viz(tmp_path: Path) -> None:
    oracle_tests = _spec2viz_tests("test_graph_import")
    import spec2viz.graph_import as oracle

    snapshot = oracle_tests._node_link(tmp_path / "snap.json")
    assert load_node_link(snapshot) == oracle.load_node_link(snapshot)
    nodes, edges = load_node_link(snapshot)
    cases = [
        {"models": ("AtomDoc",)},
        {"node_types": ("document", "semantic_tag"), "relations": ("tagged_as",), "drop_isolated": True, "spec_id": "tags", "title": "Tags"},
        {"relations": ("has_document",)},
        {},
    ]
    for index, options in enumerate(cases):
        spec = component_spec_from_graph(nodes, edges, source=f"snapshot {snapshot}", **options)
        assert spec == oracle.component_spec_from_graph(nodes, edges, source=f"snapshot {snapshot}", **options), options
        _validated(spec, tmp_path / f"snap-{index}.yml")

    python_graph = tmp_path / "python-source.graph.json"
    python_graph.write_text(json.dumps(oracle_tests.PY_GRAPH), encoding="utf-8")
    loaded = load_node_link_graph(python_graph)
    assert loaded == oracle.load_node_link_graph(python_graph)
    for index, prefixes in enumerate((("sldb.selfdoc",), None)):
        options = {"node_types": ("python_module", "python_symbol", "python_external"), "attrs": loaded[2], "module_prefixes": prefixes}
        spec = component_spec_from_graph(loaded[0], loaded[1], **options)
        assert spec == oracle.component_spec_from_graph(loaded[0], loaded[1], **options), prefixes
        _validated(spec, tmp_path / f"python-{index}.yml")


@pytest.mark.parity
def test_graph_import_of_a_store_edge_index_matches_spec2viz(tmp_path: Path) -> None:
    pytest.importorskip("spec2viz")
    from spec2viz.graph_import import component_spec_from_graph as oracle_from_graph
    from spec2viz.graph_import import load_store_index

    root = _project(tmp_path / "p", SYNC_FIXTURES[:4])
    sync = SpecSync(root / ".sldb")
    for rel in SYNC_FIXTURES[:4]:
        sync.sync(root / "specs" / rel)
    nodes, edges = index_graph(sldb_api.load_edge_index(root / ".sldb"))
    assert (nodes, edges) == load_store_index(root / ".sldb")
    for options in ({}, {"models": ("SpecNodeDoc",), "drop_isolated": True}, {"exclude_relations": ("contains",)}):
        spec = component_spec_from_graph(nodes, edges, source=f"store {root}", **options)
        assert spec == oracle_from_graph(nodes, edges, source=f"store {root}", **options), options


def _imports_sldb_does_not_read(package: Path) -> tuple[set, set]:
    """The two sides of SV-F02's declared difference, read from the package's own source:
    (edges only sldb may add: plain imports and resolved relative imports;
     edges only spec2viz may add: nested `from` imports and unresolved relative ones)."""
    def node(module: str) -> str:
        return "module_" + module.replace(".", "_").replace("-", "_")

    sldb_only, spec2viz_only = set(), set()
    for path in sorted(package.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        module = str(path.relative_to(package).with_suffix("")).replace("/", ".")
        tree = ast.parse(path.read_text(encoding="utf-8"))
        top = {id(statement) for statement in tree.body}
        for statement in ast.walk(tree):
            if isinstance(statement, ast.Import) and id(statement) in top:
                sldb_only |= {(node(module), node(alias.name)) for alias in statement.names}
            elif isinstance(statement, ast.ImportFrom) and statement.level:
                base = module.split(".")[: -statement.level] + ([statement.module] if statement.module else [])
                sldb_only.add((node(module), node(".".join(base))))
                if statement.module:
                    spec2viz_only.add((node(module), node(statement.module)))
            elif isinstance(statement, ast.ImportFrom) and id(statement) not in top:
                spec2viz_only.add((node(module), node(statement.module)))
    return sldb_only, spec2viz_only


@pytest.mark.parity
def test_python_ast_generation_of_specir_matches_spec2viz_up_to_the_declared_differences() -> None:
    pytest.importorskip("spec2viz")
    from spec2viz.generators.python_ast import generate_python_ast_spec

    ours, findings = component_spec_from_python(PACKAGE, project_id="specir", title="specIR")
    oracle = generate_python_ast_spec(PACKAGE, project_id="specir", title="specIR")
    assert findings == []
    assert {k: v for k, v in ours.items() if k != "data"} == {k: v for k, v in oracle.items() if k != "data"}

    def internal(spec: dict) -> list:
        return [(key, node) for key, node in spec["data"]["nodes"].items() if node["kind"] != "external"]

    def edges(spec: dict, relation: str) -> list:
        return [(edge["from"], edge["to"]) for edge in spec["data"]["edges"] if edge["relation"] == relation]

    assert internal(ours) == internal(oracle)
    assert edges(ours, "defines") == edges(oracle, "defines")
    our_imports, oracle_imports = edges(ours, "imports"), edges(oracle, "imports")
    assert len(our_imports) == len(set(our_imports)), "sldb repeats an imports edge"
    sldb_only, spec2viz_only = _imports_sldb_does_not_read(PACKAGE)
    assert set(our_imports) - set(oracle_imports) <= sldb_only
    assert set(oracle_imports) - set(our_imports) <= spec2viz_only

FILE:tests/test_imports.py
"""specIR imports SLDB only through its public API (`sldb.api`), and never pron or spec2viz.

Until `sldb.api.notations` exports the diagram spec models of D3, `specir.visual.spec_models` is the
one module that imports them from `sldb.models.notation.diagram_specs` (and only from there). Until it
exports `resolve_style`, `load_palette` and `NotationError`, `specir.visual.notation_style` is the one
module that imports them from `sldb.notations` (and only from there).

The one exception is specIR's extension of the MCP server of sldb (`specir.mcp_extension`): it
is the only module that reaches `sldb.mcp` (the extension contract of `sldb mcp --extension`)
or `mcp`. specIR implements no MCP server of its own.

SpecSync and the component spec generator (from a graph, a snapshot or the Python AST) are sldb's
(D1, D2): specIR calls them from `sldb.api.notations` and defines none of them (IR13a)."""

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


#: What D1 and D2 migrated to `sldb.api.notations` (IR13a): specIR calls it there and defines none of it.
MIGRATED_TO_SLDB = (
    "SpecSync", "sync_spec", "sync_catalog", "check_catalog", "catalog_entries", "spec_elements", "spec_edges",
    "format_report", "component_spec_from_graph", "component_spec_from_python", "write_component_spec",
    "load_node_link", "load_node_link_graph", "load_store_index", "index_graph", "generate_python_ast_spec",
)


def test_specir_defines_no_spec_sync_and_no_spec_generator() -> None:
    defined = []
    for path in sorted(PACKAGE.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Assign)):
                names = [t.id for t in getattr(node, "targets", []) if isinstance(t, ast.Name)] or [getattr(node, "name", "")]
                defined += [f"{path.relative_to(PACKAGE.parent)}: {name}" for name in names if name in MIGRATED_TO_SLDB]
    assert not defined, defined
    assert not (PACKAGE / "visual" / "generators").exists() and not (PACKAGE / "visual" / "sync.py").exists()

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
#: The modules that reach spec2viz as the development oracle (IR11, IR12 and IR13a's sync and generation parity).
ORACLES = {TESTS / "visual" / "parity.py", TESTS / "visual" / "render_parity.py", TESTS / "visual" / "test_sync_generation_parity.py"}
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

FILE:src/specir/visual/__init__.py
"""specIR's visual layer: the intermediate representation, its compilers and the projections of
the graph to it (IR11); its renderers, mermaid linter, JSON Schema export, packaged resources and the
render, lint and schema commands are in `specir.visual.renderers`, `lint_mermaid`, `schema`,
`templates/`, `render_file` and `commands` (IR12). IR13d extends this module with the full public API of the layer.

The spec models of the eight diagram types are sldb's (D3) and are only re-exported here for the
visual layer's callers; nothing of them is defined in specIR. `load_spec` and `validate_spec` are
used from `sldb.api.notations` directly, without a wrapper. So are syncing a spec to the store
(`SpecSync`, `sync_spec`; `sldb notations sync --spec`, D1) and generating a component spec from a
graph, a snapshot or the Python AST (`component_spec_from_graph`, `component_spec_from_python`,
`write_component_spec`; `sldb notations from-graph`, D2): specIR defines none of them (IR13a)."""

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
| SV-E01 | SpecSync: materializar un spec como SpecDoc, SpecNodeDoc y RelationDoc, crear el RelationTypeDoc que falte y borrar lo que salió del spec; informe (`format_report`) | `spec2viz/sldb_sync.py` | migrado a sldb | D1: `SpecSync`, `sync_spec` en `sldb.api.notations`; `sldb notations sync --spec`. Reutiliza `StoreWriter` y `SyncReport` de sldb | `tests/test_sldb_sync.py` (16) portado a sldb, contra store real y sin mocks, en verde; informe igual campo a campo al de spec2viz sobre los mismos specs (D1); specIR llama a la API de sldb sin envoltorio (IR13a): `tests/visual/test_sync_generation_parity.py` sincroniza con sldb y con spec2viz los 14 specs válidos de `tests/fixtures/` y los ARQ/FLOW de `tests/test_sldb_sync.py` (con un resync que quita un nodo) y compara informes y SpecDoc, SpecNodeDoc, RelationDoc, RelationTypeDoc y documentos de notación; borrado al resincronizar y RelationTypeDoc de relación no builtin con `check_edges` limpio, contra store real. Diferencia declarada: la descripción del RelationTypeDoc que crea la sincronización ya no termina en «de spec2viz». |
| SV-E02 | Sincronización de notaciones y paletas al store (`NotationSync`, `PaletteSync`, `format_notation_report`) | `spec2viz/sldb_sync.py` | usar sldb directamente | `sldb.api.notations.NotationSync`, `PaletteSync`, `sync_notation`, `sync_palette`; CLI `sldb notations sync --notation/--palette` | Los casos de notación y paleta de `tests/test_sldb_sync.py` y `tests/test_style_palette.py` que sincronizan pasan llamando a la API de sldb, sin envoltorio en specIR. |

### F. Generación de specs

| ID | Capacidad | Fuente en spec2viz | Modo | Destino y tarea | Condición de retiro |
|---|---|---|---|---|---|
| SV-F01 | from-graph: compilar el grafo de un store (edge index) o un snapshot node-link en un spec de componentes | `spec2viz/graph_import.py` | migrado a sldb | D2: `component_spec_from_graph` en `sldb.api.notations`; `sldb notations from-graph --snapshot/--store` | `tests/test_graph_import.py` (21) portado a sldb y en verde; todo spec generado valida con el modelo de componentes de D3. IR13a (`tests/visual/test_sync_generation_parity.py`): sobre los snapshots node-link de `tests/test_graph_import.py` (el de documentos y `PY_GRAPH`) y sobre el edge index de un store sincronizado, `load_node_link`, `load_node_link_graph`, `index_graph` y `component_spec_from_graph` dan lo mismo que spec2viz, y cada spec valida con `load_spec`/`validate_spec`; sin diferencias. |
| SV-F02 | Generar un spec de componentes desde el AST de Python | `spec2viz/generators/python_ast.py` | migrado a sldb | D2: `component_spec_from_python` sobre `sldb.code.scan_tree`, `write_component_spec`; `sldb notations from-graph --python` | spec2viz no tiene pruebas de este generador: la condición es la prueba nueva de D2 que compara con `generate_python_ast_spec` de spec2viz sobre un árbol pequeño (mismos módulos, clases y relaciones defines) y valida con el modelo de D3. IR13a (`tests/visual/test_sync_generation_parity.py`) compara sobre un paquete real (`src/specir`): módulos, clases y aristas defines idénticos y en el mismo orden; el spec valida. Diferencias declaradas en las aristas imports, porque sldb las lee de `sldb.code.scan_tree`: cuenta los `import x` (spec2viz solo los `from x import y`), resuelve los imports relativos contra el paquete del módulo (spec2viz emite el nombre sin resolver), no repite una arista por sentencia y no lee los `from x import y` anidados bajo el nivel superior del módulo (en funciones, `if` o `try`; spec2viz recorre todo el árbol). Lo último es una pérdida pedida al desk de sldb (`code/scan-tree-nested-imports`); los nodos external siguen a las aristas. |

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
    # `code` brings tree-sitter, which sldb's Python AST spec generator (D2) needs (IR13a's tests).
    "structuredLanguageDB[mcp,code]",
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

FILE:instruccion
Cold-bundle de la tarea task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Sincronizar un spec con specIR deja en un store de prueba los mismos SpecDoc, SpecNodeDoc y RelationDoc que spec2viz sobre los fixtures de sincronización.
- Volver a sincronizar tras quitar un elemento del spec borra su SpecNodeDoc y sus RelationDoc.
- Una relación de tipo no builtin crea su RelationTypeDoc y el índice de aristas valida después de sincronizar.
- La compilación desde grafo produce, sobre el fixture de snapshot de spec2viz, un spec de componentes que valida y es equivalente al de spec2viz, o su reemplazo por proyección tiene la prueba equivalente declarada en la matriz.
- La generación desde AST produce, sobre un paquete Python de fixture, un spec de componentes equivalente al de spec2viz.
- El paquete no importa spec2viz.

