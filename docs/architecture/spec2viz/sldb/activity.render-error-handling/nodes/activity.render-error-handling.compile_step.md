---
id: activity.render-error-handling.compile_step
spec: SpecDoc:activity.render-error-handling
element: compile_step
kind: decision
collection: steps
refs: []
atom_refs: []
contains: []
data:
  branches:
    ok: render_step
    CompileError: catch_error
---

# compile_ir(diagram): pattern-match compiler

## Description
