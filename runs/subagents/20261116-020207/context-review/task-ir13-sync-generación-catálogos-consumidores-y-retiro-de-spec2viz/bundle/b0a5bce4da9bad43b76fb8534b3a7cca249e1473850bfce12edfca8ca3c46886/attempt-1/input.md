FILE:desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
---
sldb:
  by: agent
  at: '2026-11-16T01:53:50Z'
  authority: generated
  via: save_document_payload
id: task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz
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
- task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs
- task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos
- task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual
- task-ir07-cobertura-completa-de-spec2viz-matriz-fuente-de-verdad-del-diagrama-y-gate-de-retiro
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/retirement.py
- src/specir/cli.py
- tests/visual/test_retirement_gate.py
- tests/visual/test_refs_models.py
- docs/spec2viz/acta-de-retiro.md
- docs/spec2viz/matriz-de-cobertura.md
- docs/spec2viz/gate-de-retiro.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13 Migración de consumidores y gate final de retiro de spec2viz

## Rationale

_Explain why this task exists or the business driver behind it._

Es el cierre de la migración: comprobar que nadie depende ya de spec2viz y que cada capacidad está cubierta. Esta tarea nació como una sola candidata que agrupaba sincronización, catálogos, notaciones, CLI y retiro; se partió para que cada tarea tenga un solo entregable. Las cuatro capacidades quedaron en las tareas IR13a, IR13b, IR13c e IR13d, autoradas desde la misma candidata del drawer, y aquí queda solo el entregable final: la migración de consumidores y el gate de retiro. El tipo task.aggregate no se pudo usar porque el tipo de una tarea no es editable; las dependencias cumplen el papel de agregación.

## Goal

_Describe the concrete result this task must produce._

Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.

## Scope

_State what is in scope and what is out of scope._

Dentro: comprobador del gate de retiro, que lee la matriz de cobertura y verifica que cada fila tiene su condición cumplida con una prueba citada, y que recorre en solo lectura el universo auditado buscando dependencias de spec2viz. Universo auditado: exactamente los repos consumidores y los stores que lista el inventario de consumidores de docs/spec2viz/matriz-de-cobertura.md, más el propio repo de specIR; un repo o store que no esté en ese inventario no se audita, y añadir uno exige actualizar primero el inventario. Qué cuenta como dependencia: importaciones de spec2viz en código (import spec2viz o from spec2viz); dependencias declaradas en configuración ejecutable (pyproject.toml, requirements, archivos de CI, Makefile y scripts); puntos de entrada y llamadas al comando spec2viz en código, scripts o configuración ejecutable; llamadas a su API Python; y modelos spec2viz.sldb_models registrados en un índice de store. Qué no cuenta: menciones en texto, documentación, comentarios, changelogs o documentos del desk. Salida: por cada dependencia remanente, el repo o store, la ruta del archivo, la línea y la clase de dependencia; con al menos una, el gate falla con código de salida distinto de cero y el retiro no se puede declarar; pedidos de migración a los desks de graph_ui, deskops y de cada repo con stores afectados; acta de retiro con la evidencia por fila y por consumidor; actualización de la matriz de cobertura con esa evidencia.
Fuera: implementar capacidades de spec2viz, que corresponden a las tareas de compiladores, renderers, IR13a, IR13b, IR13c e IR13d; editar archivos de otros repos; archivar o borrar el repo spec2viz, que es decisión de su dueño una vez cumplido el gate.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo src/specir/visual/retirement.py con el comprobador, expuesto como subcomando del comando de specIR; lee del inventario de la matriz de cobertura la lista de repos consumidores y de stores a revisar y recibe por argumento solo la ruta local de cada uno; no escribe en ellos. Si el gate falla, el acta registra las dependencias remanentes con su ruta y línea y deja el retiro como no declarado. Los cambios en otros repos se piden con deskops message send --to <repo> y se registran en docs/spec2viz/acta-de-retiro.md con la referencia al cambio que los resolvió. La matriz docs/spec2viz/matriz-de-cobertura.md se actualiza con la prueba que acredita cada fila. Propiedad de archivos compartidos: docs/spec2viz/matriz-de-cobertura.md ya existe cuando esta tarea empieza: la crea la tarea de cobertura (IR07). Aquí solo se actualiza, añadiendo por fila la prueba y la evidencia de cumplimiento, después de cerradas IR13a, IR13b, IR13c e IR13d; no se cambian los modos ni las condiciones de retiro que fijó IR07 sin registrarlo en el acta. Propiedad de archivo compartido: src/specir/cli.py lo crea la tarea IR13d con la base del comando y sus subcomandos; esta tarea agrega ahí solo el subcomando del gate de retiro, después de cerrada IR13d, de la que depende, sin modificar los subcomandos existentes.

Precisiones (preflight-3, resueltas por el worker de IR13 el 2026-11-15):
1. IR13c se retiró (sus filas pasaron a «usar sldb directamente»); no bloquea. Las dependencias son las del frontmatter.
2. El subcomando es `specir retirement check [--matrix docs/spec2viz/matriz-de-cobertura.md] --path NOMBRE=RUTA ...`. El inventario es la tabla «Inventario de consumidores» de la matriz: la primera palabra de la primera columna es el repo y `store `<ruta>`` es un store (su carpeta `.sldb`). El repo de specIR es el que contiene la matriz y no necesita `--path`. Si se da un nombre que no está en el inventario o falta uno que sí está, es un error de uso (código 2). Con alguna dependencia o fila sin acreditar sale con 1; si no hay ninguna, con 0.
3. Detección: Python por AST (`import`/`from spec2viz…`, `importorskip`/`import_module("spec2viz…")`, llamadas cuyo primer argumento es el comando `spec2viz` o una lista que empieza por él, salvo métodos de cadena); requisitos en `pyproject.toml`, `setup.cfg`, `setup.py`, `requirements*.txt` y CI; `spec2viz <subcomando>` en sh, Makefile y CI; habilidades (`SKILL.md` y `references/` de una skill) que nombran `spec2viz <subcomando>` como código o se llaman como spec2viz; `spec2viz.sldb_models` en `store.yaml`, `core/store_index.yaml` y `core/models/*.yaml`. No se miran `.git`, entornos, `build`, `dist`, `.sldb` ni archivos de texto.
4. La acreditación es la sección «Acreditación (IR13)» de la matriz: una fila por SV-* con estado (cumplida o abierta), la prueba que la acredita y lo que falta. Una fila cumplida debe citar al menos un `tests/….py`. Los modos y las condiciones de IR07 no cambian.
5. Paridad (G2): una fila se cumple si las pruebas citadas en su condición pasan, contra specIR o contra sldb (portadas). Lo que no está portado deja la fila abierta.

Estado (IR13, 2026-11-15): gate no cumplido; retiro no declarado (`docs/spec2viz/acta-de-retiro.md`). Comprobador y pruebas hechos. 75 filas cumplidas y 30 abiertas. G6 cumplido; G1, G2, G3, G4, G5 y G7 abiertos. `specir retirement check` sobre el universo real sale con rc 1: 122 dependencias y 30 filas abiertas. Se enviaron los pedidos a deskops, graph_ui, pron, sldb y spec2viz, y la medición de `catalog build` a sldb. La tarea sigue abierta hasta que se cumpla el gate.

## Validation

_List the checks required before this task can close._

- El comprobador falla sobre una matriz de entrada con una fila sin prueba citada y pasa cuando todas la tienen.
- Sobre un repo de entrada con una importación de spec2viz en código, una dependencia en pyproject.toml y una llamada al comando spec2viz en un script, y un índice de store con un modelo spec2viz.sldb_models, el comprobador reporta las cuatro con repo, ruta, línea y clase de dependencia, termina con código de salida distinto de cero y no modifica ningún archivo.
- Sobre un repo de entrada que solo menciona spec2viz en documentación, comentarios y un changelog, el comprobador no reporta ninguna dependencia.
- El comprobador audita exactamente los repos y stores del inventario de la matriz de cobertura más el repo de specIR, y falla con un error que lo dice si se le pide auditar uno que no está en el inventario o si falta la ruta de uno que sí está.
- Ejecutado sobre todos los repos y stores reales del inventario, el comprobador no reporta ninguna dependencia y termina con código de salida cero.
- La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado en la matriz de cobertura.
- El acta de retiro lista, por cada consumidor del inventario, el mensaje enviado a su desk, la referencia del cambio que lo resolvió y la salida del comprobador; si quedó alguna dependencia, el acta dice que el retiro no está declarado.
- Toda fila de la matriz de cobertura tiene su condición de retiro cumplida y su prueba citada.

## Done When

_Name the observable condition that makes the task complete._

El comprobador termina con código de salida cero sobre todo el universo auditado, el acta de retiro está completa y declara el retiro, y spec2viz puede archivarse sin que ningún repo del workspace falle.

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

