FILE:desk/tasks/task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5.md
---
sldb:
  by: agent
  at: '2026-11-16T10:40:23Z'
  authority: generated
  via: save_document_payload
id: task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-021430-suggestion-g5-decisi-n-de-jp-sobre-spec2viz-sldb.md
- desk/inbox/20261116-040635-suggestion-pron-ir13-resuelto-4224186.md
- task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz
depends_on:
- task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- docs/spec2viz/acta-de-retiro.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# IR13f Anotar en el acta de retiro la resolución de pron (4224186) y la decisión de JP sobre G5

## Rationale

_Explain why this task exists or the business driver behind it._

docs/spec2viz/acta-de-retiro.md es el registro del gate de retiro de spec2viz (IR13), y dos de sus entradas quedaron desactualizadas por mensajes recibidos. (1) pron resolvió su pedido: el commit 4224186527a894da6a7842ffa03c313292437425 de pron (master, pusheado) hace que el script build.py de la carpeta docs/spec2viz de pron use specir en las tres llamadas de las líneas 22 a 24. Su tester independiente verificó que build.py sale con rc 0 y que specir retirement check no muestra filas de pron (nota desk/inbox/20261116-040635-suggestion-pron-ir13-resuelto-4224186.md). La fila de pron del acta sigue en «pendiente». (2) JP decidió G5 el 2026-11-16 con la opción A: el store spec2viz/.sldb se archiva junto con el repo spec2viz cuando specir retirement check dé 0, y no se reapuntan sus 7 modelos (nota desk/inbox/20261116-021430-suggestion-g5-decisi-n-de-jp-sobre-spec2viz-sldb.md). La fila G5 sigue en «abierto», con las dos opciones planteadas.

## Goal

_Describe the concrete result this task must produce._

El acta registra a pron como resuelto, con su commit y la evidencia, y registra en G5 la decisión de JP (opción A) y lo que queda pendiente en IR por esa decisión.

## Scope

_State what is in scope and what is out of scope._

Dentro, solo en docs/spec2viz/acta-de-retiro.md: (1) la fila de pron de la tabla de consumidores (hoy con «pendiente»): pasa a «resuelto», citando el commit 4224186 de pron y lo que verificó su tester; (2) la fila «G5 Stores»: registra la decisión de JP del 2026-11-16 (opción A: archivar spec2viz/.sldb con el repo, sin reapuntar sus 7 modelos), cita el atom de spec2viz atom-decisión-de-jp-2026-11-16-g5-el-store-spec2viz-sldb-se-archiva-con-el-repo y la task.decision task-decisión-de-jp-g5-del-retiro-archivar-el-store-spec2viz-sldb-con-el-repo-o-reapuntar-sus-7-modelos-a, y lista lo pendiente en IR: quitar spec2viz/.sldb del universo de specir retirement check al declarar el retiro (IR13), y dejar de federar ese store en las pruebas (task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a). El estado de G5 queda «decidido; pendiente de ejecución en IR», no «cerrado»; (3) la lista de pasos que quedan al final del acta (los puntos «Consumidores (G4)» y «Store (G5)»): se quita pron de G4 y en G5 se reemplaza la alternativa por la decisión tomada; (4) se corre de nuevo specir retirement check y se anota su salida resumida (filas abiertas, número de dependencias y rc), igual que las corridas anteriores del acta. Fuera: la matriz de cobertura; declarar el retiro; quitar spec2viz/.sldb del universo; tocar las pruebas; cambiar pron o spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero las dos notas de desk/inbox citadas en Why y el acta completa. Editar solo docs/spec2viz/acta-de-retiro.md, conservando el formato de sus tablas y de las corridas anteriores de specir retirement check. Para comprobar lo que dice la nota de pron: grep -n specir ../pron/docs/spec2viz/build.py muestra las llamadas de las líneas 22 a 24, y git -C ../pron merge-base --is-ancestor 4224186 HEAD sale con rc 0. Si alguna de las dos cosas falla, la fila de pron no se marca como resuelta: se anota lo que se encontró y se reporta. Para verificar el atom y la task.decision de spec2viz: ls ../spec2viz/desk/atoms/ | grep g5 y ls ../spec2viz/desk/tasks/ | grep g5. El comando del comprobador es el mismo de las corridas anteriores del acta: timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb. Comandos desde la raíz de IR, con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo docs/spec2viz/acta-de-retiro.md.
- git -C ../pron merge-base --is-ancestor 4224186 HEAD sale con rc 0, y la salida de specir retirement check no tiene filas de pron.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- grep -n 'pron' docs/spec2viz/acta-de-retiro.md muestra la fila de pron como resuelta, con 4224186, y grep -n 'G5' muestra la decisión de JP (opción A) y lo pendiente en IR.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

El acta registra a pron como resuelto con su commit y su evidencia, y G5 como decidido (opción A) con lo pendiente en IR. La salida nueva de specir retirement check está anotada, y las pruebas de la matriz y del gate pasan.

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

