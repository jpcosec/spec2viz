---
sldb:
  by: agent
  at: '2026-11-21T04:20:05Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz.md
- desk/tasks/task-matriz-de-spec2viz-sv-k16-k21-k26-y-k29-pasan-a-sldb-notations-validate-y-se-retiran-los-validate-pr.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb, workspace:desk
tags:
- workspace:desk
---

# IR Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for IR.

## Notes

_Add short operational notes about the current routed set._

Estado al 2026-11-21 (madrugada): cerradas además IR04b (89f8734) y su tarea de cierre (ffc1523) e IR10 (fd05e74: reglas RuleDoc de brechas entre capas y las tools MCP specir_rules y specir_impact). IR13, el gate final de retiro de spec2viz, corrió el 2026-11-21: 'specir retirement check' da rc 1 con 63 dependencias en otros repos (graph_ui, deskops, pron, sldb y el store spec2viz/.sldb) y 8 filas abiertas de la matriz (SV-A17, K09, K16, K18, K21, K23, K26, K29). Detalle en runs/subagents/exec-deskops-e-59807359e541/retirement-check.txt. Queda abierta hasta rc 0: depende de que esos desks migren (sus inboxes tienen los pedidos) y de las capacidades pendientes de las 8 filas. Inbox en 0.

## Task Details

_Generated from the task references above._

- IR13 Migración de consumidores y gate final de retiro de spec2viz [draft] - Un comprobador del gate de retiro y un acta que demuestran, con evidencia, que toda capacidad de spec2viz está cubierta por specIR y que ningún consumidor importa ni invoca spec2viz.
- Matriz de spec2viz: SV-K16, K21, K26 y K29 pasan a sldb notations validate y se retiran los validate provisionales de specIR [draft] - En docs/spec2viz/matriz-de-cobertura.md, SV-K16, SV-K21, SV-K26 y SV-K29 quedan como 'usar sldb directamente' con equivalente 'sldb notations validate', y en estado cumplida, citando un test. SV-K09, SV-K18 y SV-K23 pasan a cumplida si todas sus hijas lo están. specir diagram validate y el alias specir validate se retiran de specIR, y su ayuda y docs/spec2viz/correspondencia-cli.md remiten a sldb notations validate. El test que cubre la tabla de equivalentes (test_every_equivalent_of_the_table_answers_its_help en tests/visual/test_cli.py) invoca 'sldb notations validate --help'. specir retirement check solo deja abierta SV-A17.
