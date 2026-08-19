# spec2viz CLI taxonomy

## Purpose

Order the CLI by artifact class instead of by implementation history.

## Top-level taxonomy

### `diagram`
Semantic diagram specs as source truth.

Owns:
- render one or more specs
- validate spec files
- export schema for diagram models

Commands:
- `spec2viz diagram render`
- `spec2viz diagram validate`
- `spec2viz diagram schema`

### `catalog`
HTML viewing bundles and registry/store orchestration.

Owns:
- build HTML from `vistas.yml`
- build HTML from hierarchical `diagram_store`
- export schema for store configs

Commands:
- `spec2viz catalog build`
- `spec2viz catalog schema`

## Compatibility layer

Legacy top-level commands remain as aliases:

- `spec2viz render` → `spec2viz diagram render`
- `spec2viz validate` → `spec2viz diagram validate`
- `spec2viz schema` → legacy mixed entrypoint for diagram schemas and `diagram-store`
- `spec2viz build` → `spec2viz catalog build`

## Source taxonomy

### Diagram source
- semantic YAML specs like `examples/component/example.yml`

### Catalog source
- legacy leaf registry: `vistas.yml`
- hierarchical store root: `project.yml` or `catalog.yml` with `diagram_store`

## Output taxonomy

### Diagram outputs
- `.puml`
- `.mmd`
- `.d2`
- `.vega.json`
- renderer-specific `.html`

### Catalog outputs
- aggregated HTML catalog with:
  - category navigation
  - project filter
  - type filter
  - tag filter
  - text search

## Decision rules

- Use `diagram` when the input is a semantic diagram spec.
- Use `catalog` when the input is a registry/store that points to rendered views.
- Keep `vistas.yml` as a leaf compatibility format.
- Prefer `diagram_store` for repo-level indexing and cross-project catalogs.
