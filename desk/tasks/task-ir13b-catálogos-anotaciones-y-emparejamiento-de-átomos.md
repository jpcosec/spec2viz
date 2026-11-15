---
sldb:
  by: agent
  at: '2026-11-15T16:54:47Z'
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
- task-espejo-sldb-emparejamiento-de-átomos-en-sldb-api-matching-d4
pills:
- desk/contexts/pill-guardrail-specir-solo-usa-la-api-pública-de-sldb.md
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas.md
files: []
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

specIR construye, sincroniza, valida y sirve catálogos de diagramas con anotaciones, y empareja átomos con elementos de diagrama usando sldb.api.matching (D4); el catálogo se sirve con sldb serve si alcanza. specIR conserva solo la parte visual del catálogo.

## Scope

_State what is in scope and what is out of scope._

Dentro: registro de vistas (vistas.yml) y stores jerárquicos de diagramas; construcción del catálogo HTML autocontenido con los renderers de IR12; sincronización y validación del catálogo; emparejamiento de átomos con elementos de diagrama (explícito y difuso) y cobertura por vista llamando a sldb.api.matching (D4); servicio del catálogo y autoguardado de anotaciones con sldb serve; si sldb serve no alcanza para las anotaciones, se pide por el desk de sldb y solo queda en specIR lo que sea visual. Fuera: implementar el emparejamiento en specIR (se migra a sldb, tarea espejo D4); sincronización de un spec individual; notaciones y paletas, que se usan desde sldb; CLI; migración de consumidores.

## Implementation Path

_Outline the expected implementation route or affected surface._

Capa delgada en el paquete specIR (specir.visual) sobre la sincronización de IR13a, los renderers de IR12, sldb.api.matching y sldb serve. Paridad medida con pruebas de specIR que comparan con las de spec2viz de catálogo, rutas de catálogo, vistas resueltas y emparejamiento de átomos como oráculo de desarrollo. Depende de la tarea espejo D4.

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

Las pruebas anteriores pasan, specIR no define su propio emparejamiento de átomos y las filas de catálogo y de emparejamiento de átomos de la matriz de cobertura tienen su condición de retiro cumplida.
