---
id: activity.render-error-handling.validate_step
spec: SpecDoc:activity.render-error-handling
element: validate_step
kind: decision
refs: []
atom_refs: []
contains: []
data:
  branches:
    ok: compile_step
    ValidationError: catch_error
---

# validate(diagram): check cross-references

## Description
