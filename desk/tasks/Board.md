# Spec2viz Tasks Board

## Current State Summary

- Objective: prove `spec2viz` as a formal reflection bridge, not only as a diagram renderer
- Current blocker: inward enforcement use is still architectural intent, not a shipped slice

## Delivery Phases

### Phase 1 - Lock the reflection contract
- `desk/tasks/001-define-semantic-ir-reflection-contract.md`
- `desk/tasks/002-define-enforcement-artifact-shape.md`

### Phase 2 - Prove one bidirectional slice
- `desk/tasks/003-create-canonical-architecture-spec-fixture.md`
- `desk/tasks/004-render-human-facing-diagram-from-fixture.md`
- `desk/tasks/005-compile-enforcement-artifact-from-fixture.md`

### Phase 3 - Prove ecosystem utility
- `desk/tasks/006-prove-architecture-rule-consumption.md`

## Active

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| 003 | fixtures | Create canonical architecture spec fixture | p1 | 001 |
| 004 | views | Render human-facing diagram from fixture | p1 | 001, 003 |
| 005 | reflection | Compile enforcement artifact from fixture | p1 | 001, 002, 003 |
| 006 | integration | Prove architecture rule consumption | p1 | 005 |

## Done

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| 001 | reflection | Define semantic IR reflection contract | p0 | none |
| 002 | enforcement | Define enforcement artifact shape | p0 | 001 |

## Blocked

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| - | - | none | - | - |

## Working Rules

1. Start from `desk/SPEC.md`.
2. Define reflection and enforcement contracts before implementation.
3. Prove each phase with fixtures before advancing.
