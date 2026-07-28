---
kind: question
author: OpenCode via deskops
created_at: 2026-06-04T00:00:00
status: open
---

# Question: how should existing Mermaid diagrams migrate to spec2viz source specs?

Deskops has semantic diagrams under `docs/diagrams/**/*.mmd` that are currently hand-maintained Mermaid projections. The emerging workflow says structured diagram specs should be source where possible, and rendered Mermaid should be treated as projection.

Questions:

- What is the recommended spec2viz source format for migrating existing Mermaid diagrams?
- Should spec2viz provide an import/scaffold command from Mermaid to a structured source spec?
- Should generated projections carry a header or sidecar metadata indicating the source spec and validation command?
- What validation command should deskops use to prove a structured diagram source and generated Mermaid stay aligned?

Context: deskops wants to use spec2viz the same way it uses SLDB: structured source plus validated human-facing projections.