FILE:docs/spec2viz/acta-de-retiro.md
# Acta de retiro de spec2viz

Tarea IR13 (`task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz`). Evaluación del
2026-11-15 sobre IR `dc5496a`, sldb `d4aeb4b1` y el inventario de consumidores de
`docs/spec2viz/matriz-de-cobertura.md`.

**Retiro: no declarado.** El comprobador `specir retirement check` sale con código 1: quedan 119
dependencias de spec2viz en el universo auditado y 13 filas de la matriz sin acreditar (re-corrida del
2026-11-16 tras IR13e, que portó contra sldb las pruebas de notaciones, paletas y vistas; antes eran 23,
y 30 antes de las decisiones de JP y la corrida con mermaid-cli real). Archivar o borrar
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

rc 1; 119 dependencias; 13 filas no acreditadas (SV-A17, G08, H01, H03, I02, K09, K16, K18, K21, K22,
K23, K26 y K29). Corrida del 2026-11-16 tras IR13e
(`task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb`), sobre
sldb `9307d485` y spec2viz `91ba1d0` (b624b75 más un commit solo de desk/store): antes de IR13e eran 23
filas (SV-A17, E02, G08, H01 a H06, I02, J06, K09, K16, K18 a K26 y K29) y 119 dependencias; las 122 de
la corrida del 2026-11-15 bajaron a 119 porque ya no aparecen las 3 invocaciones de pron
(`docs/spec2viz/build.py:22` a `:24`), cambio ajeno a IR13e. La prueba
`test_the_real_universe_has_no_dependency_and_every_row_is_accredited` es un xfail estricto mientras esto
siga así: cuando pase, la suite lo marca y hay que quitar el xfail y declarar el retiro aquí.

## Gate G1 a G7

| Ítem | Estado | Evidencia |
|---|---|---|
| G1 Filas cumplidas | abierto | 92 cumplidas y 13 abiertas en «Acreditación (IR13)» de la matriz. IR13e (2026-11-16) acreditó SV-E02, SV-H02, SV-H04, SV-H05, SV-H06, SV-J06, SV-K19, SV-K20, SV-K24 y SV-K25; la corrida con mermaid-cli real del 2026-11-15 acreditó SV-B03, SV-C13, SV-C14, SV-D01, SV-G03, SV-K12 y SV-K17. |
| G2 Suite de spec2viz | abierto | Portadas contra sldb por IR13e en `tests/visual/test_notations_parity.py` (75 passed, 1 xfailed): las 40 pruebas no CLI de `tests/test_view_doc.py`, `test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py` y `test_style_palette.py`, más 9 comparaciones «valida igual»; las 6 que invocan el CLI de spec2viz tienen su equivalente en las filas K. xfail estricto: el mensaje de `diagram_type` desconocido de test_invalid_notations_are_rejected (SV-H01, nota a sldb 20261116-022332). Los casos de mmdc (`test_mermaid_mmdc.py` y los de motor real de `test_class_diagram.py`, `test_class_packages.py` y `test_catalog_resolved_views.py`) ya corren con mermaid-cli real y pasan (2026-11-15). xfail estricto: `label_key` frente a `normKey` (`test_atoms_matching.py`). Los 38 archivos tienen fila (`tests/test_matriz_cobertura_spec2viz.py`, 5 passed). |
| G3 CLI | abierto | Los 30 equivalentes existen y los invoca `test_every_equivalent_of_the_table_answers_its_help` (`tests/visual/test_cli.py`, 44 passed). Faltan los comandos de sldb para validar notación y paleta (SV-K21, SV-K26) y el de validar un spec, que hoy da specIR de forma provisional (SV-K16, SV-K29). Nota de sldb `20261115-192054`. |
| G4 Consumidores | abierto | 119 dependencias (abajo; corrida del 2026-11-16). |
| G5 Stores | abierto | `spec2viz/.sldb` registra los 7 modelos de `spec2viz.sldb_models` (19 registros). Es el único store del universo que lo hace. |
| G6 specIR limpio | cumplido | `tests/test_imports.py` (9 passed): nada bajo `src/specir/` importa spec2viz; `test_specir_defines_no_command_the_table_gives_to_sldb`. |
| G7 Decisión del YAML | cumplido | JP aceptó el 2026-11-15 (vía supervisor) que el YAML del spec queda como formato de autoría e intercambio subordinado al grafo: `docs/decisiones/fuente-de-verdad-del-diagrama.md` y atom `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al` (la propuesta de IR07 quedó como redirección). |

## Consumidores

