---
sldb:
  by: agent
  at: '2026-11-16T08:29:18Z'
  authority: generated
  via: save_document_payload
id: task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents
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
- runs/subagents/deskops-t-5a39cc2dfbf8/result-summary.md
depends_on: []
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
files:
- tests/conftest.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Fixture mount_copy de las pruebas copia los RunDoc de runs/subagents

## Rationale

_Explain why this task exists or the business driver behind it._

El store de IR registra RunDocs, que el rol deskops-supervisor exige escribir como intención antes de cada despacho, y esos RunDocs viven en runs/subagents/<run>/run.md. El fixture mount_copy de tests/conftest.py copia solo .sldb, sldb y desk (COPIED), así que en la copia aislada 'sldb stores update' falla con 'Skipped missing documents: run-…' y las 5 pruebas de tests/test_mcp_extension.py dan error de setup. Con eso la suite completa de IR no puede salir con rc 0 mientras exista un RunDoc. Evidencia: runs/subagents/deskops-t-5a39cc2dfbf8/result-summary.md, sección «Suite completa».

## Goal

_Describe the concrete result this task must produce._

La copia aislada del store que arma mount_copy contiene también cada runs/subagents/*/run.md del repo, en la misma ruta relativa, y tests/test_mcp_extension.py pasa con RunDocs registrados en el store.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/conftest.py, solo mount_copy y sus constantes: además de COPIED, copiar cada archivo que coincida con runs/subagents/*/run.md (y solo esos, no el resto de runs/ ni session.jsonl) a la misma ruta relativa bajo la raíz de la copia; actualizar el docstring del módulo, que hoy dice que la copia tiene .sldb, sldb y desk. Fuera: tocar .sldb, desk o runs del repo; cambiar original_digest o copy_digest (siguen midiendo .sldb y desk); cambiar FEDERATED; cualquier otro archivo de tests o de src.

## Implementation Path

_Outline the expected implementation route or affected surface._

En tests/conftest.py, mount_copy (línea 70): después del bucle sobre COPIED, recorrer sorted(REPO.glob('runs/subagents/*/run.md')) y copiar cada uno con shutil.copy2 a root / path.relative_to(REPO), creando el directorio padre. Declarar el patrón como constante de módulo junto a COPIED (por ejemplo RUN_DOCS = 'runs/subagents/*/run.md'), con un comentario de una línea que diga por qué: el store registra RunDocs que viven fuera de .sldb y desk. Comandos desde la raíz de IR con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- Con RunDocs registrados en el store (hoy existen runs/subagents/deskops-e-31500ac1cfa1/run.md y runs/subagents/deskops-t-5a39cc2dfbf8/run.md): TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mcp_extension.py sale con rc 0 y 5 passed.
- git diff --stat muestra solo tests/conftest.py fuera de desk/, .sldb/ y runs/.
- Suite completa una vez bajo el lock: SPECIR_MMDC=/mnt/ssd/herramientas/mermaid-cli/mmdc TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock .venv/bin/python -m pytest -q -n 4 -p no:cacheprovider tests/ sale con rc 0.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

mount_copy copia los runs/subagents/*/run.md, tests/test_mcp_extension.py pasa con RunDocs en el store y la suite completa de IR sale con rc 0.