FILE:desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
---
sldb:
  by: agent
  at: '2026-11-12T01:22:50Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk
status: active
summary: Frontera de edición de las tareas de specIR.
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- system:specir
---

# Guardrail: los cambios en otros repos se piden por su desk

## What

_Define the context or guardrail this pill carries._

Una tarea de specIR solo crea o modifica archivos dentro del repo de specIR. Lo que deba cambiar en SLDB, graph_ui, deskops, spec2viz u otro repo se pide con un mensaje a su desk y se registra como evidencia.

## Why

_Explain why this context matters for safe execution._

Cada desk es dueño de sus tareas; editar otro repo desde aquí salta sus gates y deja el cambio sin dueño.

## When

_Describe when an agent should apply this pill._

Cuando una tarea detecta una carencia en SLDB o necesita que un consumidor de spec2viz migre.

## Where

_Name the files, surfaces, or scope this pill applies to._

Fuera de specIR: sldb/, UIs/graph_ui/, deskops/, spec2viz/ y los stores de otros repos.

## How

_Describe the correct way to apply this guidance._

deskops message send --to <repo> con el pedido concreto y la referencia a la tarea de specIR; el criterio de validación de la tarea se cumple con la evidencia del cambio hecho por el otro repo.

## How Not

_Describe the shortcut or failure mode to avoid._

No editar archivos de otros repos; no listar rutas de otros repos en el campo files de una tarea de specIR; no dar por cumplido un criterio externo sin evidencia.

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

FILE:src/specir/visual/retirement.py
"""The retirement gate of spec2viz (IR13): who still depends on spec2viz, and which rows of the coverage
matrix are not accredited yet.

The universe audited is exactly the «Inventario de consumidores» of
`docs/spec2viz/matriz-de-cobertura.md` (its repos and its `store <path>` rows) plus specIR's own repo,
the one that holds the matrix. Each one is read from the local path given for it; nothing is written.

What counts as a dependency (and nothing else):

- `importación`: `import spec2viz…`/`from spec2viz… import` in Python code, and the dynamic forms
  `importorskip("spec2viz…")`/`import_module("spec2viz…")`;
- `dependencia declarada`: spec2viz as a requirement in `pyproject.toml`, `setup.cfg`, `setup.py`,
  `requirements*.txt` or a CI file (`.github/**/*.yml`, `.gitlab-ci.yml`);
- `invocación del comando`: a Python call whose command is `spec2viz` (`run("spec2viz", …)`,
  `subprocess.run(["spec2viz", …])`, `os.system("spec2viz …")`, `shutil.which("spec2viz")`), and
  `spec2viz <subcommand>` in a shell script, a Makefile or a CI file;
- `habilidad de agente`: a `SKILL.md` (or a file under a skill's `references/`) that tells an agent to run
  `spec2viz <subcommand>` (as inline code or in a fenced block), or a skill named after spec2viz
  (`name: use-spec2viz`);
- `modelo registrado`: `spec2viz.sldb_models` in a store's `store.yaml`, `core/store_index.yaml` or
  `core/models/*.yaml`.

Mentions in prose, documentation, comments, docstrings, changelogs and desk documents do not count.

The matrix is accredited when every `SV-*` row has an entry in its «Acreditación (IR13)» table whose
state is `cumplida` and that cites at least one test (`tests/….py`)."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

#: The audited repo that is always there: the one that holds the matrix.
SPECIR = "IR"
MATRIX = Path("docs") / "spec2viz" / "matriz-de-cobertura.md"
INVENTORY_HEADING = "## Inventario de consumidores"
ACCREDITATION_HEADING = "## Acreditación (IR13)"
DONE = "cumplida"

IMPORT = "importación"
DECLARED = "dependencia declarada"
INVOCATION = "invocación del comando"
SKILL = "habilidad de agente"
MODEL = "modelo registrado"

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "build", "dist", ".sldb", ".tox",
             ".mypy_cache", ".pytest_cache", ".ruff_cache", "site-packages"}
SUBCOMMANDS = "about|build|catalog|diagram|lint|notation|palette|render|schema|validate"
#: `spec2viz <subcommand>` at a command position of a shell line.
SHELL_CALL = re.compile(rf"(?:^|[\s;&|(`\"'$])spec2viz\s+(?:{SUBCOMMANDS})\b")
#: spec2viz as a requirement: `spec2viz>=0.1`, `"spec2viz"`, `egg=spec2viz`, `pip install spec2viz`.
REQUIREMENT = re.compile(
    r"egg=spec2viz\b"
    r"|pip\s+install\b.*(?<![\w./-])spec2viz(?![\w-])"
    r"|[\"']spec2viz\s*(?:\[[^\]]*\])?\s*(?:[<>=!~]=?[^\"']*)?(?:@[^\"']*)?(?:;[^\"']*)?[\"']"
    r"|^\s*spec2viz\s*(?:\[[^\]]*\])?\s*(?:[<>=!~]=?|@|;|=|$)")
#: `spec2viz <subcommand>` as code in a skill: inline code, or any line of a fenced block.
SKILL_CALL = re.compile(rf"`spec2viz\s+(?:{SUBCOMMANDS})\b")
#: Calls whose first argument is a string but that run nothing (string, path and regex methods).
NOT_A_RUN = {"startswith", "endswith", "split", "rsplit", "replace", "find", "rfind", "index", "count", "partition",
             "rpartition", "strip", "lstrip", "rstrip", "join", "format", "get", "removeprefix", "removesuffix",
             "search", "match", "fullmatch", "compile", "sub", "findall", "glob", "rglob", "joinpath", "append"}
CI_NAMES = {".gitlab-ci.yml", ".travis.yml", "azure-pipelines.yml", "Jenkinsfile"}
CONFIG_NAMES = {"pyproject.toml", "setup.cfg", "setup.py", "tox.ini", "Pipfile"}


class InventoryError(ValueError):
    """The paths given do not match the inventory of the matrix."""


@dataclass(frozen=True, order=True)
class Dependency:
    owner: str
    path: str
    line: int
    kind: str
    text: str = field(compare=False)

    def __str__(self) -> str:
        return f"{self.owner}\t{self.path}:{self.line}\t{self.kind}\t{self.text}"


@dataclass
class Report:
    repos: list[str]
    stores: list[str]
    dependencies: list[Dependency]
    open_rows: list[str]

    @property
    def ok(self) -> bool:
        return not self.dependencies and not self.open_rows


# --- the matrix ----------------------------------------------------------------------------------


def _section(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return []
    body = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return body


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _table_rows(lines: list[str]) -> list[list[str]]:
    rows = [_cells(line) for line in lines if line.startswith("|")]
    return [row for row in rows[2:] if row and not set(row[0]) <= set("-: ")] if rows else []


def inventory(text: str) -> tuple[list[str], list[str]]:
    """The repos and the stores of the inventory, in order of first appearance."""
    repos: list[str] = []
    stores: list[str] = []
    for row in _table_rows(_section(text, INVENTORY_HEADING)):
        first = row[0]
        store = re.match(r"store\s+`([^`]+)`", first)
        name = store.group(1) if store else first.split()[0].strip("`")
        target = stores if store else repos
        if name and name not in target:
            target.append(name)
    if not repos and not stores:
        raise InventoryError(f"the matrix has no «{INVENTORY_HEADING[3:]}» table")
    return repos, stores


def matrix_rows(text: str) -> list[str]:
    return [_cells(line)[0] for line in text.splitlines() if line.startswith("| SV-")]


def accreditation(text: str) -> dict[str, tuple[str, str]]:
    """Each row id of the accreditation table with its state and the evidence it cites."""
    entries = {}
    for row in _table_rows(_section(text, ACCREDITATION_HEADING)):
        if len(row) >= 3:
            entries[row[0].strip("`")] = (row[1].lower(), row[2])
    return entries


def open_rows(text: str) -> list[str]:
    """The rows of the matrix that are not `cumplida` with a cited test, each with why."""
    entries = accreditation(text)
    problems = []
    for row in matrix_rows(text):
        state, evidence = entries.get(row, ("", ""))
        if not state:
            problems.append(f"{row}: sin entrada en la acreditación")
        elif state != DONE:
            problems.append(f"{row}: {state}")
        elif not re.search(r"tests/[\w./-]+\.py", evidence):
            problems.append(f"{row}: cumplida sin prueba citada")
    return problems


# --- dependencies --------------------------------------------------------------------------------


def _is_spec2viz_module(name: str | None) -> bool:
    return bool(name) and name.split(".")[0] == "spec2viz"


def _command_of(node: ast.expr) -> bool:
    """Whether an argument of a call names the spec2viz command."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value == "spec2viz" or node.value.startswith("spec2viz ")
    if isinstance(node, (ast.List, ast.Tuple)) and node.elts:
        head = node.elts[0]
        return isinstance(head, ast.Constant) and head.value == "spec2viz"
    return False


