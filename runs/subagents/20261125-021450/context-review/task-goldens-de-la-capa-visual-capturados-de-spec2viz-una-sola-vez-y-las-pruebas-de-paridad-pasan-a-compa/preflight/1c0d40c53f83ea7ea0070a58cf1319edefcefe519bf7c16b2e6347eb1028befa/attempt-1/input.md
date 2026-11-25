FILE:desk/tasks/task-goldens-de-la-capa-visual-capturados-de-spec2viz-una-sola-vez-y-las-pruebas-de-paridad-pasan-a-compa.md
---
sldb:
  by: agent
  at: '2026-11-25T01:08:42Z'
  authority: generated
  via: create_document
id: task-goldens-de-la-capa-visual-capturados-de-spec2viz-una-sola-vez-y-las-pruebas-de-paridad-pasan-a-compa
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Goldens de la capa visual capturados de spec2viz una sola vez, y las pruebas de paridad pasan a compararse contra esos goldens

## Rationale

_Explain why this task exists or the business driver behind it._

JP 2026-11-24: spec2viz quedo retirado y continua como IR (jpcosec/specir); un oraculo sin mantenimiento no sirve. Hoy 7 archivos de tests/visual (parity.py, render_parity.py y los test_*_parity.py) comparan con spec2viz instalado y se saltan sin el.

## Goal

_Describe the concrete result this task must produce._

Las salidas de referencia que hoy calcula spec2viz se guardan como goldens versionados bajo tests/visual/goldens/, y las pruebas de paridad comparan specIR contra esos archivos en vez de importar spec2viz.

## Scope

_State what is in scope and what is out of scope._

Un script de captura de una sola vez (tests/visual/capture_goldens.py o similar, que use spec2viz de /mnt/ssd/proyectos/SLDB_1/spec2viz), los goldens, y los tests de paridad reescritos contra goldens. Fuera: quitar el marcador parity y la dependencia (tarea siguiente).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/visual/parity.py y render_parity.py para ver que se compara. 2) Script que corre spec2viz sobre los mismos casos y escribe goldens. 3) Reescribir los tests para leer goldens (sin importar spec2viz). 4) Correr solo tests/visual con spec2viz desinstalado del PYTHONPATH: nada se salta por falta de spec2viz.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q tests/visual -rs

## Done When

_Name the observable condition that makes the task complete._

Con spec2viz fuera del entorno, PYTHONPATH=src pytest -q tests/visual corre las comparaciones contra goldens sin saltarse ninguna por spec2viz.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-goldens-de-la-capa-visual-capturados-de-spec2viz-una-sola-vez-y-las-pruebas-de-paridad-pasan-a-compa: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

