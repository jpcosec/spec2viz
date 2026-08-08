---
id: task-spec2viz-migration-and-spec-provenance
status: draft
task_type: design
routine: default-task-routine
pills:
- pill-pattern-preserve-spec2viz-contracts-while-fixing-cli-behavior
atoms:
- atom-spec-driven-artifact-architecture
files:
- spec2viz/importer.py
- spec2viz/provenance.py
- tests/test_importer.py
tags:
- system:spec2viz
- topic:migration
- topic:provenance
---

# Migración de Diagramas Mermaid y Trazabilidad de Especificación

ID: task-spec2viz-migration-and-spec-provenance
Status: draft

## Rationale

Existen diagramas Mermaid legados hechos a mano bajo `docs/diagrams/`. La filosofía de `spec2viz` exige que la fuente sea la especificación estructurada YAML y que el Mermaid sea una proyección generada. Se requiere un mecanismo para migrar diagramas existentes a YAML y asegurar que las proyecciones mantengan metadatos de trazabilidad (*provenance*).

## Goal

Proveer el comando `spec2viz import mermaid <file.mmd>` para andamiar una fuente YAML a partir de Mermaid existente, e integrar cabeceras de trazabilidad en las proyecciones Mermaid generadas.

## Scope

- Implementar `spec2viz import mermaid <path.mmd>` para crear una especificación YAML borrador.
- Inyectar comentarios de metadatos de proveniencia en el encabezado del código Mermaid proyectado (referenciando la fuente YAML y el comando de validación).
- Añadir tests unitarios para la importación y trazabilidad.

## Non-goals

- Convertir automáticamente diagramas extremadamente complejos sin revisión humana.

## Implementation Path

1. Implementar `spec2viz/importer.py` para parsear nodos/bordes de Mermaid básico hacia modelos de `spec2viz`.
2. Modificar los generadores para incluir comentarios `# Generated from: <spec.yml>` en los diagramas producidos.
3. Probar la migración en diagramas de ejemplo.

## Validation

- `pytest tests/test_importer.py`
- `pytest`

## Done When

- `spec2viz import mermaid docs/diagrams/example.mmd` genera una especificación YAML válida.
- Las proyecciones Mermaid generadas contienen comentarios de encabezado con su trazabilidad y comando de validación.