def _python(owner: str, rel: str, source: str) -> list[Dependency]:
    lines = source.splitlines()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [Dependency(owner, rel, n, IMPORT, line.strip()) for n, line in enumerate(lines, 1)
                if re.match(r"\s*(import|from)\s+spec2viz\b", line)]
    found = []

    def add(node: ast.AST, kind: str) -> None:
        found.append(Dependency(owner, rel, node.lineno, kind, lines[node.lineno - 1].strip()))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(_is_spec2viz_module(a.name) for a in node.names):
            add(node, IMPORT)
        elif isinstance(node, ast.ImportFrom) and not node.level and _is_spec2viz_module(node.module):
            add(node, IMPORT)
        elif isinstance(node, ast.Call) and node.args:
            func = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
            first = node.args[0]
            if func in ("importorskip", "import_module", "__import__"):
                if isinstance(first, ast.Constant) and isinstance(first.value, str) and _is_spec2viz_module(first.value):
                    add(node, IMPORT)
            elif func not in NOT_A_RUN and _command_of(first):
                add(node, INVOCATION)
    return found


def _lines(owner: str, rel: str, source: str, pattern: re.Pattern, kind: str, comment: str = "#") -> list[Dependency]:
    return [Dependency(owner, rel, n, kind, line.strip()) for n, line in enumerate(source.splitlines(), 1)
            if not line.lstrip().startswith(comment) and pattern.search(line)]


