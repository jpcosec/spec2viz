# spec2viz

`spec2viz` turns semantic YAML specifications into diagrams and charts.

It is meant for teams that want to author structured specs once and render them into outputs such as PlantUML, Mermaid, and Vega.

## What It Does

- validates diagram specs with Pydantic models
- compiles semantic specs into renderer-agnostic IR
- renders sequence, state, component, activity, deployment, and matrix views
- supports both a Python API and a CLI

## Install

```bash
python3 -m pip install .
```

For local development:

```bash
python3 -m pip install -e .[dev]
```

## CLI

Inspect the available commands:

```bash
spec2viz --help
```

Validate a spec:

```bash
spec2viz validate tests/fixtures/sequence.create-quotation.yml
```

Render one or more specs:

```bash
spec2viz render tests/fixtures/sequence.create-quotation.yml --out out
spec2viz render tests/fixtures/state.quotation.yml --backend mermaid --out out
```

Export the JSON Schema for all supported specs or one diagram type:

```bash
spec2viz schema > spec2viz.schema.json
spec2viz schema --type sequence --out sequence.schema.json
```

## Python API

```python
from spec2viz import compile_ir, load, render, validate

diagram = load("tests/fixtures/sequence.create-quotation.yml")
validate(diagram)
ir = compile_ir(diagram)
output = render(ir)
```

Write rendered output directly to disk:

```python
from spec2viz import render_to_file

path = render_to_file("tests/fixtures/matrix.quotation-view.yml", out="out")
print(path)
```

Generate JSON Schema for editor integration or documentation:

```python
from spec2viz import json_schema, write_json_schema

schema = json_schema("sequence")
write_json_schema("sequence.schema.json", diagram_type="sequence")
```

## Examples

Sample source specs and rendered outputs live under `examples/`.

- `examples/sequence/example.yml`
- `examples/state/example.yml`
- `examples/component/example.yml`
- `examples/activity/example.yml`
- `examples/deployment/example.yml`
- `examples/matrix/example.yml`

## Validation and Tests

Run the full suite:

```bash
pytest -q
```

Validate packaged installation behavior:

```bash
python3 -m pip install --force-reinstall .
spec2viz --help
```

## Migration From `yaml-charts`

The project was renamed from `yaml-charts` / `yaml_charts` to `spec2viz`.

- preferred import path: `spec2viz`
- preferred CLI command: `spec2viz`
- legacy imports under `yaml_charts` still resolve with a deprecation warning
- legacy CLI `yaml-charts` still works as a compatibility shim and prints a migration notice

New code should use `spec2viz` everywhere.
