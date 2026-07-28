# Test Fixture: spec2viz fixtures and golden outputs

ID: pill-002

## What

Spec2viz fixture and golden-output tasks must preserve a clear contract between canonical input specs, rendered artifacts, and expected diffs.

## Why

Spec2viz proves reflection through artifacts. Golden files are not incidental snapshots; they are executable expectations. Updating them without a contract hides regressions.

## When

Apply to tasks touching examples, fixtures, PlantUML/Mermaid/D2 output, enforcement artifacts, batch rendering, or golden file synchronization.

## Where

Primary owner surfaces:

- `tools/spec2viz/examples/`
- `tools/spec2viz/tests/`
- renderer output fixtures and golden files
- `tools/spec2viz/spec2viz/renderers/`
- `tools/spec2viz/spec2viz/loader.py`

## Required Reads

- Read the task file.
- Read this pill and `pill-001-spec2viz-contract-validation.md`.
- Read only the fixture, renderer, and golden files named by the task.

## Execution Boundary

Only update golden files when generated output changes intentionally. If output changes because of renderer drift, fix the renderer instead of blessing the drift.

## Validation Contract

Regenerate the affected artifact, diff it against the golden file, and explain whether each diff is intentional. For batch tasks, verify every expected artifact is regenerated and no unrelated golden file changes.

## How Not

Do not bulk overwrite goldens to get tests green. Do not mix fixture schema changes with renderer changes unless the task explicitly couples them.

## Drift Signals

- Golden files change without a corresponding task reason.
- A fixture validates only because schema validation was weakened.
- Batch rendering skips files silently.
- Output paths change without tests noticing.

## Tags

- system:spec2viz
- topic:fixtures
- topic:golden-files
