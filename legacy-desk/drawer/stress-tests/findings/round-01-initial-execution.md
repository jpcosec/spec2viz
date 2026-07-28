# Round 01: Initial execution of spec2viz stress tests

## Summary
- STs executed: ST-schema, ST-validate, ST-render, ST-render-combos, ST-render-multi, ST-plantuml, ST-mermaid, ST-edge-cases, ST-reflection, ST-api
- Total findings: 18

## Findings

### Finding SPEC2VIZ-01: `schema --type <invalid>` dumps full Python traceback
- **ST**: ST-schema
- **Step**: 6
- **Command**: `spec2viz schema --type nonexistent`
- **Expected**: User-friendly error: "Error: 'nonexistent' is not a valid diagram type. Valid types: sequence, state, component, activity, deployment, component_view_matrix, reflection"
- **Observed**: Full 12-line Python traceback ending in `ValueError: 'nonexistent' is not a valid DiagramType` with no suggestion of valid types
- **Severity**: medium
- **Type**: error-message

### Finding SPEC2VIZ-02: `schema --type matrix` fails — diagram type is `component_view_matrix` not `matrix`
- **ST**: ST-schema
- **Step**: 9
- **Command**: `spec2viz schema --type matrix`
- **Expected**: Schema output or clear error saying "use --type component_view_matrix"
- **Observed**: Full traceback: `ValueError: 'matrix' is not a valid DiagramType`. The enum value is `component_view_matrix` but the example directory is `examples/matrix/` and fixtures use `type: matrix` in YAML
- **Severity**: medium
- **Type**: discoverability / consistency

### Finding SPEC2VIZ-03: Batch validate output ambiguous with same-named files
- **ST**: ST-validate
- **Step**: 12
- **Command**: `spec2viz validate examples/sequence/example.yml examples/state/example.yml examples/component/example.yml`
- **Expected**: Each file identified clearly, e.g. "examples/sequence/example.yml: OK"
- **Observed**: All three show "example.yml: OK" — no way to tell which file passed since they share the same basename
- **Severity**: low
- **Type**: discoverability

### Finding SPEC2VIZ-04: Passing a directory dumps IsADirectoryError traceback
- **ST**: ST-validate (also ST-edge-cases step 4)
- **Step**: 13
- **Command**: `spec2viz validate examples/`
- **Expected**: "Error: 'examples' is a directory. Please specify a YAML file."
- **Observed**: Full 12-line traceback ending in `IsADirectoryError: [Errno 21] Is a directory: 'examples'`
- **Severity**: medium
- **Type**: error-message

### Finding SPEC2VIZ-05: Empty file dumps AttributeError traceback
- **ST**: ST-edge-cases
- **Step**: 3
- **Command**: `echo "" > /tmp/viz-empty.yml && spec2viz validate /tmp/viz-empty.yml`
- **Expected**: "Error: empty file" or "Error: YAML parse error"
- **Observed**: Full traceback: `AttributeError: 'NoneType' object has no attribute 'get'` (yaml.safe_load returns None for empty string)
- **Severity**: medium
- **Type**: error-message

### Finding SPEC2VIZ-06: Batch render overwrites output files with same basename
- **ST**: ST-render, ST-render-multi, ST-render-combos
- **Step**: 12 (ST-render), 1-3 (ST-render-multi), 1-2 (ST-render-combos)
- **Command**: `spec2viz render examples/sequence/example.yml examples/state/example.yml --out /tmp/viz-out --renderer mermaid`
- **Expected**: Each input produces a unique output file (e.g. `sequence-example.mmd`, `state-example.mmd`)
- **Observed**: All inputs named `example.yml` produce the same output filename `example.mmd`. The last file rendered overwrites all previous ones. Only 1 file exists instead of N.
- **Severity**: high
- **Type**: silent-failure

### Finding SPEC2VIZ-07: No `--continue-on-error` flag — batch stops at first failure
- **ST**: ST-render-multi
- **Step**: 4
- **Command**: `spec2viz render /tmp/viz-bad.yml examples/sequence/example.yml --out /tmp/viz-batch 2>&1`
- **Expected**: Warns about bad file, continues with valid files
- **Observed**: Stops at first error. Exit code 1. No "2 files: 1 failed, 1 succeeded" summary.
- **Severity**: medium
- **Type**: edge-case

### Finding SPEC2VIZ-08: No batch summary output after multi-file render
- **ST**: ST-render-multi
- **Step**: 5
- **Command**: `spec2viz render 6 example files --out /tmp/viz-all --renderer mermaid`
- **Expected**: Summary like "5/6 rendered successfully, 1 failed (matrix: MermaidRenderer cannot render MatrixIR)"
- **Observed**: Renders files one by one, stops abruptly at the error with no final tally
- **Severity**: low
- **Type**: discoverability

