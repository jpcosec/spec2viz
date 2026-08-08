---
id: task-spec2viz-v2-orchestration-and-templating
status: draft
task_type: design
routine: default-task-routine
pills:
- pill-pattern-preserve-spec2viz-contracts-while-fixing-cli-behavior
atoms:
- atom-self-generating-spec-derived-cli
- atom-spec-to-visualization-pipeline
files:
- spec2viz/registry.py
- spec2viz/orchestrator.py
- spec2viz/templating.py
- tests/test_v2_orchestrator.py
tags:
- system:spec2viz
- topic:orchestration
- topic:plugins
- topic:templating
---

# spec2viz 2.0: Orquestador project.yml, Registro de Plugins y Templating Dinámico

ID: task-spec2viz-v2-orchestration-and-templating
Status: draft

## Rationale

La arquitectura actual requiere scripts locales "pegamento" y archivos estáticos generados en disco para construir vistas HTML. Además, el `template.html` tiene valores de branding harcodeados ("Overclock Architecture"), lo que ensucia la generación de arquitectura cuando se recicla en otros proyectos.

## Goal

Evolucionar `spec2viz` para soportar un manifiesto orquestador `project.yml`, un Registro de Plugins dinámico para modelos Pydantic/compiladores locales, y la inyección parametrizada de branding (`project_name`, `brand_name`) en las plantillas HTML.

## Scope

- Implementar la lectura de `project.yml` como archivo de configuración de proyecto.
- Crear el sistema de registro `spec2viz/registry.py` con decoradores `register_diagram_type`.
- Permitir la carga e inyección de plugins Python locales indicados en `project.yml`.
- Parametrizar la inyección de metadatos de branding en `template.html`.
- Permitir compilación y renderizado en memoria sin obligar a escribir archivos estáticos intermedios.

## Non-goals

- Eliminar la compatibilidad hacia atrás con `vistas.yml` existente.

## Implementation Path

1. Crear `spec2viz/registry.py` definiendo `MODEL_REGISTRY` y `COMPILER_REGISTRY`.
2. Crear `spec2viz/orchestrator.py` para procesar `project.yml` y resolver las dependencias e inyecciones.
3. Actualizar la lógica de renderizado de HTML para reemplazar variables de plantilla como `{{ project_name }}` o `{{ brand_name }}`.
4. Agregar tests de integración.

## Validation

- `pytest tests/test_v2_orchestrator.py`
- `pytest`

## Done When

- Al ejecutar `spec2viz build --config project.yml`, se cargan dinámicamente plugins locales, se validan los modelos Pydantic y se inyecta el branding correcto en el HTML resultante.
- No se requiere crear scripts de pegamento locales para compilar diagramas de arquitectura personalizables.
