# Spec2viz Desk Standards

This `desk/` is the execution surface for `spec2viz` work.

Use it to keep the package aligned with its dual role:

- deterministic semantic compiler core
- formal reflection bridge for outward views and inward enforcement artifacts

---

## Task Rules

1. Separate core compilation tasks from renderer tasks.
2. Any inward-enforcement feature must be artifact-based and deterministic.
3. Any outward-rendering task must name the source IR and target output clearly.
4. Do not let UI/rendering concerns leak into model or compiler semantics.
5. Every task must define which side it strengthens: `core`, `views`, or `reflection`.
