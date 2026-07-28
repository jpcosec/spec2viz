# Spec2viz Tasks Board

## Current State Summary

- Objective: prove `spec2viz` as a formal reflection bridge, not only as a diagram renderer
- Current blocker: inward enforcement use is still architectural intent, not a shipped slice

## Delivery Phases



### Phase 4 - Expand renderer reach
- `desk/tasks/007-add-d2-renderer-spike.md`

## Active

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| 007 | views | Add D2 renderer spike from existing IR | p2 | 004 |
| 008 | compat | Fix legacy yaml_charts compatibility shim | p0 | none |
| 009 | fixtures | Sync golden PlantUML files | p1 | 003 |

## Blocked

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| - | - | none | - | - |

## Working Rules

1. Start from `desk/SPEC.md`.
2. Define reflection and enforcement contracts before implementation.
3. Prove each phase with fixtures before advancing.
