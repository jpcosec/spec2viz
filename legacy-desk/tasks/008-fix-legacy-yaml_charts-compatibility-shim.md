---
id: '008'
domain: compat
status: open
priority: p0
depends_on: []
created: ''
---

# Fix legacy yaml_charts compatibility shim

## Objective

CLI-managed task materialized from the desk board source of truth.

## Reference

- Finding: SPEC2VIZ-16
- Board: `spec2viz/desk/tasks/Board.md`
- Desk: `spec2viz`

## What to Fix

- Domain: `spec2viz/compat`
- Priority: `p0`
- Status: `open`
- Location: `spec2viz/spec2vix/` package

The `spec2vix/` package exists but never creates a top-level `yaml_charts` module. The docs (README, atom-spec2viz, COVERAGE) all claim legacy imports work.

## How to Do It

Add a top-level compatibility shim so that `import yaml_charts` works and emits a deprecation warning pointing users to the new `spec2viz` package. The shim should be installed by the package's wheel/pip entry points so it is available at the `yaml_charts` import path.

## Pills

- `desk/contexts/pill-001-spec2viz-contract-validation.md`
- `../../../../desk/contexts/pill-001-current-desk-execution-gates.md`
- `../../../../desk/contexts/pill-002-modular-task-boundaries.md`
- `../../../../desk/contexts/pill-003-cli-stress-test-validation.md`

## Validation

`python -c "import yaml_charts"` succeeds and prints a deprecation warning.