def _skill(owner: str, rel: str, source: str) -> list[Dependency]:
    found, fenced = [], False
    for n, line in enumerate(source.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        named = n < 10 and re.match(r"name:\s*\S*spec2viz", line)  # the skill itself is spec2viz's (use-spec2viz)
        if named or (SHELL_CALL if fenced else SKILL_CALL).search(line):
            found.append(Dependency(owner, rel, n, SKILL, line.strip()))
    return found


def _is_skill(rel: Path) -> bool:
    return rel.name == "SKILL.md" or ("skills" in rel.parts and "references" in rel.parts and rel.suffix == ".md")


def _is_ci(rel: Path) -> bool:
    return rel.name in CI_NAMES or (rel.parts[:1] == (".github",) and rel.suffix in (".yml", ".yaml"))


def scan_repo(owner: str, root: Path) -> list[Dependency]:
    """Every dependency on spec2viz in the repo at `root`, read-only."""
    found: list[Dependency] = []
    for path in sorted(_files(root)):
        rel = path.relative_to(root)
        name = rel.name
        kinds = []
        if name.endswith(".py"):
            kinds.append("python")
        if name in CONFIG_NAMES - {"setup.py"} or re.match(r"requirements.*\.(txt|in)$", name):
            kinds.append("config")
        if _is_ci(rel):
            kinds += ["config", "shell"]
        if name.endswith(".sh") or name in ("Makefile", "makefile", "justfile", "Justfile"):
            kinds.append("shell")
        if _is_skill(rel):
            kinds.append("skill")
        if not kinds:
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "spec2viz" not in source:
            continue
        rel_s = rel.as_posix()
        if "python" in kinds:
            found += _python(owner, rel_s, source)
            if name == "setup.py":
                found += _lines(owner, rel_s, source, REQUIREMENT, DECLARED)
        if "config" in kinds:
            found += _lines(owner, rel_s, source, REQUIREMENT, DECLARED)
        if "shell" in kinds:
            found += _lines(owner, rel_s, source, SHELL_CALL, INVOCATION)
        if "skill" in kinds:
            found += _skill(owner, rel_s, source)
    return sorted(set(found))


def _files(root: Path):
    stack = [root]
    while stack:
        directory = stack.pop()
        try:
            entries = list(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_symlink():
                continue
            if entry.is_dir():
                if entry.name not in SKIP_DIRS:
                    stack.append(entry)
            elif entry.is_file():
                yield entry


def scan_store(owner: str, store: Path) -> list[Dependency]:
    """The models of `spec2viz.sldb_models` registered in the store at `store` (its `.sldb` folder)."""
    files = [store / "store.yaml", store / "core" / "store_index.yaml", *sorted((store / "core" / "models").glob("*.yaml"))]
    found = []
    for path in files:
        if path.is_file():
            source = path.read_text(encoding="utf-8")
            found += _lines(owner, path.relative_to(store).as_posix(), source, re.compile(r"spec2viz\.sldb_models\b"), MODEL)
    return found


# --- the gate ------------------------------------------------------------------------------------


def check(matrix: Path, paths: dict[str, Path]) -> Report:
    """Audit the inventory of `matrix` (its repos and stores at `paths`) plus specIR's repo.

    `paths` maps each name of the inventory to its local path; specIR's repo is the one that holds
    the matrix and needs no path. A name outside the inventory, or a name of it without a path, is an
    `InventoryError`."""
    text = matrix.read_text(encoding="utf-8")
    repos, stores = inventory(text)
    specir_root = matrix.resolve().parents[len(MATRIX.parts) - 1]
    if SPECIR not in repos:
        repos.append(SPECIR)
    expected = (set(repos) - {SPECIR}) | set(stores)
    unknown = sorted(set(paths) - expected - {SPECIR})
    if unknown:
        raise InventoryError(f"not in the inventory of {matrix.name}: {', '.join(unknown)}")
    missing = sorted(expected - set(paths))
    if missing:
        raise InventoryError(f"no path given for: {', '.join(missing)}")
    roots = {name: Path(paths.get(name, specir_root)) for name in [*repos, *stores]}
    absent = sorted(name for name, root in roots.items() if not root.is_dir())
    if absent:
        raise InventoryError(f"path not found for: {', '.join(f'{n}={roots[n]}' for n in absent)}")
    dependencies = [dep for name in repos for dep in scan_repo(name, roots[name])]
    dependencies += [dep for name in stores for dep in scan_store(name, roots[name])]
    return Report(repos, stores, dependencies, open_rows(text))


def format_gate_report(report: Report) -> str:
    lines = [f"audited repos: {', '.join(report.repos)}", f"audited stores: {', '.join(report.stores) or '-'}"]
    lines += [f"dependencies: {len(report.dependencies)}"] + [f"  {dep}" for dep in report.dependencies]
    lines += [f"rows not accredited: {len(report.open_rows)}"] + [f"  {row}" for row in report.open_rows]
    lines.append("gate: " + ("passed, the retirement can be declared" if report.ok else "failed, the retirement is not declared"))
    return "\n".join(lines)


__all__ = ["Dependency", "InventoryError", "Report", "accreditation", "check", "format_gate_report", "inventory",
           "matrix_rows", "open_rows", "scan_repo", "scan_store"]

FILE:src/specir/cli.py
"""The `specir` command: the visual layer's CLI, with the taxonomy of spec2viz's (IR13d).

- `diagram` (render, validate, lint, schema) and `catalog` (schema) are IR12's groups
  (`specir.visual.commands`); this module mounts them and adds `catalog build` (IR13b's page, with
  the option to save its annotations through `sldb serve`), the top-level aliases `render`,
  `validate`, `lint`, `schema` and `build`, and `about`.
- `retirement check` (IR13) is the retirement gate of spec2viz (`specir.visual.retirement`): it audits,
  read-only, the inventory of the coverage matrix plus specIR's repo, and the matrix's accreditation.
- What spec2viz's CLI did that is sldb's has no command here, by design (JP: no wrapper over sldb's
  CLI or API): syncing a spec, a notation, a palette or a catalog (`sldb notations sync --spec`,
  `--notation`, `--palette`, `--catalog [--check]`), generating a spec from a graph or from Python
  (`sldb notations from-graph`), listing notations and palettes (`sldb notations list`), resolving a
  view (`sldb notations view`) and serving the catalog's annotations (`sldb serve`). The table is
  `docs/spec2viz/correspondencia-cli.md`.
- `diagram validate` (and `validate`) runs sldb's `load_spec`/`validate_spec` and redefines
  nothing: sldb has no command that validates a spec yet (SV-K16); when it has one, it goes."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from specir.visual.commands import (
    DIAGRAM_RENDERERS,
    _lint_paths,
    _render_paths,
    _validate_paths,
    _write_schema,
    catalog,
    diagram,
)

#: The top-level aliases, each with the group command it stands for (spec2viz's legacy commands).
ALIASES = {"render": "diagram render", "validate": "diagram validate", "lint": "diagram lint", "schema": "diagram schema",
           "build": "catalog build"}


@click.group(
    help=(
        "specIR CLI: semantic diagram specs -> diagrams -> catalog HTML.\n\n"
        "\b\nTaxonomy:\n"
        "- diagram: semantic diagram specs (render, validate, lint, schema)\n"
        "- catalog: HTML bundles and hierarchical diagram stores (build, schema)\n\n"
        "Top-level aliases (render, validate, lint, schema, build) remain available for compatibility.\n\n"
        "Syncing specs, notations, palettes and catalogs into a store, generating specs from a graph "
        "or from Python, resolving views and serving annotations are sldb's: use `sldb notations ...` "
        "and `sldb serve` directly."
    )
)
@click.version_option(package_name="specir", prog_name="specir")
def main():
    pass


main.add_command(diagram)
main.add_command(catalog)


@main.command("about", short_help="Where diagrams live and how the flow reaches HTML.")
def about():
    """Point to where the diagrams live and the full spec -> HTML flow, with sldb's commands for the store."""
    from sldb.api.notations import find_store

    cwd = Path.cwd()
    store = find_store(cwd)
    click.echo("specir — semantic specs -> diagrams -> catalog HTML (specIR's visual layer over sldb)\n")

    click.echo("Where the diagrams live:")
    click.echo("  spec files       : YAML specs (`type:` one of the eight diagram types) next to their vistas.yml")
    click.echo(f"  store            : {store if store else f'no .sldb store above {cwd}'}")
    click.echo("  specs in a store : SpecDoc documents (`sldb notations list --store <.sldb>`)")
    click.echo("  catalog config   : a vistas.yml registry or a project.yml / diagram-store config\n")

    click.echo("Flow to HTML:")
    click.echo("  1. specir diagram validate <spec.yml>")
    click.echo("  2. specir diagram render   <spec.yml> --out <dir>")
    click.echo("  3. specir diagram lint     <rendered.mmd>")
    click.echo("  4. specir catalog build    --config <vistas.yml> --out <out.html>")
    click.echo("     (build alias = catalog build; --atoms-dir injects window.ATOMS_DB)\n")

    click.echo("Into the store (sldb, used directly):")
    click.echo("  sldb notations sync --spec <spec.yml> --store <.sldb>")
    click.echo("  sldb notations sync --catalog <vistas.yml> [--check] --store <.sldb>")
    click.echo("  sldb notations from-graph --python <src_dir> | --store <.sldb> | --snapshot <graph.json>")
    click.echo("  sldb notations view <SpecDoc id> --store <.sldb>\n")

    click.echo("Save a built catalog's annotations (replaces spec2viz's `catalog serve`):")
    click.echo("  sldb models add specir.visual.catalog.annotations:CatalogAnnotationsDoc --store <.sldb>")
    click.echo("  sldb serve --store <.sldb> --cors --port 8765")
    click.echo("  specir catalog build --config <vistas.yml> --out <out.html> --sldb-url http://127.0.0.1:8765")


# ── catalog build and its alias ─────────────────────────────────────────────────────────────────


def _build_catalog(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...],
                   strict_atoms: bool, annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    from specir.visual.catalog import AnnotationsTarget, build_catalog

    target = AnnotationsTarget(server=sldb_url or "", doc=annotations_doc or "") if (annotations or sldb_url or annotations_doc) else None
    try:
        build_catalog(config, out, base_dir, atoms_dir, list(atoms_tags) or None, strict_atoms, target)
        click.echo(f"Rendered catalog -> {out}")
    except Exception as exc:
        click.echo(f"Error building catalog: {exc}", err=True)
        sys.exit(1)


def _catalog_build_options(function):
    options = [
        click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="Path to a legacy vistas.yml registry or a hierarchical diagram store config."),
        click.option("--out", required=True, type=click.Path(path_type=Path), help="HTML file to write."),
        click.option("--base-dir", type=click.Path(exists=True, path_type=Path), help="Base directory for template and vista source paths. Defaults to the config file directory."),
        click.option("--atoms-dir", type=click.Path(exists=True, path_type=Path), help="Directory with W5H1 atom markdown files to inject as window.ATOMS_DB."),
        click.option("--atoms-tag", "atoms_tags", multiple=True, help="Embed only atoms carrying this tag (full `ns:value` or just `value`); repeatable. Default: all atoms."),
        click.option("--strict-atoms", is_flag=True, help="Fail the build if a spec `atoms:` id does not exist among the loaded atoms (default: warning)."),
        click.option("--annotations", is_flag=True, help="Save the page's annotations in an sldb store through `sldb serve`; the server and the document can also come from the page URL (`?sldb=<url>&annotations=<id>`)."),
        click.option("--sldb-url", default=None, help="Base URL of `sldb serve --cors` that keeps the annotations (implies --annotations)."),
        click.option("--annotations-doc", default=None, help="Id of the CatalogAnnotationsDoc that holds them (implies --annotations). Default: derived from the catalog's name."),
    ]
    for option in reversed(options):
        function = option(function)
    return function


@catalog.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@_catalog_build_options
def catalog_build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool,
                  annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    """Build a diagram catalog HTML bundle from a vistas registry or diagram store."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations, sldb_url, annotations_doc)


@main.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@_catalog_build_options
def build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool,
          annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    """Legacy alias for `catalog build`."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations, sldb_url, annotations_doc)


# ── the other top-level aliases ─────────────────────────────────────────────────────────────────


@main.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option("--renderer", "--backend", type=click.Choice(DIAGRAM_RENDERERS), default=None, help="Force a renderer instead of using the spec type default.")
def render(paths: list[Path], out: Path, renderer: str | None):
    """Legacy alias for `diagram render`."""
    _render_paths(paths, out, renderer)


@main.command("validate", short_help="Validate semantic diagram spec files (sldb's load_spec and validate_spec).")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def validate_cmd(paths: list[Path]):
    """Legacy alias for `diagram validate`."""
    _validate_paths(paths)


@main.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def lint_cmd(paths: list[Path]):
    """Legacy alias for `diagram lint`."""
    _lint_paths(paths)


@main.command("schema", short_help="Export JSON Schema for semantic specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one type: class, sequence, state, component, activity, deployment, component_view_matrix, or diagram-store.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def schema(diagram_type: str | None, out: Path | None):
    """Legacy schema entrypoint for diagram specs and diagram stores."""
    _write_schema(diagram_type, out)


@main.group("retirement", short_help="The retirement gate of spec2viz (IR13).")
def retirement():
    """The retirement gate of spec2viz: `docs/spec2viz/gate-de-retiro.md`."""


@retirement.command("check", short_help="Audit the consumers and stores of the inventory and the matrix's accreditation.")
@click.option("--matrix", default=str(Path("docs") / "spec2viz" / "matriz-de-cobertura.md"), show_default=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path), help="The coverage matrix; its repo is specIR's.")
@click.option("--path", "paths", multiple=True, metavar="NAME=PATH",
              help="Local path of each repo and store of the matrix's inventory (a store's path is its .sldb folder).")
def retirement_check(matrix: Path, paths: tuple[str, ...]):
    """Report every remaining dependency on spec2viz (repo or store, path, line and kind) and every row
    of the matrix not accredited; exit 1 when there is one, 0 when the retirement can be declared.
    Nothing is written."""
    from specir.visual.retirement import InventoryError, check, format_gate_report

    given: dict[str, Path] = {}
    for item in paths:
        name, sep, value = item.partition("=")
        if not sep or not name or not value:
            raise click.UsageError(f"--path takes NAME=PATH, not {item!r}")
        given[name] = Path(value)
    try:
        report = check(matrix, given)
    except InventoryError as exc:
        raise click.UsageError(str(exc)) from exc
    click.echo(format_gate_report(report))
    sys.exit(0 if report.ok else 1)


__all__ = ["ALIASES", "main"]


if __name__ == "__main__":
    main()

FILE:tests/visual/test_retirement_gate.py
"""The retirement gate of spec2viz (IR13): `specir.visual.retirement` and `specir retirement check`.

Synthetic repos and stores are built in tmp; the real run audits the inventory of
`docs/spec2viz/matriz-de-cobertura.md` in the workspace and is a strict xfail while a dependency or a
row not accredited remains (`docs/spec2viz/acta-de-retiro.md`)."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from click.testing import CliRunner

from specir.cli import main
from specir.visual.retirement import (
    DECLARED,
    IMPORT,
    INVOCATION,
    MODEL,
    SKILL,
    InventoryError,
    check,
    inventory,
    open_rows,
)

REPO = Path(__file__).resolve().parents[2]
WORKSPACE = REPO.parent
MATRIX = REPO / "docs" / "spec2viz" / "matriz-de-cobertura.md"

ROWS = """## Matriz

| ID | Capacidad | Fuente | Modo | Destino | Condición |
|---|---|---|---|---|---|
| SV-A01 | a | `x.py` | migrar tal cual | IR | c |
| SV-A02 | b | `y.py` | reemplazar | IR | c |
"""

INVENTORY = """## Inventario de consumidores

| Consumidor | Archivo y línea | Clase | Sustituto previsto |
|---|---|---|---|
| app | `app/x.py:1` | importación | sldb |
| app | `app/pyproject.toml:3` | dependencia declarada | quitar |
| store `app/.sldb` | `store.yaml:4` | modelos | sldb |
"""


def accreditation(second: str) -> str:
    return f"""## Acreditación (IR13)

| Fila | Estado | Prueba que la acredita | Falta |
|---|---|---|---|
| `SV-A01` | cumplida | `tests/visual/test_api.py` (31 passed) | - |
{second}
"""


def specir_repo(tmp_path: Path, second: str = "| `SV-A02` | cumplida | `tests/visual/test_cli.py` | - |") -> Path:
    matrix = tmp_path / "IR" / "docs" / "spec2viz" / "matriz-de-cobertura.md"
    matrix.parent.mkdir(parents=True)
    matrix.write_text(f"# Matriz\n\n{ROWS}\n{INVENTORY}\n{accreditation(second)}", encoding="utf-8")
    return matrix


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def app_with_every_dependency(tmp_path: Path) -> tuple[Path, Path]:
    app = tmp_path / "app"
    write(app / "pkg" / "view.py", "import json\n\nfrom spec2viz.notation_view import resolve_view\n")
    write(app / "pyproject.toml", '[project]\nname = "app"\ndependencies = [\n  "spec2viz>=0.1.0",\n]\n')
    write(app / "scripts" / "build.sh", "#!/bin/sh\nset -e\nspec2viz diagram render specs/*.yml --out out\n")
    store = app / ".sldb"
    write(store / "store.yaml", "models:\n- name: SpecDoc\n  model_ref: spec2viz.sldb_models:SpecDoc\n")
    return app, store


def snapshot(root: Path) -> dict[str, str]:
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file()}


def test_the_inventory_names_the_repos_and_the_stores_of_the_matrix() -> None:
    assert inventory(INVENTORY) == (["app"], ["app/.sldb"])
    repos, stores = inventory(MATRIX.read_text(encoding="utf-8"))
    assert {"graph_ui", "deskops", "pron", "sldb", "IR"} <= set(repos)
    assert stores == ["spec2viz/.sldb"]


def test_a_row_without_a_cited_test_fails_and_passes_once_every_row_has_one(tmp_path: Path) -> None:
    text = f"{ROWS}\n{accreditation('| `SV-A02` | cumplida | la ayuda lo muestra | - |')}"
    assert open_rows(text) == ["SV-A02: cumplida sin prueba citada"]
    assert open_rows(f"{ROWS}\n{accreditation('')}") == ["SV-A02: sin entrada en la acreditación"]
    assert open_rows(f"{ROWS}\n{accreditation('| `SV-A02` | abierta | - | falta el pedido |')}") == ["SV-A02: abierta"]
    assert open_rows(f"{ROWS}\n{accreditation('| `SV-A02` | cumplida | `tests/visual/test_cli.py` | - |')}") == []


def test_every_dependency_is_reported_with_repo_path_line_and_kind_and_nothing_is_written(tmp_path: Path) -> None:
    matrix = specir_repo(tmp_path)
    app, store = app_with_every_dependency(tmp_path)
    before = snapshot(tmp_path)
    report = check(matrix, {"app": app, "app/.sldb": store})
    found = {(d.owner, d.path, d.line, d.kind) for d in report.dependencies}
    assert found == {
        ("app", "pkg/view.py", 3, IMPORT),
        ("app", "pyproject.toml", 4, DECLARED),
        ("app", "scripts/build.sh", 3, INVOCATION),
        ("app/.sldb", "store.yaml", 3, MODEL),
    }
    assert not report.ok
    result = CliRunner().invoke(main, ["retirement", "check", "--matrix", str(matrix), "--path", f"app={app}", "--path", f"app/.sldb={store}"])
    assert result.exit_code == 1, result.output
    assert "app\tpkg/view.py:3\timportación" in result.output
    assert "gate: failed" in result.output
    assert snapshot(tmp_path) == before


def test_python_calls_dynamic_imports_ci_and_skills_count(tmp_path: Path) -> None:
    matrix = specir_repo(tmp_path)
    app = tmp_path / "app"
    write(app / "tests" / "test_x.py", (
        "import subprocess, pytest\n"
        "spec2viz = pytest.importorskip('spec2viz')\n"
        "subprocess.run(['spec2viz', 'diagram', 'sync', 'a.yml'], check=True)\n"
        "def run(*args): ...\n"
        "run('spec2viz', 'catalog', 'build')\n"
    ))
    write(app / ".github" / "requirements-suite.txt", "-e git+https://example.invalid/spec2viz@master#egg=spec2viz\n")
    write(app / ".github" / "workflows" / "ci.yml", "jobs:\n  b:\n    steps:\n      - run: spec2viz catalog build --config c.yml\n")
    write(app / ".claude" / "skills" / "use-it" / "SKILL.md", "# Use\n\nRun `spec2viz diagram render spec.yml`.\nA spec2viz diagram spec is YAML.\n")
    write(app / ".opencode" / "skills" / "use-spec2viz" / "SKILL.md", "---\nname: use-spec2viz\n---\n\nUse spec2viz.\n")
    store = tmp_path / "app" / ".sldb"
    store.mkdir()
    found = {(d.path, d.line, d.kind) for d in check(matrix, {"app": app, "app/.sldb": store}).dependencies}
    assert found == {
        ("tests/test_x.py", 2, IMPORT),
        ("tests/test_x.py", 3, INVOCATION),
        ("tests/test_x.py", 5, INVOCATION),
        (".github/requirements-suite.txt", 1, DECLARED),
        (".github/workflows/ci.yml", 4, INVOCATION),
        (".claude/skills/use-it/SKILL.md", 3, SKILL),
        (".opencode/skills/use-spec2viz/SKILL.md", 2, SKILL),
    }


def test_mentions_in_docs_comments_and_changelogs_are_not_dependencies(tmp_path: Path) -> None:
    matrix = specir_repo(tmp_path)
    app = tmp_path / "app"
    write(app / "README.md", "Diagrams were built with `spec2viz diagram render` before specIR.\n")
    write(app / "CHANGELOG.md", "- dropped spec2viz (import spec2viz no longer needed)\n")
    write(app / "docs" / "guide.md", "from spec2viz import render\n")
    write(app / "desk" / "tasks" / "task-x.md", "spec2viz catalog build --config c.yml\n")
    write(app / "pkg" / "mod.py", '"""Ported from spec2viz: `spec2viz diagram sync` became sldb\'s."""\n# import spec2viz\nlabel = "spec2viz render spec.yml"\n')
    write(app / "pyproject.toml", '[project]\nname = "app"\n# spec2viz was a dependency\ndescription = "after spec2viz"\n')
    write(app / "build.sh", "# spec2viz diagram render was here\necho done\n")
    write(app / "pkg" / "names.py", 'def f(n):\n    return n.startswith("spec2viz ") or n.split("spec2viz")\n')
    store = app / ".sldb"
    write(store / "store.yaml", "models:\n- name: SpecDoc\n  model_ref: sldb.models.notation.spec_doc:SpecDoc\n")
    report = check(matrix, {"app": app, "app/.sldb": store})
    assert report.dependencies == []
    assert report.ok


