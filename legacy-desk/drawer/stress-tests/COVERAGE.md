# COVERAGE.md: spec2viz stress-test coverage plan

## CLI surfaces

| Comando | ST | Estado |
|---------|----|--------|
| `spec2viz validate` | ST-validate | executed |
| `spec2viz render` | ST-render | executed |
| `spec2viz schema` | ST-schema | executed |
| Validate all diagram types | ST-validate (cubre 1-7) | implicit |
| Render all type+renderer combos | ST-render-combos | executed |
| Render multiple files | ST-render-multi | executed |
| PlantUML output | ST-plantuml | executed |
| Mermaid output | ST-mermaid | executed |
| Reflection/enforcement | ST-reflection | executed |
| Python API | ST-api | executed |
| Edge cases OS/IO | ST-edge-cases | executed |
| Test suite health | ST-test-suite-health | seed |
| Legacy yaml_charts compatibility | ST-yaml-charts | seed |
| Vega output correctness | ST-vega | seed |
| Styled diagrams (theme, kinds) | ST-styled-diagrams | seed |
| spec.md vs implementación | ST-spec-consistency | seed |

## Use-cases cubiertos

| UC | Narrativa | STs que lo cubren |
|----|-----------|-------------------|
| UC-01 | Validate spec | ST-validate |
| UC-02 | Render diagram | ST-render, ST-render-combos, ST-plantuml, ST-mermaid, ST-styled-diagrams |
| UC-03 | Schema export | ST-schema |
| UC-04 | Full pipeline | ST-render-multi, ST-validate, ST-render |
| UC-05 | Reflection/enforcement | ST-reflection |
| UC-06 | Python API | ST-api, ST-yaml-charts |

## Superficies cubiertas (nuevas)

| Superficie | ST | Estado |
|------------|----|--------|
| Test suite health | ST-test-suite-health | seed |
| Legacy yaml_charts compatibility | ST-yaml-charts | seed |
| Vega output correctness | ST-vega | seed |
| Styled diagrams (theme, kinds) | ST-styled-diagrams | seed |
| spec.md vs implementación | ST-spec-consistency | seed |

<!--
Template:
| `spec2viz <subcomando>` | ST-XXX | seed/executed/complete |
-->
