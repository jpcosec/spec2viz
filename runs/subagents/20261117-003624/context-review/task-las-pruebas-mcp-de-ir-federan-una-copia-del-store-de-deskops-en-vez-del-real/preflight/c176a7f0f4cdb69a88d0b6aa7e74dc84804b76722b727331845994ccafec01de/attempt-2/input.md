FILE:desk/tasks/task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real.md
---
sldb:
  by: agent
  at: '2026-11-17T00:08:00Z'
  authority: generated
  via: save_document_payload
id: task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- tests/conftest.py
- tests/test_mcp_extension.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Las pruebas MCP de IR federan una copia del store de deskops en vez del real

## Rationale

_Explain why this task exists or the business driver behind it._

tests/test_mcp_extension.py::test_reading_through_every_tool_leaves_every_store_untouched digiere el store real de deskops (FEDERATED en tests/conftest.py). Cualquier agente que escriba en deskops mientras corre la suite completa de IR la hace fallar sin relación con la tarea que se prueba. Le pasó tres veces seguidas al tester de IR13g (runs/subagents/deskops-t-e9062210030f, corridas 1 a 3), y antes al de la federación. Así, la suite de IR no da verde mientras deskops trabaja.

## Goal

_Describe the concrete result this task must produce._

La suite completa de IR es reproducible con independencia de lo que hagan otros desks: las pruebas MCP enlazan y digieren una copia del store de deskops tomada al inicio de la sesión, no el store real.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/conftest.py y tests/test_mcp_extension.py. El fixture que enlaza deskops copia su store (y lo que haga falta para que sus enlaces resuelvan) a un directorio temporal de sesión, y la prueba de untouched digiere esa copia. Se conserva la cobertura de leer a través de un store federado. Fuera: cambiar deskops o sldb; la tarea de federación de spec2viz, que ya cambia esos archivos y va primero.

## Implementation Path

_Outline the expected implementation route or affected surface._

Empezar con task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a integrada (closeout 4f1e108 en main de IR). Seguir su patrón: build_spec_store construye un store temporal y el digest cubre ese store temporal. Si copiar el store de deskops rompe la resolución de sus enlaces a sldb, pron o scion, detenerse y anotarlo como bloqueo en result-summary.md. Precisiones (preflight-1): (a) Una función auxiliar build_deskops_copy(tmp_path_factory) -> Path, llamada desde un fixture de pytest con scope="session", hace la copia una vez, al montarse el fixture y antes de cualquier prueba que lo use. Crea <tmp>/deskops con el .sldb de deskops (sin la caché) y los archivos que lista git -C <deskops> ls-files, y devuelve <tmp>/deskops/.sldb. (b) Enlaces (corregida en el ciclo de corrección 1, tras el FAIL D2 del tester deskops-t-af2c27434a91): la copia no debe permitir que la sesión salga de <tmp>. Los symlinks a los repos reales quedan prohibidos, porque los stores de sldb y scion federan de vuelta ../deskops/.sldb, y así la sesión MCP leía el store real. Primera opción: quitar de la copia los enlaces a sldb, pron y scion con la CLI pública (sldb stores remove, con --store sobre la copia). Si sldb rechaza quitar un enlace porque un modelo de deskops depende de él, la segunda opción es copiar ese store enlazado igual que el de deskops (su .sldb sin caché más los archivos de su git ls-files) a <tmp>/<nombre>. Así sus enlaces relativos de vuelta a ../deskops resuelven a la copia. Un enlace de esas copias que apunte fuera de <tmp> se quita con sldb stores remove. Si sldb también rechaza eso, se detiene y se reporta. Esos stores copiados solo se leen y no se digieren. (c) FEDERATED pasa a recibir esa copia, por fixture y no como constante con la ruta real. federated_digest digiere la copia, con el mismo criterio de hoy: el árbol .sldb más los .md listados por git ls-files del proyecto real, leídos en la copia. mount_copy enlaza la copia con sldb stores add <copia> --name deskops. (d) La prueba de untouched es tests/test_mcp_extension.py::test_reading_through_every_tool_leaves_every_store_untouched; sus aserciones no se relajan.

## Validation

_List the checks required before this task can close._

- grep -nE 'WORKSPACE / "deskops"|\.\./deskops' tests/conftest.py tests/test_mcp_extension.py solo encuentra, si encuentra algo, el origen de la copia dentro de build_deskops_copy; ninguna prueba ni digest usa la ruta real.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -rs -p no:cacheprovider tests/test_mcp_extension.py sale con rc 0 y sin skipped.
- En la copia montada, sldb stores list (o el store_index de la copia) muestra el alias deskops apuntando a un directorio temporal, no a ../deskops del workspace.
- strace -f sobre la corrida de tests/test_mcp_extension.py: pasada la ventana de la copia, ningún proceso (pytest, sldb mcp, sldb stores) abre archivos bajo SLDB_1/deskops/ del workspace.
- Suite completa una vez bajo flock /dev/shm/sldb1-tests.lock con rc 0.
- deskops graph missing --root . (desde la raíz de IR) sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas MCP de IR no leen ni digieren el store real de deskops y la suite completa da verde aunque deskops escriba durante la corrida.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-las-pruebas-mcp-de-ir-federan-una-copia-del-store-de-deskops-en-vez-del-real: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