def test_the_universe_is_exactly_the_inventory_plus_specir(tmp_path: Path) -> None:
    matrix = specir_repo(tmp_path)
    app, store = app_with_every_dependency(tmp_path)
    with pytest.raises(InventoryError, match="not in the inventory.*other"):
        check(matrix, {"app": app, "app/.sldb": store, "other": tmp_path})
    with pytest.raises(InventoryError, match="no path given for: app/.sldb"):
        check(matrix, {"app": app})
    report = check(matrix, {"app": app, "app/.sldb": store})
    assert report.repos == ["app", "IR"] and report.stores == ["app/.sldb"]
    result = CliRunner().invoke(main, ["retirement", "check", "--matrix", str(matrix), "--path", f"other={tmp_path}"])
    assert result.exit_code == 2 and "not in the inventory" in result.output


def real_paths() -> dict[str, Path]:
    repos, stores = inventory(MATRIX.read_text(encoding="utf-8"))
    located = {"graph_ui": WORKSPACE / "UIs" / "graph_ui"}
    paths = {name: located.get(name, WORKSPACE / name) for name in [*repos, *stores] if name != "IR"}
    missing = [name for name, path in paths.items() if not path.is_dir()]
    if missing:
        pytest.skip(f"repos or stores of the inventory not in the workspace: {missing}")
    return paths


@pytest.mark.xfail(strict=True, reason="consumers still depend on spec2viz and rows remain open: docs/spec2viz/acta-de-retiro.md")
def test_the_real_universe_has_no_dependency_and_every_row_is_accredited() -> None:
    report = check(MATRIX, real_paths())
    assert report.ok, f"{len(report.dependencies)} dependencies, {len(report.open_rows)} rows not accredited"