### Finding SPEC2VIZ-09: Render without `--out` writes to CWD silently
- **ST**: ST-render
- **Step**: 10
- **Command**: `spec2viz render examples/sequence/example.yml --renderer plantuml`
- **Expected**: Writes to CWD as documented, but should perhaps warn or use a dedicated output dir
- **Observed**: Renders `example.puml` to CWD (`/home/jp/proyectos/hum-ecosystem/tools/spec2viz/`). No warning. Output file mixes with project files.
- **Severity**: low
- **Type**: discoverability

### Finding SPEC2VIZ-10: `-h` is not a valid option (Click default)
- **ST**: ST-edge-cases
- **Step**: 8
- **Command**: `spec2viz -h`
- **Expected**: `-h` should show help (standard CLI convention)
- **Observed**: "Error: No such option '-h'." Only `--help` works.
- **Severity**: low
- **Type**: discoverability

### Finding SPEC2VIZ-11: No `--version` flag
- **ST**: ST-edge-cases
- **Step**: 14
- **Command**: `spec2viz --version`
- **Expected**: Version number
- **Observed**: "Error: No such option '--version'."
- **Severity**: low
- **Type**: discoverability

### Finding SPEC2VIZ-12: `python -m spec2viz` not supported
- **ST**: ST-edge-cases
- **Step**: 13
- **Command**: `python -m spec2viz --help`
- **Expected**: Same output as `spec2viz --help`
- **Observed**: "No module named spec2viz.__main__; 'spec2viz' is a package and cannot be directly executed"
- **Severity**: low
- **Type**: discoverability

### Finding SPEC2VIZ-13: `-h` vs `--help` differ (not identical)
- **ST**: ST-edge-cases
- **Step**: 8
- **Command**: `diff <(spec2viz --help) <(spec2viz -h)`
- **Expected**: Identical output
- **Observed**: Files differ. `-h` gives an error, `--help` shows help.
- **Severity**: low
- **Type**: consistency

### Finding SPEC2VIZ-14: `compile_ir` with invalid arg throws AttributeError instead of CompileError
- **ST**: ST-api
- **Step**: 7
- **Command**: `compile_ir('not_a_diagram')`
- **Expected**: Typed exception (`CompileError`, `TypeError`)
- **Observed**: `AttributeError: 'str' object has no attribute 'type'` — exception hierarchy is flat, no typed errors
- **Severity**: low
- **Type**: error-message

### Finding SPEC2VIZ-15: Reflection is not discoverable from CLI help
- **ST**: ST-reflection
- **Step**: 1
- **Command**: `spec2viz validate --help 2>&1 | grep -i reflection`
- **Expected**: Mention of reflection type in help
- **Observed**: "reflection not mentioned in help". The `validate --help` only says "Validate diagram YAML files." with no mention of supported types.
- **Severity**: low
- **Type**: discoverability

### Finding SPEC2VIZ-16: Legacy `yaml_charts` compatibility shim does not work
- **ST**: (uncovered surface)
- **Command**: `python3 -c "import yaml_charts"`
- **Expected**: Deprecation warning + module loads
- **Observed**: `ModuleNotFoundError: No module named 'yaml_charts'`. The docs (README, atom-spec2viz, COVERAGE) all claim legacy imports work. The `spec2viz/spec2vix/` package exists but never creates a top-level `yaml_charts` module.
- **Severity**: high
- **Type**: silent-failure

### Finding SPEC2VIZ-17: Golden PlantUML files out of sync with current output
- **ST**: ST-plantuml
- **Step**: 5
- **Command**: Diff examples/ golden .puml files vs generated output
- **Expected**: All match (or all differ with clear indication of intentional change)
- **Observed**: Only `activity/example.puml` matches. `component`, `deployment`, `sequence`, `state` all differ. The golden files appear stale.
- **Severity**: medium
- **Type**: consistency

### Finding SPEC2VIZ-18: UTF-8 test fixture in ST-edge-cases missing required `version` field
- **ST**: ST-edge-cases
- **Step**: 6
- **Command**: The ST script's UTF-8 test YAML omits `version:`, causing a Pydantic validation error
- **Expected**: Should include all required fields to successfully test UTF-8 handling
- **Observed**: Script generated fixture fails validation with Pydantic error about missing `version` field (not about UTF-8). After adding `version: "1.0"`, UTF-8 works fine.
- **Severity**: low (ST script bug, not tool bug)
- **Type**: edge-case

## Notes
- All 142 existing pytest tests pass (tests/ directory, 0.82s)
- Test suite health: healthy
- Matrix diagram type is `component_view_matrix` in enum but `matrix` in directory/YAML — two naming conventions
- `reflection` is a valid DiagramType with its own example and enforcement pipeline
- Styled diagrams (component.styled.yml) render correctly with skinparam styles
- Vega output for matrix is valid Vega-Lite JSON
