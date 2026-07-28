---
id: '007'
domain: views
status: open
priority: p2
depends_on:
- '004'
created: ''
---

# Add D2 renderer spike from existing IR

## Objective

Prove that `spec2viz` can target D2 as an additional outward renderer without changing semantic models or compiler behavior.

## Reference

- Board: `spec2viz/desk/tasks/Board.md`
- Desk: `spec2viz`

## What to Fix

- Domain: `views`
- Priority: `p2`
- Status: `open`
- Source IR: `SequenceIR`, `StateIR`, `ComponentIR`, `ActivityIR`, `DeploymentIR`
- Target output: D2 source text

## How to Do It

Add a D2 renderer spike behind the existing renderer boundary.

Keep the work renderer-only at first:

- implement `spec2viz/renderers/d2.py`
- register the renderer in `spec2viz/renderers/__init__.py`
- start with graph-friendly diagram families first
- leave `MatrixIR` on Vega unless a D2 representation is clearly better
- do not treat D2 as a visual editing solution; this spike is about text-first rendering only

## Pills

- `desk/contexts/pill-001-spec2viz-contract-validation.md`
- `desk/contexts/pill-002-fixture-and-golden-output-contract.md`
- `../../../../desk/contexts/pill-001-current-desk-execution-gates.md`
- `../../../../desk/contexts/pill-002-modular-task-boundaries.md`

## Validation

Render at least one existing fixture per supported diagram family to D2 text and confirm the generated output is structurally valid D2.