FILE:tests/visual/test_refs_models.py
"""The model and schema cases of spec2viz's `tests/test_refs.py` (SV-I03, IR13), ported against sldb's
spec models (D3) and specIR's schema export, without a wrapper.

The resolution cases of that file are in sldb (`tests/matching/test_matching_refs.py`, D4), the store
discovery in `tests/visual/test_catalog_parity.py` (IR13b) and the import rule in `tests/test_imports.py`."""

from __future__ import annotations

import json

import pytest

from sldb.models.notation.diagram_specs.activity import StepModel
from sldb.models.notation.diagram_specs.class_diagram import ClassDefinition
from sldb.models.notation.diagram_specs.component import NodeModel
from sldb.models.notation.diagram_specs.deployment import ArtifactModel, DeploymentNodeModel
from sldb.models.notation.diagram_specs.sequence import ParticipantModel
from sldb.models.notation.diagram_specs.state import StateData
from specir.visual import json_schema


@pytest.mark.parametrize("model", [NodeModel, DeploymentNodeModel, ArtifactModel, StepModel, ClassDefinition, ParticipantModel])
def test_models_accept_refs(model):
    assert model.model_fields["refs"].default_factory() == []
    kwargs = {"id": "p"} if model is ParticipantModel else {"label": "L"} if model is StepModel else {}
    assert model(**kwargs, refs=["TaskDoc:task-x", "desk:AtomDoc:atom-y"]).refs == ["TaskDoc:task-x", "desk:AtomDoc:atom-y"]


@pytest.mark.parametrize("bad", ["sin-modelo", "Model:", ":name", "a b:c", "Model:na me"])
def test_refs_without_model_part_are_rejected(bad):
    with pytest.raises(Exception):
        NodeModel(refs=[bad])


def test_state_model_and_schema_expose_refs():
    data = StateData(entity="E", initial="a", states=[{"id": "a", "label": "A", "refs": ["TaskDoc:t"]}], transitions=[])
    assert data.states[0].refs == ["TaskDoc:t"]
    assert "refs" in json.dumps(json_schema("state"))

FILE:docs/spec2viz/acta-de-retiro.md
# Acta de retiro de spec2viz

Tarea IR13 (`task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`). Evaluación del
2026-11-15 sobre IR `dc5496a`, sldb `d4aeb4b1` y el inventario de consumidores de
`docs/spec2viz/matriz-de-cobertura.md`.

**Retiro: no declarado.** El comprobador `specir retirement check` sale con código 1: quedan 122
dependencias de spec2viz en el universo auditado y 30 filas de la matriz sin acreditar. Archivar o borrar
spec2viz lo decide JP cuando el gate se cumpla; esta tarea no lo hace.

## Comprobador

`specir retirement check` (`src/specir/visual/retirement.py`, pruebas en
`tests/visual/test_retirement_gate.py`) audita en solo lectura exactamente los repos y stores del
inventario de la matriz más el repo de specIR, y la sección «Acreditación (IR13)» de la matriz. Cada
dependencia sale con repo o store, ruta, línea y clase (importación, dependencia declarada, invocación del
comando, habilidad de agente, modelo registrado). Un nombre fuera del inventario o uno del inventario sin
ruta es un error de uso (código 2). Las menciones en prosa, documentación, comentarios, docstrings,
changelogs y documentos del desk no cuentan.

Corrida real:

```
cd IR && .venv/bin/specir retirement check \
  --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron \
  --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb
```

rc 1; 122 dependencias; 30 filas no acreditadas. La prueba
`test_the_real_universe_has_no_dependency_and_every_row_is_accredited` es un xfail estricto mientras esto
siga así: cuando pase, la suite lo marca y hay que quitar el xfail y declarar el retiro aquí.

## Gate G1 a G7

| Ítem | Estado | Evidencia |
|---|---|---|
| G1 Filas cumplidas | abierto | 75 cumplidas y 30 abiertas en «Acreditación (IR13)» de la matriz. |
| G2 Suite de spec2viz | abierto | Sin portar: `tests/test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py`, `test_style_palette.py`, `test_view_doc.py` (filas «usar sldb directamente», eran de IR13c). Saltados sin mmdc: los casos de `test_mermaid_mmdc.py` y los de motor real de `test_class_diagram.py`, `test_class_packages.py` y `test_catalog_resolved_views.py`. xfail estricto: `label_key` frente a `normKey` (`test_atoms_matching.py`). Los 38 archivos tienen fila (`tests/test_matriz_cobertura_spec2viz.py`, 5 passed). |
| G3 CLI | abierto | Los 30 equivalentes existen y los invoca `test_every_equivalent_of_the_table_answers_its_help` (`tests/visual/test_cli.py`, 44 passed). Faltan los comandos de sldb para validar notación y paleta (SV-K21, SV-K26) y el de validar un spec, que hoy da specIR de forma provisional (SV-K16, SV-K29). Nota de sldb `20261115-192054`. |
| G4 Consumidores | abierto | 122 dependencias (abajo). |
| G5 Stores | abierto | `spec2viz/.sldb` registra los 7 modelos de `spec2viz.sldb_models` (19 registros). Es el único store del universo que lo hace. |
| G6 specIR limpio | cumplido | `tests/test_imports.py` (9 passed): nada bajo `src/specir/` importa spec2viz; `test_specir_defines_no_command_the_table_gives_to_sldb`. |
| G7 Decisión del YAML | abierto | `docs/decisiones/fuente-de-verdad-del-diagrama.md` sigue como propuesta pendiente de JP. |

## Consumidores

| Consumidor | Dependencias (clase) | Mensaje enviado | Cambio que lo resolvió |
|---|---|---|---|
| graph_ui | 34: 9 importaciones (`frontends/mindmap/sldb_adapter.py:245`, `:437` y pruebas), 3 declaradas (`pyproject.toml:19`, `:24`, `.github/requirements-suite.txt:10`), 22 invocaciones en pruebas | `UIs/graph_ui/desk/inbox/20261115-224814-suggestion-ir13-pide-migrar-graph-ui-de-spec2viz-a-sldb-resolve-view-sync-de-specs-viewdoc-pilotos.md` | pendiente |
| deskops | 22: 20 de habilidad de agente (`.claude/skills/deskops-workflow/SKILL.md`, `references/spec2viz-cli.md`, `.opencode/skills/use-spec2viz/SKILL.md`), 2 invocaciones (`desk/drawer/plans/workspace-documental/render_diagram.py:7`, `:9`). Además, la regla de rutas `deskops/graph/desk_graph.py:75` (no es dependencia; depende de G7) | `deskops/desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md` | pendiente |
| pron | 3 invocaciones (`docs/spec2viz/build.py:22`, `:23`, `:24`) | `pron/desk/inbox/20261115-224816-suggestion-ir13-pide-pasar-docs-spec2viz-build-py-de-pron-de-spec2viz-a-specir.md` | pendiente |
| sldb | 1 importación (oráculo de D2, `tests/notations/test_component_spec_python.py:43`). Además, el registro `docs/architecture/spec2viz/vistas.yml` que se construye con `spec2viz catalog build` y `contracts/identity.toml:299` (no son dependencias para el comprobador) | `sldb/desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md` | pendiente |
| store `spec2viz/.sldb` | 19 modelos registrados | `spec2viz/desk/inbox/20261115-225013-suggestion-ir13-el-store-de-spec2viz-es-el-nico-que-registra-spec2viz-sldb-models-gate-g5.md` | pendiente |
| IR (specIR) | 43 importaciones, todas en pruebas: los oráculos de paridad (`tests/visual/parity.py`, `render_parity.py` y los `importorskip("spec2viz")` de las pruebas de paridad) y la lectura del CLI de spec2viz en `tests/test_matriz_cobertura_spec2viz.py:31`. Se saltan sin spec2viz. Además, `tests/conftest.py:24` y `:80` y `tests/test_mcp_extension.py:24` federan el store `spec2viz/.sldb` (no es dependencia para el comprobador, pero la suite falla si el store desaparece) | propio: se resuelve en IR al declarar el retiro (quitar oráculos que ya tienen goldens, guardar como golden la corrida de paridad del catálogo de IR13b y cambiar la federación por un fixture) | pendiente |

Para enviar los mensajes se registraron en `desk/registry` de IR los repos deskops, pron, graph_ui (id
`graph-ui`) y spec2viz con `deskops repo register`; antes solo estaba sldb.

## Salida del comprobador (dependencias)

