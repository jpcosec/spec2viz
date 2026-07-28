# Pattern: preserve spec2viz contracts while fixing CLI behavior

ID: pill-001

## What

This pill gives a fresh subagent the minimum context needed to execute a spec2viz task without drifting from CLI repair into renderer redesign.

## Why

Spec2viz is a formal reflection bridge, not just a renderer. Fixing user-facing command crashes can accidentally drift the schema names, aliases, fixture expectations, or generated artifacts away from the contract.

## When

Apply to tasks that touch `schema`, `validate`, `render`, renderer discovery, batch rendering, compatibility shims, or golden files.

## Where

Primary owner files:

- `tools/spec2viz/spec2viz/cli.py`
- `tools/spec2viz/spec2viz/schema.py`
- `tools/spec2viz/spec2viz/loader.py`
- `tools/spec2viz/spec2viz/renderers/`
- `tools/spec2viz/examples/`
- `tools/spec2viz/tests/`

## Required Reads

- Read the assigned task file.
- Read this pill.
- Read `desk/SPEC.md` only if the task changes reflection/enforcement semantics.
- Read the specific renderer/schema/fixture files named by the task.

## Execution Boundary

Keep the canonical diagram contract intact. Add user-facing aliases or errors at the CLI boundary, but do not rename internal diagram types unless the task explicitly says to update schemas, fixtures, and golden outputs together.

## How

Validate through CLI commands and compare generated artifacts when fixtures or golden files are involved. Keep aliases user-friendly without hiding canonical diagram types.

## Validation Contract

For schema/render/validate tasks, check the failing command, valid command, invalid input command, and any promised generated file diff.

## How Not

Do not fix a crash by weakening schema validation or silently changing canonical fixture output without updating the expected artifact intentionally. Do not add compatibility shims beyond the named legacy surface.

## Drift Signals

- The executor changes canonical diagram names to satisfy one alias.
- The executor updates golden files without explaining the behavior change.
- The executor fixes a renderer path but leaves schema/export behavior inconsistent.
- The executor broadens legacy compatibility beyond the named shim task.

## Tags

- system:spec2viz
- topic:cli
- topic:contract
