---
id: '009'
domain: fixtures
status: open
priority: p1
depends_on:
- '003'
created: ''
---

# Sync golden PlantUML files

## Objective

CLI-managed task materialized from the desk board source of truth.

## Reference

- Finding: SPEC2VIZ-17
- Board: `spec2viz/desk/tasks/Board.md`
- Desk: `spec2viz`

## What to Fix

- Domain: `spec2viz/fixtures`
- Priority: `p1`
- Status: `open`
- Location: `examples/*/example.puml` golden files

Only `activity/example.puml` matches current output. The `component`, `deployment`, `sequence`, and `state` golden PlantUML files are stale and differ from the current render output.

## How to Do It

Regenerate each stale golden `.puml` file by running the current render pipeline against the corresponding YAML fixture. Review the diffs to confirm the changes are intentional (renderer improvements, not regressions). Commit the updated golden files.

## Pills

- `desk/contexts/pill-001-spec2viz-contract-validation.md`
- `desk/contexts/pill-002-fixture-and-golden-output-contract.md`
- `../../../../desk/contexts/pill-001-current-desk-execution-gates.md`
- `../../../../desk/contexts/pill-002-modular-task-boundaries.md`

## Validation

For each diagram family, `diff examples/<family>/example.puml <(spec2viz render examples/<family>/example.yml --renderer plantuml -)` shows no diff.
