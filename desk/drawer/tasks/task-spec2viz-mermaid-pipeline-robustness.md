---
id: task-spec2viz-mermaid-pipeline-robustness
status: draft
task_type: implementation
routine: default-task-routine
pills:
- pill-pattern-preserve-spec2viz-contracts-while-fixing-cli-behavior
atoms:
- atom-spec-to-visualization-pipeline
files:
- spec2viz/compilers/mermaid.py
- spec2viz/cli.py
- tests/test_mermaid_compiler.py
tags:
- system:spec2viz
- topic:mermaid
- topic:compiler
---

# Robustez en el Pipeline de Renderizado y Validación de Mermaid

ID: task-spec2viz-mermaid-pipeline-robustness
Status: draft

## Rationale

Actualmente `spec2viz` genera diagramas Mermaid que rompen silenciosamente en el navegador cuando las etiquetas de los bordes contienen caracteres especiales (como paréntesis `()`), debido a que no están envueltas en comillas (`-->|label|`). Además, la CLI genera PlantUML por defecto mientras que el `template.html` base asume Mermaid, causando un desajuste que requiere banderas explícitas para evitar fallos. Por último, no existe una validación linteo fail-fast antes de compilar el HTML.

## Goal

Garantizar que el compilador de Mermaid genere etiquetas bien formadas con comillas automáticas, alinear el backend por defecto de la CLI a Mermaid, y añadir un paso de linteo estático fail-fast para detectar sintaxis Mermaid inválida antes del build final.

## Scope

- Modificar el compilador Mermaid en `spec2viz/` para envolver los labels de los bordes entre comillas automáticas (`-->|"label"|`).
- Cambiar el backend por defecto de `spec2viz render` a `mermaid`.
- Añadir validación/linteo básico de sintaxis Mermaid en `spec2viz render` / `spec2viz build` que falle de forma explícita si el código generado es sintácticamente inválido.
- Agregar tests unitarios para verificar el comportamiento con labels complejos.

## Non-goals

- Reemplazar el motor de Mermaid por uno nuevo.
- Implementar soporte para diagramas D2 en este paso.

## Implementation Path

1. Editar `spec2viz/compilers/mermaid.py` (o módulo equivalente) para envolver `edge.label` en comillas dobles si está presente.
2. Modificar `spec2viz/cli.py` estableciendo `--backend` por defecto en `"mermaid"`.
3. Implementar la función de linteo/validación en el pipeline de renderizado.
4. Ejecutar la suite de tests en `tests/`.

## Validation

- `pytest tests/test_mermaid_compiler.py`
- `pytest`

## Done When

- Los diagramas con etiquetas como `Intención Operativa (F0)` se renderizan como `-->|"Intención Operativa (F0)"|` sin romper el parser de Mermaid.
- `spec2viz render` sin banderas genera Mermaid por defecto.
- El build falla con un mensaje de error claro si se intenta inyectar sintaxis Mermaid corrupta.
