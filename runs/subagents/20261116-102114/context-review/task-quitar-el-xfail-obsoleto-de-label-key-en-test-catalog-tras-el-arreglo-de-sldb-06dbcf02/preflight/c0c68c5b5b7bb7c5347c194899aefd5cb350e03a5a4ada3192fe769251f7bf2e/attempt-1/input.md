FILE:desk/tasks/task-quitar-el-xfail-obsoleto-de-label-key-en-test-catalog-tras-el-arreglo-de-sldb-06dbcf02.md
---
sldb:
  by: agent
  at: '2026-11-16T10:21:04Z'
  authority: generated
  via: save_document_payload
id: task-quitar-el-xfail-obsoleto-de-label-key-en-test-catalog-tras-el-arreglo-de-sldb-06dbcf02
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- topic:pruebas
- host:robocop2
current_node: ritual-execution
history: []
references:
- runs/subagents/deskops-t-8825fdd278af/result-summary.md
depends_on: []
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- tests/visual/test_catalog.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Quitar el xfail obsoleto de label_key en test_catalog tras el arreglo de sldb 06dbcf02

## Rationale

_Explain why this task exists or the business driver behind it._

tests/visual/test_catalog.py tiene test_label_key_of_sldb_splits_underscores_like_norm_key marcado pytest.mark.xfail(strict=True, reason="sldb's label_key keeps '_' ..."), porque label_key de sldb no separaba el guion bajo como normKey de la plantilla del catálogo (nota a sldb 20261115-214942). sldb lo arregló en el commit 06dbcf02 («matching: label_key trata el guion bajo como separador, igual que normKey del catálogo»), y IR usa sldb como instalación editable desde ../sldb. Desde entonces la prueba pasa, el xfail estricto se vuelve XPASS(strict) = FAILED y la suite completa de IR sale con rc 1. Evidencia: runs/subagents/deskops-t-8825fdd278af/result-summary.md, sección «El fallo de la verificación 2».

## Goal

_Describe the concrete result this task must produce._

test_label_key_of_sldb_splits_underscores_like_norm_key corre como prueba normal (sin xfail) y pasa contra el sldb actual, y la suite completa de IR vuelve a salir con rc 0.

## Scope

_State what is in scope and what is out of scope._

Dentro: en tests/visual/test_catalog.py, quitar solo el decorador pytest.mark.xfail(strict=True, ...) de test_label_key_of_sldb_splits_underscores_like_norm_key, sin cambiar su cuerpo, su docstring ni el decorador @needs_node. Fuera: cualquier otro archivo o prueba; actualizar las filas SV-G08 y SV-I02 de docs/spec2viz/matriz-de-cobertura.md o el acta (ese archivo tiene cambios sin commitear de la tarea IR13e, que acreditará esas filas en su ciclo de corrección); cambiar sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Antes de editar, confirmar con git -C ../sldb merge-base --is-ancestor 06dbcf02 HEAD (rc 0) que el arreglo está en el sldb instalado, y correr solo esa prueba (TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider "tests/visual/test_catalog.py::test_label_key_of_sldb_splits_underscores_like_norm_key") para ver el XPASS(strict). Borrar el decorador completo @pytest.mark.xfail(strict=True, reason=...) que está justo encima de la función (hoy ocupa una sola línea), sin tocar @needs_node, el cuerpo ni el docstring. Si la prueba sin xfail no pasa, detenerse y reportarlo: no se cambia la aserción. El árbol de trabajo tiene además cambios sin commitear de otras dos tareas: tests/conftest.py, de task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents, y los 5 archivos de IR13e. No se tocan. Son precondición bloqueante de la suite completa: antes de correrla, comprobar con git diff --stat tests/conftest.py que el cambio de mount_copy (RUN_DOCS) está presente. Si falta, no correr la suite, detenerse y reportarlo, porque sin él tests/test_mcp_extension.py falla por los RunDocs. Comandos desde la raíz de IR con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- git -C ../sldb merge-base --is-ancestor 06dbcf02 HEAD sale con rc 0.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/visual/test_catalog.py sale con rc 0, sin xfailed ni xpassed para test_label_key_of_sldb_splits_underscores_like_norm_key.
- git diff tests/visual/test_catalog.py muestra solo las líneas borradas del decorador xfail.
- {'Suite completa una vez, bajo flock /dev/shm/sldb1-tests.lock': 'SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ sale con rc 0.'}
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

La prueba corre sin xfail y pasa, el diff de tests/visual/test_catalog.py es solo la eliminación del decorador, y la suite completa de IR sale con rc 0.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-quitar-el-xfail-obsoleto-de-label-key-en-test-catalog-tras-el-arreglo-de-sldb-06dbcf02: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

