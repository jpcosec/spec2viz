---
sldb:
  by: agent
  at: '2026-11-16T00:51:33Z'
  authority: generated
  via: create_document
# runtime-xxx
id: runtime-claude-en-scion
# draft | active | archived
status: active
# Runtime binary identifier matching RoleDoc.kind values, e.g. pi, claude, codex
kind: claude
binary: claude
# Empty means this runtime does not support that capability
model_flag: ''
fallback_models_flag: ''
# comma | space | repeat
fallback_models_join: comma
tools_flag: --allowedTools
# comma | space | repeat
tools_join: comma
system_prompt_flag: ''
# inline | file
system_prompt_delivery: inline
# Optional fixed system prompt text; empty means role-provided
system_prompt: ⸢rev•system_prompt⸥
session_flag: ''
extra_args: []
# RoleDoc fields this runtime cannot honor
unsupported_role_fields: []
# e.g. system:deskops
tags:
- system:deskops
---

# Claude en scion

## Summary

_Summarize what this runtime is and when to use it._

Claude Code (OAuth de suscripción, secret CLAUDE_AUTH) como harness de scion para los ejecutores del desk de IR.

## Notes

_Operational notes such as authentication requirements or version pins._

Sin API key: el hub usa el secret CLAUDE_AUTH (OAuth de suscripción). El template lo genera deskops runtime template con --harness claude; model va como alias de tamaño (medium) y lo resuelve el harness-config claude del fork.
