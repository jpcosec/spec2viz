# result-summary — task-una-capacidad-del-dominio-declara-para-quien-es-y-cual-es-su-prueba-de-aceptacion-y-las-ocho-capacid

run_id: exec-deskops-e-1d2444804e95
session: (claude, Scion agent; no child session file)
session_sha256: n/a

Code commit (branch deskops/deskops-e-1d2444804e95, worktree .worktrees/deskops-e-1d2444804e95): f5f59e1, no Task-Id trailer (per the brief).

## What
- `CapabilityDoc(DomainOperationDoc)` in src/specir/models/domain.py with `audience: list[str]` (>= 1 non-blank). I did NOT add it to DomainOperationDoc: the extractors (extract/plan.py, django_drf.py) and the blog fixtures create DomainOperationDoc without an audience, and an error rule over all of them would flood any extracted store. A capability is the subclass.
- Link to the test: relation type `accepted_by` (CapabilityDoc -> MaterializationContractDoc, data/relation_types.yaml) + a MaterializationContractDoc (target_kind test, target_identity path::test, source_atoms [capability]). `source_atoms` is not a reference field, so the rule cannot walk it; the RelationDoc edge is what the rule reads.
- Rule `rule-specir-capability-has-an-acceptance-test` (data/rules.yaml): error, on_check.
- View `view-specir-capabilities` (new data/views.yaml, seeded by specir.install: view_seeds): capability, audience, test edge, plus the capabilities' materializations.
- install also registers MaterializationContractDoc (ref deskops.models:...), which needs deskops importable (not a declared dependency of IR).
- Store of IR: specIR installed in it (11+1 models, relation types, rules, view), CodeAnchorDoc registered, 8 CapabilityDoc under specir/capabilities/, materializations for 7 (tests/visual/test_api.py::test_validate_passes) and 8 (tests/visual/test_cli.py::test_render_each_type), two CodeAnchorDoc (intact per `sldb anchors check`).
- Audience values per capability are my reading of the table (not stated in it): 1,3,4,8 [JP, agente]; 2,5 [JP]; 6 [JP, graph_ui]; 7 [agente]. Review them.
- Plan paridad-por-capacidades: README.md and dag.yaml mark the work as replaced by this task. deskops has no verb for plan files (they are not tracked docs), so I edited the two plain files by hand.

## Findings the supervisor must see
- The 6 capabilities without a test (1-6) are reported by the rule as errors, as asked. Consequence: `sldb stores check` and `rules check` of the IR store now exit 1 until they get tests. I made tests/conftest.py (check_store) and tests/test_mcp_undo.py (clean) accept only that rule's errors.
- tests/test_mcp_extension.py::test_specir_types_over_a_store_without_them now uses a new empty store: the IR store has specIR installed now.
- conftest COPIED gets "specir" (the documents' .md live there).
- Unrelated: sldb gained the `anchors_resolve` tool during the run; two tests of test_mcp_extension.py (tool sets) and test_reading_through_every_tool... need it added to SLDB_READ / calls.
- Running specir.install on the IR store re-extracted ~360 existing index yamls and BoardDoc/ReviewDoc model files (the store is stale against the installed sldb). I reverted that noise; the store still has the pre-existing alerts (root-stale, Board contract moved), no new ones.
- The 'ancla intacta' is checked with `sldb anchors check` on the CodeAnchorDoc code:<path>::<test>; the materialization's target_identity matches it by name (the model has no anchor field).

## Files committed
.sldb/core/models/*, .sldb/core/store_index.yaml, .sldb/store.yaml, .sldb/core/documents/{CapabilityDoc,CodeAnchorDoc,ViewDoc,RuleDoc,RelationTypeDoc}/, 2 RelationDoc, 2 MaterializationContractDoc, specir/ (the .md of those docs), desk/drawer/plans/paridad-por-capacidades/{README.md,dag.yaml}, src/specir/{data/relation_types.yaml,data/rules.yaml,data/views.yaml,install.py,models/__init__.py,models/domain.py}, tests/{conftest.py,test_capabilities_as_nodes.py,test_mcp_extension.py,test_mcp_undo.py,models/test_domain_models.py}
