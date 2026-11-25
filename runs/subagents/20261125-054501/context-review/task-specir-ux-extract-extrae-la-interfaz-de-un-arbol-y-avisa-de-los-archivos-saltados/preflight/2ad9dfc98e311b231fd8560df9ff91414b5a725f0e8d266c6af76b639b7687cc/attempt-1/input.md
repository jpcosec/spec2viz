FILE:desk/tasks/task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados.md
---
sldb:
  by: agent
  at: '2026-11-25T05:43:20Z'
  authority: generated
  via: save_document_payload
id: task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-los-nombres-de-relacion-de-specir-quedan-acotados-a-255-bytes-con-un-resumen-con-hash
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/graph-ui-diccionario-de-componentes/dag.yaml
---

# specir ux extract extrae la interfaz de un arbol y avisa de los archivos saltados

## Rationale

_Explain why this task exists or the business driver behind it._

T2 del plan graph_ui: hoy solo existe specir.extract.extract_frontend en Python y la gramatica ausente se salta en silencio (206 archivos TS/JS en skipped sin aviso). Plan desk/drawer/plans/graph-ui-diccionario-de-componentes/README.md (medicion sobre graph_ui 36adfbb).

## Goal

_Describe the concrete result this task must produce._

Un comando de CLI que corre extract_frontend, avisa de los archivos que code_facts salto, y con --strict falla (rc 1) si hubo saltados.

## Scope

_State what is in scope and what is out of scope._

src/specir/cli.py (grupo ux nuevo con extract), src/specir/extract/__init__.py si hace falta exponer skipped en el ExtractionReport, y un test. Fuera: dictionary y coverage (T8/T9), localizador, cambios en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/IR. Grupo click nuevo 'ux' en src/specir/cli.py (siguiendo como estan declarados catalog y retirement) con el comando 'extract ROOT [--store PATH] [--path P ...]' que llama a specir.extract.extract_frontend y escribe un resumen (nodos creados/actualizados, no derivados). code_facts(root, paths) de sldb ya devuelve la lista 'skipped' junto a 'facts': propagarla al ExtractionReport (campo nuevo skipped: list, default vacio) y que el comando la imprima en stderr como aviso con cuenta y los primeros 10, con el motivo si sldb lo da; rc 0 igual (avisar no es fallar), salvo --strict que da rc 1 si hay saltados. Test nuevo tests/extract/test_ux_extract_cli.py con CliRunner: (a) un arbol con un .tsx extrae y rc 0; (b) con un archivo que code_facts salta (p. ej. simulando skipped con monkeypatch de code_facts) el aviso aparece en stderr y con --strict rc 1. Correr solo ese test y tests/extract/test_frontend_extraction.py.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=src /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/extract/test_ux_extract_cli.py tests/extract/test_frontend_extraction.py

## Done When

_Name the observable condition that makes the task complete._

specir ux extract existe, propaga e imprime los saltados, --strict da rc 1 con saltados, y tests/extract/test_ux_extract_cli.py pasa con tests/extract/test_frontend_extraction.py.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

