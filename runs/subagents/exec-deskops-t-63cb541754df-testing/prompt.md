Task: task-matriz-de-spec2viz-sv-k16-k21-k26-y-k29-pasan-a-sldb-notations-validate-y-se-retiran-los-validate-pr
Title: Matriz de spec2viz: SV-K16, K21, K26 y K29 pasan a sldb notations validate y se retiran los validate provisionales de specIR
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-21T06:29:13Z'
  authority: generated
  via: save_document_payload
id: task-matriz-de-spec2viz-sv-k16-k21-k26-y-k29-pasan-a-sldb-notations-validate-y-se-retiran-los-validate-pr
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Matriz de spec2viz: SV-K16, K21, K26 y K29 pasan a sldb notations validate y se retiran los validate provisionales de specIR

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: sldb publicó 'sldb notations validate <nombre|ruta> [--json] [--store S]' (valida una notación, una paleta o un spec; findings notations/<tipo>-invalid; exit 0 sin errores, 1 con alguno). Era lo que pedían las filas SV-K16 y SV-K29 (decisión de IR13d: specir diagram validate y specir validate quedaban provisionales hasta que sldb tuviera su comando) y SV-K21 y SV-K26 (remitían a load_notation y load_palette porque sldb no tenía comando). specir retirement check (2026-11-21) da 8 filas abiertas: SV-A17, K09, K16, K18, K21, K23, K26 y K29. K09, K18 y K23 son subgrupos que esperan a sus hijas.

## Goal

_Describe the concrete result this task must produce._

En docs/spec2viz/matriz-de-cobertura.md, SV-K16, SV-K21, SV-K26 y SV-K29 quedan como 'usar sldb directamente' con equivalente 'sldb notations validate', y en estado cumplida, citando un test. SV-K09, SV-K18 y SV-K23 pasan a cumplida si todas sus hijas lo están. specir diagram validate y el alias specir validate se retiran de specIR, y su ayuda y docs/spec2viz/correspondencia-cli.md remiten a sldb notations validate. El test que cubre la tabla de equivalentes (test_every_equivalent_of_the_table_answers_its_help en tests/visual/test_cli.py) invoca 'sldb notations validate --help'. specir retirement check solo deja abierta SV-A17.

## Scope

_State what is in scope and what is out of scope._

Dentro: docs/spec2viz/matriz-de-cobertura.md, docs/spec2viz/correspondencia-cli.md, la definición de specir diagram validate y specir validate en src/specir (borrarlas), tests/visual/test_cli.py y los tests que llamen a esos comandos, CHANGELOG si existe. Fuera: SV-A17 (store de spec2viz), los tests de paridad que importan spec2viz y el acta de retiro.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: actualizar la tabla de equivalentes y el test para que 'sldb notations validate --help' responda. p2: borrar specir diagram validate y specir validate y ajustar sus tests (que ahora comprueben que specIR no los define, como test_specir_defines_no_command_ hace para otros). p3: actualizar las cuatro filas y las tres de subgrupo en la matriz, citando el test. p4: correr specir retirement check con las rutas del inventario y dejar la salida en el run dir: solo SV-A17 abierta. p5: commit desde tu worktree con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/visual/test_cli.py tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py

## Done When

_Name the observable condition that makes the task complete._

tests/visual/test_cli.py, tests/test_matriz_cobertura_spec2viz.py y tests/visual/test_retirement_gate.py pasan, y specir retirement check lista solo SV-A17 entre las filas abiertas.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-matriz-de-spec2viz-sv-k16-k21-k26-y-k29-pasan-a-sldb-notations-validate-y-se-retiran-los-validate-pr"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
