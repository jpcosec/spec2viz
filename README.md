# spec2viz

`spec2viz` turns semantic YAML specifications into diagrams and charts.

It is meant for teams that want to author structured specs once and render them into outputs such as PlantUML, Mermaid, and Vega.

Within the `hum-ecosystem`, `spec2viz` is the human-watchable rendering layer over canonical `specYaml` semantics. Renderer hints may exist, but semantic truth belongs upstream in `specyaml/`.

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
spec2viz diagram --help
spec2viz catalog --help
```

Diagram commands:

```bash
spec2viz diagram validate tests/fixtures/sequence.create-quotation.yml
spec2viz diagram render tests/fixtures/sequence.create-quotation.yml --out out
spec2viz diagram render tests/fixtures/state.quotation.yml --backend mermaid --out out
spec2viz diagram render examples/component/example.yml --renderer d2 --out out
spec2viz diagram render examples/reflection/example.enforcement.yml --renderer json --out out
spec2viz diagram schema --type sequence --out sequence.schema.json
```

Legacy aliases still work:

```bash
spec2viz validate tests/fixtures/sequence.create-quotation.yml
spec2viz render tests/fixtures/sequence.create-quotation.yml --out out
spec2viz schema --type sequence --out sequence.schema.json
```

Supported renderers:

- `plantuml`
- `mermaid`
- `vega`
- `d2`
- `antonia-html`
- `json`

Catalog commands build a deskops architecture HTML bundle from a legacy `vistas.yml` registry or a hierarchical diagram store:

```bash
spec2viz catalog build --config examples/fixtures/vistas.yml --out out/architecture.html
spec2viz catalog build --config examples/fixtures/vistas.yml --out out/architecture.html --base-dir examples/fixtures --atoms-dir desk/atoms
spec2viz catalog build --config catalog.yml --out out/catalog.html
spec2viz catalog build --config examples/catalog/project.yml --out out/catalog.html
spec2viz catalog schema --out diagram-store.schema.json
```

Hierarchical stores can aggregate other stores and legacy `vistas.yml` leaves, then expose one filtered HTML catalog by category, type, project, and tags.

Minimal `project.yml` / diagram-store shape:

```yaml
diagram_store:
  kind: diagram-store
  template: template.html
  title: Repo Diagram Catalog
  brand_name: Repo Diagram Catalog
  project_name: projects/example
  stores:
    - path: projects/example/docs/vistas.yml
      project: projects/example
      tags:
        - domain:crm
```

## PlantUML Kind Styling

Component specs can now carry renderer-specific color overrides in YAML. This keeps purpose in the semantic `kind` field while letting PlantUML choose how each kind should look.

```yaml
id: architecture.example
title: Example Architecture
type: component
version: "0.1"
style:
  kinds:
    core:
      plantuml:
        background: "#D8ECFF"
        border: "#4C78A8"
        font: "#16324F"
    boundary:
      plantuml:
        background: "#FCECC9"
        border: "#D4A73C"
        font: "#5E450B"
data:
  nodes:
    App:
      kind: core
    Api:
      kind: boundary
```

Notes:

- this currently applies to PlantUML rendering for `component` diagrams
- `kind` stays semantic; the `style.kinds` block is only a renderer hint
- if you omit `style.kinds`, PlantUML falls back to the built-in palette for `core`, `boundary`, and `database`

Export the JSON Schema for all supported specs or one diagram/store type:

```bash
spec2viz schema > spec2viz.schema.json
spec2viz schema --type sequence --out sequence.schema.json
spec2viz schema --type diagram-store --out diagram-store.schema.json
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
- `examples/schema/spec2viz.schema.json`
- `examples/schema/sequence.schema.json`

Refresh the checked-in schema examples when the models change:

```bash
spec2viz schema --out examples/schema/spec2viz.schema.json
spec2viz schema --type sequence --out examples/schema/sequence.schema.json
```

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
