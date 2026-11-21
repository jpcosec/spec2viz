# Result summary

- run_id: run-deskops-e-5ccf277d5e67
- session: scion://agent/deskops-e-5ccf277d5e67
- session_sha256: n/a (Scion agent, no transcript file)
- task: task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac

## What was done
No file of IR imports or runs spec2viz any more. `specir retirement check` (output in `retirement-check.txt`) lists 0 IR dependencies (the 19 left are spec2viz's own store, outside scope; matrix row SV-A17 is open, not this task's).

- New `tests/visual/oracle.py` + golden `tests/visual/goldens/spec2viz-2de1056-oracle.json` (73+ answers): each former live comparison asks `oracle.expect(kind, ...)` (answer keyed by test id + call number) or `oracle.frozen(name)` (spec2viz-owned inputs/lists) and compares to the golden. Same tests, same parametrization, same inputs.
- Recorder: `runs/subagents/exec-deskops-e-5ccf277d5e67/record_goldens.py` (outside tests/). It recomputes the 4 existing goldens with spec2viz (verified byte-identical: `--check-existing`), and records the oracle golden by running the parity tests with spec2viz live (the tests assert live == recorded while recording). `--only <pytest args>` re-records a subset. spec2viz checkout code/tests are unchanged since 2de1056 (checkout HEAD is 91ba1d0, desk commits only), so the golden is named 2de1056.
- parity.py / render_parity.py: spec2viz_* helpers, write_goldens and __main__ removed (moved to the recorder).
- Live tests deleted because existing goldens already cover them: test_specir_matches_spec2viz (44), test_specir_renders_what_spec2viz_renders (36), test_specir_exports_what_spec2viz_exports, test_specir_finds_what_spec2viz_finds, and the "saved oracle is last run" pair (2; they compared a golden with live spec2viz).
- Converted to golden: selector/extensions/defaults, view_to_mermaid (8), render_to_file (6), resource bytes (SHA-256), check_catalog (12), catalog sync/failure, catalog pages (digest + warnings), strict atoms, sync of fixtures (14) and sync specs, graph-import snapshots/store, python-AST generation, and the matriz test (CLI commands, modules and test files lists frozen: no longer reads the spec2viz checkout).
- test_visual_names: the "imported only by the oracle" test now expects nobody (renamed test_spec2viz_is_imported_by_nobody). test_cli.py: its table test used matrix.commands_from_source, now matrix.cli_commands (frozen).

## Validation (validation.log)
`PYTHONHASHSEED=3 python -m pytest -q -p no:cacheprovider tests/visual tests/test_matriz_cobertura_spec2viz.py -rs` with spec2viz NOT installed: 615 passed, 13 skipped, exit 0 (skips: mmdc, sldb/graph_ui/pron repos not in worktree, test_api reads spec2viz source file).
Baseline (spec2viz installed, before): 683 collected; now 628. The 55 fewer are the live duplicates listed above (only ones with an existing golden twin); every other test id is kept, and the catalog/sync/etc. parity cases that were skipped without spec2viz now run (63 with the parity marker).

## Reviewer notes / caveats
- Catalog pages are kept as SHA-256 (pages are >100 KB). Normalized before hashing: view-id path hash (`-1a2b3c4d`), atom `aliases` order, and the `"4 nueva"`/`"nueva"` key — all PYTHONHASHSEED/tmp-path dependent in both specIR and spec2viz.
- python-AST parity now runs on a frozen copy of src/specir held in the golden, so it no longer moves with src/.
- Left alone (out of scope, no import): tests/visual/test_api.py reads spec2viz's __init__.py source if the checkout exists; pyproject marker text for `parity` still says "skipped when spec2viz is not installed".
- Files changed: tests/test_matriz_cobertura_spec2viz.py tests/visual/parity.py tests/visual/render_parity.py tests/visual/oracle.py tests/visual/test_catalog_parity.py tests/visual/test_cli.py tests/visual/test_lint_mermaid.py tests/visual/test_render_cases.py tests/visual/test_render_commands.py tests/visual/test_render_parity.py tests/visual/test_resources.py tests/visual/test_schema.py tests/visual/test_sync_generation_parity.py tests/visual/test_visual_names.py tests/visual/test_visual_parity.py tests/visual/goldens/spec2viz-2de1056-oracle.json
