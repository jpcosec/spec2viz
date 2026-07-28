---
# pill-xxx
id: pill-pattern-preserve-spec2viz-contracts-while-fixing-cli-behavior
# e.g., language:python, library:pydantic
tags: []
---

# Pattern: preserve spec2viz contracts while fixing CLI behavior

## What

_Define the context or guardrail this pill carries._

This pill gives a fresh subagent the minimum context needed to execute a spec2viz task without drifting from CLI repair into renderer redesign.

## Why

_Explain why this context matters for safe execution._

Spec2viz is a formal reflection bridge, not just a renderer. Fixing user-facing command crashes can accidentally drift the schema names, aliases, fixture expectations, or generated artifacts away from the contract.

## When

_Describe when an agent should apply this pill._

Apply to tasks that touch schema, validate, render, renderer discovery, batch rendering, compatibility shims, or golden files.

## Where

_Name the files, surfaces, or scope this pill applies to._

Primary owner files: cli.py, schema.py, loader.py, renderers, examples, tests

## How

_Describe the correct way to apply this guidance._

Validate through CLI commands and compare generated artifacts when fixtures or golden files are involved. Keep aliases user-friendly without hiding canonical diagram types.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not fix a crash by weakening schema validation or silently changing canonical fixture output without updating the expected artifact intentionally. Do not add compatibility shims beyond the named legacy surface.
