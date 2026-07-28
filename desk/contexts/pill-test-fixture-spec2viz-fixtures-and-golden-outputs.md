---
# pill-xxx
id: pill-test-fixture-spec2viz-fixtures-and-golden-outputs
# e.g., language:python, library:pydantic
tags: []
---

# Test Fixture: spec2viz fixtures and golden outputs

## What

_Define the context or guardrail this pill carries._

Spec2viz fixture and golden-output tasks must preserve a clear contract between canonical input specs, rendered artifacts, and expected diffs.

## Why

_Explain why this context matters for safe execution._

Spec2viz proves reflection through artifacts. Golden files are not incidental snapshots; they are executable expectations. Updating them without a contract hides regressions.

## When

_Describe when an agent should apply this pill._

Apply to tasks touching examples, fixtures, PlantUML/Mermaid/D2 output, enforcement artifacts, batch rendering, or golden file synchronization.

## Where

_Name the files, surfaces, or scope this pill applies to._

Primary owner surfaces: examples, tests, renderer output fixtures and golden files, renderers, loader.py

## How

_Describe the correct way to apply this guidance._

Regenerate the affected artifact, diff it against the golden file, and explain whether each diff is intentional. For batch tasks, verify every expected artifact is regenerated and no unrelated golden file changes.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not bulk overwrite goldens to get tests green. Do not mix fixture schema changes with renderer changes unless the task explicitly couples them.