```
graph_ui	.github/requirements-suite.txt:10	dependencia declarada	-e git+https://github.com/jpcosec/spec2viz@master#egg=spec2viz
graph_ui	frontends/mindmap/sldb_adapter.py:245	importación	from spec2viz.notation_view import ViewError, resolve_view
graph_ui	frontends/mindmap/sldb_adapter.py:437	importación	from spec2viz.notation_view import ViewError, resolve_documents
graph_ui	pyproject.toml:19	dependencia declarada	notation = ["spec2viz>=0.1.0"]
graph_ui	pyproject.toml:24	dependencia declarada	"spec2viz>=0.1.0",
graph_ui	tests/e2e_mindmap_notation.py:27	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/e2e_mindmap_notation.py:42	invocación del comando	if not all(p.exists() for p in pilots) or not shutil.which("spec2viz"):
graph_ui	tests/e2e_mindmap_notation.py:48	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *(p.name for p in pilots), "--store", ".sldb"],
graph_ui	tests/e2e_notation_activity.py:121	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_activity.py:128	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *[s.name for s in specs], "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_class.py:51	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_class.py:58	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *[s.name for s in specs], "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_deployment.py:85	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_deployment.py:92	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *[s.name for s in specs], "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_legibility.py:38	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/e2e_notation_legibility.py:169	invocación del comando	if not ACTIVITY.exists() or not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_legibility.py:175	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", FIXTURE.name, DENSE.name, ACTIVITY.name, "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_sequence.py:101	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_sequence.py:108	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *[s.name for s in specs], "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_notation_style.py:141	invocación del comando	if not shutil.which("spec2viz"):
graph_ui	tests/e2e_notation_style.py:147	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", "component-infra.yml", "--notation", "infra.yml", "--store", ".sldb"],
graph_ui	tests/e2e_review_workbench_views.py:40	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/e2e_review_workbench_views.py:76	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *pilots, "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/e2e_review_workbench_views.py:86	invocación del comando	if not all((PILOTS / p).exists() for p in HERE + THERE) or not shutil.which("spec2viz"):
graph_ui	tests/e2e_review_workbench_views.py:96	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", "component-infra.yml", "--notation", "infra.yml", "--store", ".sldb"],
graph_ui	tests/test_mindmap_notation.py:20	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/test_mindmap_notation.py:21	importación	from spec2viz.notation_view import resolve_view  # noqa: E402
graph_ui	tests/test_mindmap_notation.py:40	invocación del comando	if not all(p.exists() for p in pilots) or not shutil.which("spec2viz"):
graph_ui	tests/test_mindmap_notation.py:45	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *(p.name for p in pilots), "--store", ".sldb"],
graph_ui	tests/test_projection_views.py:18	importación	spec2viz = pytest.importorskip("spec2viz")
graph_ui	tests/test_projection_views.py:28	invocación del comando	if not all((PILOTS / p).exists() for p in pilots) or not shutil.which("spec2viz"):
graph_ui	tests/test_projection_views.py:33	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", *pilots, "--store", ".sldb"], cwd=root, check=True, capture_output=True)
graph_ui	tests/test_projection_views.py:82	invocación del comando	subprocess.run(["spec2viz", "diagram", "sync", "component-infra.yml", "--notation", "infra.yml", "--store", ".sldb"],
graph_ui	tests/test_projection_views.py:167	importación	pytest.importorskip("spec2viz.sldb_models").ViewDoc  # task a: the model lives in spec2viz
deskops	.claude/skills/deskops-workflow/SKILL.md:27	habilidad de agente	(`spec2viz diagram render` / `spec2viz catalog build`) derive from specs and decisions. Atoms
deskops	.claude/skills/deskops-workflow/SKILL.md:59	habilidad de agente	re-run `spec2viz diagram render` / `spec2viz catalog build`. Validate before rendering:
deskops	.claude/skills/deskops-workflow/SKILL.md:60	habilidad de agente	`spec2viz diagram validate <spec.yml>`.
deskops	.claude/skills/deskops-workflow/SKILL.md:101	habilidad de agente	| Validate a diagram spec | `spec2viz diagram validate <spec.yml>` |
deskops	.claude/skills/deskops-workflow/SKILL.md:102	habilidad de agente	| Render a diagram | `spec2viz diagram render <spec.yml> --out <dir> [--renderer mermaid\|plantuml\|vega\|d2\|antonia-html\|json]` |
deskops	.claude/skills/deskops-workflow/SKILL.md:103	habilidad de agente	| Build a diagram catalog | `spec2viz catalog build --config <catalog.yml> --out <out.html>` |
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:8	habilidad de agente	commands (`spec2viz render`, `spec2viz validate`, `spec2viz schema`, `spec2viz lint`) remain as
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:13	habilidad de agente	- `spec2viz diagram validate <spec.yml> [<spec2.yml> ...]` — validate one or more diagram specs
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:15	habilidad de agente	- `spec2viz diagram render <spec.yml> [<spec2.yml> ...] --out <dir> \
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:19	habilidad de agente	- `spec2viz diagram schema [--type sequence|state|component|activity|deployment|matrix] [--out <file>]`
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:21	habilidad de agente	- `spec2viz diagram generate` — generate a component spec from Python source AST (reverse
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:23	habilidad de agente	- `spec2viz diagram lint <spec-or-mmd> [...]` — lint rendered Mermaid for browser-breaking syntax.
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:27	habilidad de agente	- `spec2viz catalog build --config <vistas.yml-or-diagram-store.yml> --out <out.html> \
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:33	habilidad de agente	- `spec2viz catalog schema [--out <file>]` — JSON Schema for diagram-store / `project.yml` configs.
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:34	habilidad de agente	- `spec2viz catalog serve` — serve a built catalog locally with auto-save for viewer annotations
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:80	habilidad de agente	- `spec2viz render <spec.yml> --out <dir> [--renderer ...]` == `spec2viz diagram render`
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:81	habilidad de agente	- `spec2viz validate <spec.yml>` == `spec2viz diagram validate`
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:82	habilidad de agente	- `spec2viz schema [--type ...] [--out ...]` == `spec2viz diagram schema` (also accepts
deskops	.claude/skills/deskops-workflow/references/spec2viz-cli.md:84	habilidad de agente	- `spec2viz lint <spec-or-mmd>` == `spec2viz diagram lint`
deskops	.opencode/skills/use-spec2viz/SKILL.md:2	habilidad de agente	name: use-spec2viz
deskops	desk/drawer/plans/workspace-documental/render_diagram.py:7	invocación del comando	subprocess.run(['spec2viz','diagram','validate',str(B/'dag.diagram.yaml')],check=True)
deskops	desk/drawer/plans/workspace-documental/render_diagram.py:9	invocación del comando	subprocess.run(['spec2viz','diagram','render',str(B/'dag.diagram.yaml'),'--renderer',renderer,'--out',str(B)],check=True)
pron	docs/spec2viz/build.py:22	invocación del comando	run('spec2viz', 'diagram', 'validate', *specs)
pron	docs/spec2viz/build.py:23	invocación del comando	run('spec2viz', 'diagram', 'render', *specs, '--backend', 'mermaid', '--out', 'out/mermaid')
pron	docs/spec2viz/build.py:24	invocación del comando	run('spec2viz', 'catalog', 'build', '--config', 'catalog.yml', '--out', 'index.html')
sldb	tests/notations/test_component_spec_python.py:43	importación	python_ast = pytest.importorskip("spec2viz.generators.python_ast")
IR	tests/test_matriz_cobertura_spec2viz.py:31	importación	main = importlib.import_module("spec2viz.cli").main
IR	tests/visual/parity.py:52	importación	from spec2viz.compilers import compile_ir
IR	tests/visual/parity.py:53	importación	from spec2viz.loader import load
IR	tests/visual/parity.py:54	importación	from spec2viz.validator import validate
IR	tests/visual/render_parity.py:74	importación	from spec2viz.compilers import compile_ir
IR	tests/visual/render_parity.py:75	importación	from spec2viz.loader import load
IR	tests/visual/render_parity.py:76	importación	from spec2viz.renderers import render
IR	tests/visual/render_parity.py:77	importación	from spec2viz.renderers.bpmn import render_bpmn_html
IR	tests/visual/render_parity.py:87	importación	from spec2viz.cli import DIAGRAM_RENDERERS
IR	tests/visual/render_parity.py:88	importación	from spec2viz.renderers import DEFAULT_RENDERER, EXT_MAP
IR	tests/visual/render_parity.py:94	importación	from spec2viz.renderers.view_mermaid import view_to_mermaid
IR	tests/visual/render_parity.py:100	importación	from spec2viz.linters.mermaid import lint_mermaid
IR	tests/visual/render_parity.py:106	importación	from spec2viz.schema import json_schema
IR	tests/visual/render_parity.py:112	importación	from spec2viz import render_to_file
IR	tests/visual/render_parity.py:119	importación	import spec2viz
IR	tests/visual/render_parity.py:190	importación	from spec2viz.linters.mermaid import lint_mermaid
IR	tests/visual/render_parity.py:191	importación	from spec2viz.schema import json_schema
IR	tests/visual/test_catalog_parity.py:39	importación	spec2viz = pytest.importorskip("spec2viz")
IR	tests/visual/test_catalog_parity.py:49	importación	from spec2viz.sldb_sync import check_catalog as oracle
IR	tests/visual/test_catalog_parity.py:102	importación	from spec2viz.sldb_sync import SpecSync as OracleSync
IR	tests/visual/test_catalog_parity.py:103	importación	from spec2viz.sldb_sync import sync_catalog as oracle_sync
IR	tests/visual/test_catalog_parity.py:122	importación	from spec2viz.cli import main
IR	tests/visual/test_catalog_parity.py:154	importación	from spec2viz.deskops import render_deskops
IR	tests/visual/test_catalog_parity.py:203	importación	from spec2viz.deskops import render_deskops
IR	tests/visual/test_lint_mermaid.py:86	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_cases.py:314	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_commands.py:251	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:53	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:59	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_render_parity.py:83	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_resources.py:62	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_schema.py:44	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:105	importación	spec2viz = pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:117	importación	from spec2viz.sldb_sync import SpecSync as Spec2VizSync
IR	tests/visual/test_sync_generation_parity.py:201	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:229	importación	import spec2viz.graph_import as oracle
IR	tests/visual/test_sync_generation_parity.py:258	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:259	importación	from spec2viz.graph_import import component_spec_from_graph as oracle_from_graph
IR	tests/visual/test_sync_generation_parity.py:260	importación	from spec2viz.graph_import import load_store_index
IR	tests/visual/test_sync_generation_parity.py:302	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_sync_generation_parity.py:303	importación	from spec2viz.generators.python_ast import generate_python_ast_spec
IR	tests/visual/test_visual_parity.py:35	importación	pytest.importorskip("spec2viz")
IR	tests/visual/test_visual_parity.py:43	importación	pytest.importorskip("spec2viz")
spec2viz/.sldb	store.yaml:44	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	store.yaml:47	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	store.yaml:50	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	store.yaml:53	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	store.yaml:56	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/store_index.yaml:141	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	core/store_index.yaml:154	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	core/store_index.yaml:167	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	core/store_index.yaml:180	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	core/store_index.yaml:193	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/store_index.yaml:246	modelo registrado	model_ref: spec2viz.sldb_models:ViewDoc
spec2viz/.sldb	core/store_index.yaml:259	modelo registrado	model_ref: spec2viz.sldb_models:PaletteDoc
spec2viz/.sldb	core/models/GlyphDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:GlyphDoc
spec2viz/.sldb	core/models/LinkDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:LinkDoc
spec2viz/.sldb	core/models/NotationDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:NotationDoc
spec2viz/.sldb	core/models/PaletteDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:PaletteDoc
spec2viz/.sldb	core/models/SpecDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:SpecDoc
spec2viz/.sldb	core/models/SpecNodeDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:SpecNodeDoc
spec2viz/.sldb	core/models/ViewDoc.yaml:2	modelo registrado	model_ref: spec2viz.sldb_models:ViewDoc
```

## Medición de `specir catalog build` (pendiente de IR13d)

`specir catalog build --config tests/visual/fixtures/catalog/examples/catalog/project.yml` dentro de IR
no termina en 300 s (`timeout 300`, rc 124, 3 min 50 s de CPU). Con cProfile (corrida cortada a los
150 s), 146 de los 149 s se van en `sldb.api.matching.attach_atom_edges`. Esa función hace 31 llamadas a
`StoreReader.edges_of`, que suman 62 llamadas a `load_edge_index` de ~1,1 s cada una:

- `with_live_stale` recalcula el stale vivo en cada llamada (284 251 `_moved`, 63 s).
- `EdgeIndex._ensure_maps` reconstruye los mapas en cada copia (61 veces, 66 s).

El store que descubre el catálogo es el `.sldb` de IR, que federa 8 stores (con `deskops` y `sldb`
duplicados desde `/mnt/ssd/herramientas`). Ahí `load_edge_index` tarda 28,6 s la primera vez y 0,4 s las
siguientes, pero devuelve un objeto nuevo cada vez (1963 stale).

Es de sldb, no de specIR: specIR solo usa la API pública. Pedido en
`sldb/desk/inbox/20261115-224941-suggestion-matching-edges-catalog-build-con-tomos-tarda-minutos-porque-cada-edges-of-recompone-live-stale-y-mapas-del-ndice-federado.md`.

## Lo que falta para declarar el retiro

1. Consumidores (G4): que graph_ui, deskops, pron y sldb resuelvan sus pedidos y respondan con el commit.
2. Store (G5): reapuntar los modelos de `spec2viz/.sldb` a los de sldb, o archivar el store con el repo
   (decisión del dueño).
3. Filas «usar sldb directamente» (SV-A17, SV-E02, SV-H01 a SV-H06, SV-J06, SV-K18 a SV-K26): portar los
   casos de `tests/test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py`,
   `test_style_palette.py` y `test_view_doc.py` contra la API de sldb, sin envoltorio. Ninguna tarea lo
   tiene desde que se retiró IR13c.
4. sldb: comando para validar spec, notación y paleta (SV-K16, K21, K26, K29; después hay que retirar
   `specir diagram validate`/`validate`). También el `label_key` con `_` (SV-G08 y SV-I02).
5. mmdc: correr la suite con mermaid-cli instalado (SV-B03, C13, C14, D01, G03 y, por dependencia, K09,
   K12 y K17).
6. IR: quitar o congelar los oráculos de paridad y la federación del store de spec2viz en las pruebas.
7. G7: decisión de JP sobre el YAML de spec frente al grafo.

FILE:docs/spec2viz/gate-de-retiro.md
# Gate de retiro de spec2viz: procedimiento

La lista comprobable del gate (G1 a G7) está en la sección «Gate de retiro» de
`docs/spec2viz/matriz-de-cobertura.md`; este documento no la repite, solo fija quién la evalúa, en qué
orden y qué pasa si falla.

## Quién y cuándo

- Lo evalúa la tarea IR13 (`task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`), una
  vez cerradas IR11, IR12, IR13a, IR13b, IR13d y las tareas de sldb D1 a D4.
- IR13 es la única que escribe evidencia en la matriz (la prueba que acredita cada fila) y el acta de
  retiro `docs/spec2viz/acta-de-retiro.md`.
- Archivar o borrar el repo spec2viz es decisión de su dueño una vez cumplido el gate; ni IR07 ni IR13 lo
  hacen.

## Orden de evaluación

1. **G7** primero: si la decisión del YAML no está aceptada por JP, el gate no se evalúa.
2. **G6** (specIR limpio): prueba de imports de specIR.
3. **G1, G2 y G3** (filas, suite y CLI): por cada fila, ejecutar la prueba citada; la tabla «Pruebas de
   spec2viz por fila» no puede dejar un archivo de `spec2viz/tests/` sin fila ni un caso sin portar o sin
   prueba equivalente declarada.
4. **G4 y G5** (consumidores y stores): el comprobador de IR13 (`specir retirement check`) recorre en solo
   lectura exactamente el universo del «Inventario de consumidores» de la matriz más el repo de specIR, y
   lista cada dependencia remanente con repo o store, ruta, línea y clase.

## Si falla

- Cualquier ítem en falso: el comprobador sale con código distinto de cero y el retiro no se declara.
- Una dependencia remanente en otro repo no se corrige desde specIR: se pide al desk de ese repo
  (`deskops message send --to <repo>`) y se registra como evidencia pendiente.
- Una fila cuya condición resulta imposible se reescribe en la matriz con aprobación de JP; nunca se
  marca como descartada sin prueba.

FILE:instruccion
Cold-bundle de la tarea task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- El comprobador falla sobre una matriz de entrada con una fila sin prueba citada y pasa cuando todas la tienen.
- Sobre un repo de entrada con una importación de spec2viz en código, una dependencia en pyproject.toml y una llamada al comando spec2viz en un script, y un índice de store con un modelo spec2viz.sldb_models, el comprobador reporta las cuatro con repo, ruta, línea y clase de dependencia, termina con código de salida distinto de cero y no modifica ningún archivo.
- Sobre un repo de entrada que solo menciona spec2viz en documentación, comentarios y un changelog, el comprobador no reporta ninguna dependencia.
- El comprobador audita exactamente los repos y stores del inventario de la matriz de cobertura más el repo de specIR, y falla con un error que lo dice si se le pide auditar uno que no está en el inventario o si falta la ruta de uno que sí está.
- Ejecutado sobre todos los repos y stores reales del inventario, el comprobador no reporta ninguna dependencia y termina con código de salida cero.
- La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado en la matriz de cobertura.
- El acta de retiro lista, por cada consumidor del inventario, el mensaje enviado a su desk, la referencia del cambio que lo resolvió y la salida del comprobador; si quedó alguna dependencia, el acta dice que el retiro no está declarado.
- Toda fila de la matriz de cobertura tiene su condición de retiro cumplida y su prueba citada.

