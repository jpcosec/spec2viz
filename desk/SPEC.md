# Spec2viz Delivery Spec

`spec2viz` is a deterministic semantic compiler that turns explicit structured specifications into a shared semantic IR.

That IR has two valid uses:

1. outward projection
   - diagrams and views for humans
2. inward formalization
   - rule artifacts, architecture metadata, or enforcement-ready structures for machines

`spec2viz` is therefore both:

- a human-facing visualization tool
- a formal reflection bridge

---

## Real Use Case

We want to author one structured architecture spec once and then:

- render it as Mermaid or PlantUML for human review
- compile the same semantic content into rule artifacts that can help enforce grouped ring boundaries or architecture constraints

The first delivery slice should prove both directions from one source spec.

---

## Minimal Feature Slice To Deliver

1. define one canonical architecture spec fixture
2. compile it into semantic IR
3. render it outward into at least one human-facing diagram
4. compile it inward into one rule/enforcement artifact

---

## Current Strengths

This package already has substantial implementation:

- models
- loader
- validator
- compiler pipeline
- renderers
- CLI
- tests

So the desk should not treat `spec2viz` as empty.
It should focus on the reflection-bridge role that is not yet explicitly delivered.

---

## What Is Still Missing

- explicit use of semantic IR for inward enforcement artifacts
- a canonical example showing one source spec serving both humans and machines
- a documented boundary between compiler core and reflection outputs

---

## Non-Goals For The First Slice

Out of scope for the first reflection slice:

- full generalized policy engine generation
- large architecture-lint framework implementation
- broad multi-backend optimization work

The first slice only needs to prove one real reflection path.
