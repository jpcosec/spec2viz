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

---

## Renderer And Editing Posture

`spec2viz` treats the semantic spec as the source of truth.

That has a direct consequence for renderer choices:

- D2 is a good text-first renderer target with live preview, but not a true visual drag-and-drop editor
- Vega is suitable for programmable data views, not for visually editing architecture or flow diagrams
- draw.io is a better candidate when visual editing is a hard requirement, but it behaves more like an editable document export than a clean semantic renderer target

So the current bias should be:

- use PlantUML, Mermaid, or D2 when text-first rendering is acceptable
- keep Vega for structured chart-style outputs such as matrix views
- treat draw.io support as a separate export concern driven by explicit visual-editing needs

If visual editing becomes a product requirement, the team must decide explicitly between:

- semantic spec as source of truth with export to a visual tool
- visual editor document as source of truth
- a hybrid model with partial or lossy round-tripping
