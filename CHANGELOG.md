# Changelog

## 0.2.0 - 2026-05-01

Defined the semantic IR reflection contract and enforcement artifact shape.

- added `ReflectionDiagram`, `ReflectionIR`, and `EnforcementArtifact` models in `spec2viz/models/reflection.py`
- implemented `SemanticMetadata` with 6-dimensional (6D) model support (Who, What, Where, When, How, Why)
- updated `DiagramType` enum to include the new `reflection` diagram type
- exposed `ReflectionDiagram` through the top-level `spec2viz.models` package

## 0.1.0 - 2026-04-22

Initial packaged `spec2viz` release and rename from `yaml-charts`.

- renamed the project, import path, and primary CLI from `yaml-charts` / `yaml_charts` to `spec2viz`
- added packaging metadata, a real `README.md`, checked-in examples, and install verification
- added compatibility shims for legacy `yaml_charts` imports and the `yaml-charts` command with deprecation warnings
- added JSON Schema export through the Python API and `spec2viz schema`
- added descriptions for every Pydantic field so generated schemas and docs carry semantic guidance
- added packaging and example regression tests to keep docs, examples, and shipped behavior aligned

### Migration Notes

- use `spec2viz` instead of `yaml-charts`
- use `import spec2viz` instead of `import yaml_charts`
- regenerate any editor integrations or schema references with `spec2viz schema`
- treat the legacy name as deprecated compatibility only
