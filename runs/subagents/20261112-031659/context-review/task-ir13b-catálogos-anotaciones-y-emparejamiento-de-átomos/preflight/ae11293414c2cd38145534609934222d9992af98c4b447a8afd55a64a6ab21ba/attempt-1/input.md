FILE:desk/tasks/task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos.md
---
sldb:
  by: agent
  at: '2026-11-12T01:25:44Z'
  authority: generated
  via: save_document_payload
id: task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos
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
- task-ir12-renderers-linter-y-recursos-estáticos-de-spec2viz
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files:
- src/specir/visual/catalog.py
- src/specir/visual/catalog_serve.py
- src/specir/visual/atoms.py
- tests/visual/test_catalog.py
- tests/visual/test_catalog_serve.py
- tests/visual/test_atoms_matching.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones
- atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb
from_drawer: desk/drawer/tasks/task-ir13-sync-generacion-catalogos-consumidores-y-retiro-de-spec2viz.md
---

# IR13b Catálogos, anotaciones y emparejamiento de átomos

## Rationale

_Explain why this task exists or the business driver behind it._

Parte de la migración final de spec2viz, separada de IR13 para que cada tarea tenga un solo entregable. El catálogo es la forma en que los repos publican y navegan sus diagramas junto con los átomos que los explican.

## Goal

_Describe the concrete result this task must produce._

specIR construye, sincroniza, valida y sirve catálogos de diagramas, con anotaciones y con los átomos emparejados a cada elemento, cubriendo lo que hace spec2viz.

## Scope

_State what is in scope and what is out of scope._

Dentro: registro de vistas (vistas.yml) y stores jerárquicos de diagramas; construcción del catálogo HTML autocontenido; sincronización del catálogo al store; validación del registro; servidor local con autoguardado de anotaciones; emparejamiento de átomos con elementos de diagrama (explícito y difuso) y cobertura por vista. Cada pieza se migra tal cual o se reemplaza, según la matriz de cobertura.
Fuera: sincronización de un spec individual; notaciones y paletas; CLI; migración de consumidores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Módulos src/specir/visual/catalog.py, catalog_serve.py y atoms.py sobre la sincronización de la tarea IR13a y los renderizadores de la tarea de renderers. Paridad medida portando a tests/visual/ las pruebas de spec2viz de catálogo, rutas de catálogo, vistas resueltas y emparejamiento de átomos.

## Validation

_List the checks required before this task can close._

- La validación de un registro de vistas reporta en specIR los mismos errores tipados que spec2viz sobre los fixtures de catálogo.
- La sincronización del catálogo deja en un store de prueba el mismo contenido que spec2viz, y no escribe nada si alguna vista falla.
- El catálogo construido contiene las mismas vistas, categorías y navegación que el de spec2viz sobre el fixture, y abre sin recursos externos faltantes.
- Una anotación hecha en el servidor local queda guardada y reaparece al recargar.
- El emparejamiento de átomos reporta los mismos átomos por elemento y la misma cobertura por vista que spec2viz sobre los fixtures de átomos; un id de átomo desconocido es advertencia, o error en modo estricto.
- El paquete no importa spec2viz.

## Done When

_Name the observable condition that makes the task complete._

Las pruebas anteriores pasan y las filas de catálogo y de emparejamiento de átomos de la matriz de cobertura tienen su condición de retiro cumplida.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-ir13b-catálogos-anotaciones-y-emparejamiento-de-átomos: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

