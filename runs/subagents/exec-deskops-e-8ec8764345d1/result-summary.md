# IR10 result summary

run_id: exec-deskops-e-8ec8764345d1
session: not available to the executor (no child session path recorded)
session_sha256: not available

## What was done (worktree .worktrees/deskops-e-8ec8764345d1, branch deskops/deskops-e-8ec8764345d1)
- Rules (RuleDoc, data/rules.yaml, evaluated by sldb `rules_check`): added `rule-specir-interface-field-is-served` (error),
  `rule-specir-entity-is-persisted` (alert), `rule-specir-policy-reaches-the-interface` (alert); the existing ones cover
  control->action, action->API op (error), op->handler, handler->domain op. Edge-provenance rule now lists bound_to/field_of.
- New types needed by the field rule: `InterfaceFieldDoc`, `ApiFieldDoc`; relation types `bound_to`, `field_of`.
  (Decision for review: the model had no field-level node, so the "interface field absent from the serializer" gap needed them.)
- `src/specir/impact.py`: domain mapping only; paths come from `sldb.api.graph.graph_path(explain=True)`; each hop gets the
  origen/verificacion/evidencia of its RelationDoc; `inferred` flag when a hop is `inferido`.
- `src/specir/mcp_extension.py`: read-only tools `specir_rules` and `specir_impact` (node, field, direction dependents|dependencies, layer).
- Tests: tests/models/test_rules_and_impact.py (seeded gap per rule, clean blog, status->PublishButton full path, provenance and inferred
  flag, no writes by tree digest, no patch keys, no own graph traversal); updated counts in test_domain_models.py and tool list in test_mcp_extension.py.

## Validation
See validation.log. tests/visual was not run (untouched surface).

## For the supervisor
- Impact "dependents" is directed (nodes whose chain leads to the changed node); `dependencies` is the reverse. Policy is not a dependent of a table.
- `field` is validated against the node's columns/fields; it labels the change, the traversal is node-level.
