---
sldb:
  by: agent
  at: '2026-11-15T16:54:51Z'
  authority: generated
  via: save_document_payload
id: task-ir13d-cli-api-python-y-habilidad-de-agente-de-la-capa-visual
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
current_node: ritual-execution
history: []
references: []
depends_on:
- task-ir13a-sincronización-de-specs-al-store-y-generación-de-specs
- task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos
- task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/cli.py
- src/specir/visual/__init__.py
- skills/use-specir/SKILL.md
- docs/spec2viz/correspondencia-cli.md
- tests/visual/test_cli.py
- tests/visual/test_api.py
- tests/visual/test_packaging.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-specir-depende-solo-de-la-api-pública-de-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13d CLI, API Python y habilidad de agente de la capa visual

## Rationale

_Explain why this task exists or the business driver behind it._

Parte de la migración final de spec2viz, separada de IR13 para que cada tarea tenga un solo entregable. Los consumidores de spec2viz lo usan por su comando, por su API Python y por una habilidad de agente; sin equivalentes en specIR no tienen a dónde migrar.

## Goal

_Describe the concrete result this task must produce._

specIR ofrece un comando, una API Python pública y una habilidad de agente que cubren cada entrada pública de spec2viz.

## Scope

_State what is in scope and what is out of scope._

Dentro: comando de specIR con equivalentes de todos los comandos y subgrupos de spec2viz (diagram, notation, palette, catalog, y los alias de primer nivel render, validate, lint, schema y build, y about); API Python pública equivalente a la que exporta el paquete spec2viz; habilidad de agente que reemplaza a la de uso de spec2viz; tabla de correspondencia comando por comando.
Fuera: implementar las capacidades, que vienen de las tareas de compiladores, renderers, IR13a, IR13b e IR13c; instalar la habilidad en otros repos; migrar consumidores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulo src/specir/cli.py y exportaciones públicas en src/specir/visual/__init__.py que conectan las capacidades ya implementadas; habilidad en skills/use-specir/SKILL.md; correspondencia en docs/spec2viz/correspondencia-cli.md. Paridad medida portando a tests/visual/ las pruebas de spec2viz de CLI, API y empaquetado. Propiedad de archivos compartidos: src/specir/visual/__init__.py ya existe cuando esta tarea empieza: lo crea la tarea de compiladores y proyecciones (IR11), de la que esta depende por la cadena IR13a e IR12. Aquí solo se extiende con las exportaciones públicas que faltan; no se recrea ni se quitan las exportaciones existentes.

## Validation

_List the checks required before this task can close._

- Cada comando y subgrupo que lista la ayuda de spec2viz tiene una fila en la tabla de correspondencia con su equivalente en specIR, y una prueba invoca cada equivalente.
- Las pruebas de API de spec2viz portadas pasan contra la API pública de specIR.
- La habilidad de agente nombra solo comandos que existen en el comando de specIR (comprobado por una prueba que los extrae y los invoca con ayuda).
- El paquete se instala en un entorno limpio y el comando arranca sin spec2viz instalado.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y las filas de CLI, API Python y habilidad de la matriz de cobertura tienen su condición de retiro cumplida.
