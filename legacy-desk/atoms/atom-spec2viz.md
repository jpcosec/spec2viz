---
atom_id: spec2viz
status: draft
kind: code
maturity: active
created_by: subagent
date: 2026-06-02
---

# spec2viz

## What it is
spec2viz is a Python tool that compiles semantic YAML diagram specs into renderer-agnostic intermediate representations and outputs PlantUML, Mermaid, or SVG for sequence, state, component, activity, deployment, and matrix diagrams.

## Why
Within the hum-ecosystem, spec2viz provides the human-watchable rendering layer over canonical specYaml semantics. It separates semantic model from rendering so that teams author structured YAML once and produce multiple visual artifact formats without hand-editing diagram mark-up languages.

## How it's made
Python 3.11+ with Pydantic 2.0 for model validation, PyYAML for parsing, and Click for the CLI. The pipeline follows a strict Model → Compiler → IR → Renderer separation. Tests use pytest; no extra lint or type-check tooling beyond what the project uses informally. A legacy yaml-charts import shim exists for backward compatibility.

## When
First packaged release v0.1.0 was 2026-04-22, renamed from yaml-charts. v0.2.0 followed on 2026-05-01 with reflection/enforcement models. This places spec2viz in the early active phase of the ecosystem's second tooling generation.

## Purpose
To let teams author structured diagram specs as YAML (semantic truth) and render them into multiple visual backends, ensuring that diagram artifacts are versionable, LLM-editable, and reproducible — without manual PUML/Mermaid editing.

## Patterns
- **Strict pipeline separation**: Model → Compiler → IR → Renderer, with clear boundaries enforced in DEVELOPER_GUIDE.md and STANDARDS.md
- **Renderer-agnostic IR**: The intermediate representation carries only graphic intent, not renderer specifics; backends are plugged in via a registry
- **Legacy compatibility shims**: Old `yaml_charts` imports and `yaml-charts` CLI commands still resolve with deprecation warnings
- **Fixture-driven testing**: Every diagram type has a YAML fixture under `tests/fixtures/` and a corresponding test file
- **Schema generation**: Pydantic models are exposed as JSON Schema for editor integration

## State of maturity
Active. The core six diagram types (component, sequence, state, activity, deployment, matrix) are implemented and tested. CLI and Python API are stable. v0.2.0 added the reflection/enforcement model. Documentation is current. No known unused code paths. No automated CI pipeline is visible in the repo.

## Open questions
- How does `spec2viz` relate to the `specyaml/` project mentioned in the README — is that a sibling, a parent, or planned work?
- The `spec2viz/spec2vix/` subpackage exists but appears empty (only `__init__.py`) — is it dead code or placeholder for future work?
- No CI configuration (GitHub Actions, etc.) is present; is the project intended to be CI-free, or is that forthcoming?
- What is the Vega backend status — it's listed as a supported output but no Vega-specific renderer implementation is visible in `spec2viz/renderers/`

## References
- `README.md` — project overview, install, CLI, API, examples
- `spec.md` — the 957-line semantic spec that defines the YAML schema for every diagram type
- `pyproject.toml` — package metadata and dependencies
- `DEVELOPER_GUIDE.md` — how to add a new diagram type
- `CHANGELOG.md` — release history
- `desk/STANDARDS.md` — local desk conventions
- `packaging instructions.md` — packaging checklist
- `spec2viz/__init__.py` — public API surface
- `spec2viz/cli.py` — CLI entry point
- `spec2viz/ir.py` — intermediate representation dataclasses
- `spec2viz/models/` — Pydantic model definitions per diagram type
- `spec2viz/compilers/` — model-to-IR compilers
- `spec2viz/renderers/` — IR-to-output renderers (PlantUML, Mermaid)
- `examples/` — sample YAML specs and generated artifacts
- `tests/` — test suite (30+ test files)
