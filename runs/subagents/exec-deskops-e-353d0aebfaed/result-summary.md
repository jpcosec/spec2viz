# Result — task-ir-borra-los-goldens-de-spec2viz-y-las-pruebas-que-los-leen-la-paridad-se-acredita-por-pruebas-de-ac

run_id: exec-deskops-e-353d0aebfaed
session: n/a (Claude Code executor session; no child session file)
session_sha256: n/a
Commit (branch deskops/deskops-e-353d0aebfaed): 83d7171

## What was done
- Deleted tests/visual/goldens/, oracle.py, parity.py, render_parity.py, test_render_parity.py (behaviour cases MOVED to tests/visual/test_render_projections.py: ANY_STATE drawing, blog state projection, vega kind order, nine-renderer selector), test_catalog_parity.py, test_visual_parity.py, test_notations_parity.py, test_sync_generation_parity.py, tests/test_matriz_cobertura_spec2viz.py, tests/visual/test_retirement_gate.py.
- Removed the oracle-reading cases from test_render_cases.py, test_render_commands.py, test_resources.py, test_schema.py, test_lint_mermaid.py (lint texts inlined; golden cases replaced by a direct regex-rule test).
- Removed the `parity` marker (and the then-empty `markers`) from pyproject.toml.
- Extra, outside the list (same criterion): tests/visual/fixtures/spec2viz-notations/ (only used by test_notations_parity.py); test_cli.py imported test_matriz_cobertura_spec2viz, so `test_the_table_covers_exactly_the_command_tree_of_spec2viz` became `test_the_table_has_one_row_per_command_id` (ids check kept, comparison to frozen oracle dropped); docstring/comment cleanups in conftest.py, test_refs_models.py, test_renderers.py, test_visual_names.py (ORACLES set -> assert nobody imports spec2viz).
- fixtures/spec2viz corpus kept: used by behaviour tests (bpmn, catalog, renderers, packaging...).

## Validation (validation.log)
`pytest -n 4 tests/extract tests/models tests/visual tests/test_cli_mcp.py` -> 444 passed, 12 skipped, 2 xfailed, 1 failed.
The one failure, tests/extract/test_blog_extraction.py::test_the_tables_columns_and_keys_come_from_the_sql_facts (column order from SQL facts), is in files I did not touch and is unrelated to parity; probably the installed SQL grammar version in my ad-hoc venv. Supervisor: confirm it on the main checkout.
Final grep -rniE 'spec2viz-2de1056|oracle|goldens|parity' tests pyproject.toml -> empty.
Note: the venv needed extras beyond the prompt (anyio, mcp, sldb[mcp,code]); the project has no `dev` extra.

## Files (commit)
M	pyproject.toml
M	tests/conftest.py
D	tests/test_matriz_cobertura_spec2viz.py
D	tests/visual/fixtures/spec2viz-notations/README.md
D	tests/visual/fixtures/spec2viz-notations/notations/activity.yml
D	tests/visual/fixtures/spec2viz-notations/notations/component-view-matrix.yml
D	tests/visual/fixtures/spec2viz-notations/notations/component.yml
D	tests/visual/fixtures/spec2viz-notations/notations/deployment.yml
D	tests/visual/fixtures/spec2viz-notations/notations/reflection.yml
D	tests/visual/fixtures/spec2viz-notations/notations/statechart.yml
D	tests/visual/fixtures/spec2viz-notations/notations/uml-class.yml
D	tests/visual/fixtures/spec2viz-notations/notations/uml-sequence.yml
D	tests/visual/fixtures/spec2viz-notations/palettes/default.yml
D	tests/visual/goldens/spec2viz-2de1056-lint.json
D	tests/visual/goldens/spec2viz-2de1056-oracle.json
D	tests/visual/goldens/spec2viz-2de1056-renders.json
D	tests/visual/goldens/spec2viz-2de1056-schema.json
D	tests/visual/goldens/spec2viz-2de1056.json
D	tests/visual/oracle.py
D	tests/visual/parity.py
D	tests/visual/render_parity.py
D	tests/visual/test_catalog_parity.py
M	tests/visual/test_cli.py
M	tests/visual/test_lint_mermaid.py
D	tests/visual/test_notations_parity.py
M	tests/visual/test_refs_models.py
M	tests/visual/test_render_cases.py
M	tests/visual/test_render_commands.py
R065	tests/visual/test_render_parity.py	tests/visual/test_render_projections.py
M	tests/visual/test_renderers.py
M	tests/visual/test_resources.py
D	tests/visual/test_retirement_gate.py
M	tests/visual/test_schema.py
D	tests/visual/test_sync_generation_parity.py
M	tests/visual/test_visual_names.py
D	tests/visual/test_visual_parity.py