| Consumidor | Dependencias (clase) | Mensaje enviado | Cambio que lo resolvió |
|---|---|---|---|
| graph_ui | 34: 9 importaciones (`frontends/mindmap/sldb_adapter.py:245`, `:437` y pruebas), 3 declaradas (`pyproject.toml:19`, `:24`, `.github/requirements-suite.txt:10`), 22 invocaciones en pruebas | `UIs/graph_ui/desk/inbox/20261115-224814-suggestion-ir13-pide-migrar-graph-ui-de-spec2viz-a-sldb-resolve-view-sync-de-specs-viewdoc-pilotos.md` | pendiente |
| deskops | 22: 20 de habilidad de agente (`.claude/skills/deskops-workflow/SKILL.md`, `references/spec2viz-cli.md`, `.opencode/skills/use-spec2viz/SKILL.md`), 2 invocaciones (`desk/drawer/plans/workspace-documental/render_diagram.py:7`, `:9`). Además, la regla de rutas `deskops/graph/desk_graph.py:75` (no es dependencia; decidida, ver «Decisiones» 4) | `deskops/desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md` | pendiente |
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
3. Filas «usar sldb directamente»: portadas por IR13e (`tests/visual/test_notations_parity.py`). Quedan
   SV-H01 (sldb da otro mensaje ante un `diagram_type` desconocido; nota a sldb 20261116-022332), SV-A17
   (solo G5), SV-H03 y su dependiente SV-K22 (solo G4 de graph_ui), y SV-K18 y SV-K23 (dependen de SV-K21,
   SV-K22 y SV-K26).
4. sldb: comando para validar spec, notación y paleta (SV-K16, K21, K26, K29; después hay que retirar
   `specir diagram validate`/`validate`). También el `label_key` con `_` (SV-G08 y SV-I02).
5. mmdc: resuelto el 2026-11-15. Con mermaid-cli real (`SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc`)
   pasan los casos de motor real; quedaron cumplidas SV-B03, C13, C14, D01, G03, K12 y K17. SV-K09 sigue
   abierta por SV-K16.
6. IR: quitar o congelar los oráculos de paridad y la federación del store de spec2viz en las pruebas.
7. G7: resuelto el 2026-11-15 (decisión aceptada por JP; ver «Decisiones»).
8. En el momento del retiro: el BPMN pasa a `exporter="specir"` y a un `targetNamespace` de specir, y la
   página del catálogo a una clave de `localStorage` de specir, con goldens nuevos y migración de las
   anotaciones guardadas con `spec2viz.catalog.annotations.v1` (decisión 3).
9. Archivar spec2viz cuando `specir retirement check` salga con 0 (decisión 6).

## Decisiones

Registradas el 2026-11-15. Todas aceptadas por JP (transmitidas por el supervisor con autorización
explícita).

1. **G7, el YAML del spec** (decisión del dueño, JP): el YAML del spec queda como formato de autoría e
   intercambio subordinado al grafo, según `docs/decisiones/fuente-de-verdad-del-diagrama.md`. Registro:
   atom `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al`
   (la propuesta `atom-propuesta-pendiente-de-jp-…` se fusionó en él con `deskops atoms merge`). No hay
   task.decision asociada a G7 en el desk de IR.
2. **mmdc con motor real**: JP autorizó lanzar `/usr/bin/google-chrome` para mermaid-cli. Instalado en
   `/mnt/ssd/herramientas/mermaid-cli` (fuera de los repos), con un envoltorio `mmdc` que corre Chrome en
   headless con `timeout` y perfil temporal en `/dev/shm`. Cómo apuntar `SPECIR_MMDC`: habilidad
   `skills/use-specir/SKILL.md`, sección «Real mermaid engine (mmdc)».
3. **Exporter de BPMN y clave de `localStorage`** (elegida por el coordinador): mientras dure la paridad se
   mantienen `exporter="spec2viz"`, `targetNamespace="http://spec2viz/bpmn"` (SV-C06) y la clave
   `spec2viz.catalog.annotations.v1` (SV-G06). En el momento del retiro pasan a specir con goldens nuevos
   y migración de anotaciones (paso 8 de la lista anterior).
4. **deskops, regla de rutas** (elegida por el coordinador; la ejecuta el desk de deskops, no IR):
   `deskops/graph/desk_graph.py:75` deja de nombrar spec2viz y reconoce los specs YAML como artefactos de
   autoría sincronizados con `sldb notations sync`.
5. **sldb, `docs/architecture/spec2viz`** (elegida por el coordinador; la ejecuta el desk de sldb, no IR):
   los specs se quedan como fixtures durante la paridad; el catálogo se construye con
   `specir catalog build` y se sincroniza con `sldb notations sync --catalog`.
6. **Archivo de spec2viz**: spec2viz se archiva cuando `specir retirement check` salga con 0.

FILE:instruccion
Cold-bundle de la tarea task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo docs/spec2viz/acta-de-retiro.md.
- git -C ../pron merge-base --is-ancestor 4224186 HEAD sale con rc 0, y la salida de specir retirement check no tiene filas de pron.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- grep -n 'pron' docs/spec2viz/acta-de-retiro.md muestra la fila de pron como resuelta, con 4224186, y grep -n 'G5' muestra la decisión de JP (opción A) y lo pendiente en IR.
- deskops graph missing --root . sale con rc 0.

