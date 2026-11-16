---
sldb:
  by: agent
  at: '2026-11-16T00:53:31Z'
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
files:
- src/specir/visual/catalog/__init__.py
- src/specir/visual/catalog/loader.py
- src/specir/visual/catalog/sections.py
- src/specir/visual/catalog/views.py
- src/specir/visual/catalog/fragments.py
- src/specir/visual/catalog/atoms.py
- src/specir/visual/catalog/annotations.py
- src/specir/visual/catalog/build.py
- src/specir/visual/templates/annotations-sldb.js
- src/specir/visual/notation_style.py
- src/specir/visual/__init__.py
- tests/visual/test_catalog.py
- tests/visual/test_catalog_parity.py
- tests/visual/test_catalog_annotations.py
- tests/test_imports.py
- tests/visual/test_visual_names.py
- tests/visual/test_resources.py
- docs/spec2viz/matriz-de-cobertura.md
- pyproject.toml
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

Precisiones (preflight):

1. «Alcanza»: D4 comprobó que `sldb serve` lee un documento por id (`GET /document?id=`) y lo escribe con guarda optimista (`POST /save` con `changes[].expected` igual al payload leído; 409 si cambió). Eso alcanza para el autoguardado: specIR no levanta servidor propio. El catálogo HTML se abre como archivo y su JS habla con `sldb serve --cors`.
2. Pedido a sldb: no hace falta para el servidor. Cualquier carencia que aparezca (por ejemplo nombres que `sldb.api` no exporta) se envía con `deskops message send --to sldb` y se cita en el informe de la tarea.
3. Límite visual. Quedan en specIR: el cargador del registro de vistas y de los stores jerárquicos (vistas, categorías, anchors, tags, `project.yml`), el HTML del catálogo (secciones, navegación, filtros, tableros desde la vista resuelta con el `view_mermaid` de IR12), el adaptador de una vista del catálogo a `SpecView` con el descubrimiento del store de la vista, la inyección de átomos en el HTML (`split_shared_atoms`), el modelo del store que guarda las anotaciones de un catálogo y el JS que las guarda en `sldb serve`. Se usan de sldb, sin envoltorio: la regla de rutas (`sldb.api.notations.catalog_paths`), `check_catalog`, `sync_catalog` y `sldb notations sync --catalog [--check]`, `resolve_view`, `SpecSync` y todo `sldb.api.matching`.
4. «Mismos errores tipados»: por cada entrada que devuelve `check_catalog`, la vista, el spec, el nombre de la clase de la excepción y su mensaje, comparados con `check_catalog` de spec2viz sobre los registros de las pruebas de rutas y notaciones de catálogo de spec2viz y sobre su propio registro de arquitectura (el vistas.yml de su carpeta de documentación).
5. «Mismo contenido» y «mismas vistas»: en el store, los documentos (modelo, nombre y payload) normalizados como en IR13a. En el catálogo, extraídos del HTML: secciones (anchor, id de vista, título, categoría, tipo, proyecto y tags, en orden), bloques de categoría, enlaces de navegación (href y texto, en orden), filtros y tableros. En los átomos, `ATOMS_DB`, `ATOMS_BY_VIEW`, `ATOMS_EXPLICIT`, `ATOMS_LINKED`, `REFS_EXPLICIT` y `COVERAGE_BY_VIEW` iguales como JSON.
6. Modo estricto: el parámetro `strict_atoms` de la construcción del catálogo (el `--strict-atoms` de spec2viz), que lanza `UnknownAtomError` de sldb. Sin él, el aviso queda en el HTML y en stderr.
7. Matriz: `docs/spec2viz/matriz-de-cobertura.md`, filas SV-G01 a SV-G08 y SV-I01 a SV-I05. IR13b cita en ellas sus pruebas sin marcarlas cumplidas; eso lo hace IR13. La CLI (`catalog build`, el alias `build` y lo que reemplaza a `catalog serve`) es de IR13d: los casos de build del módulo de pruebas test_cli de spec2viz se portan sobre la API de specIR.

Precisiones (bundle):

1. Cierre frente a la matriz: IR13b cierra con sus pruebas en verde y citadas en las filas SV-G01 a SV-G08 y SV-I01 a SV-I05, cuya condición de retiro esas pruebas acreditan. La marca de fila cumplida la pone solo IR13, como dice la matriz. El «Done When» se lee así.
2. «El paquete» es `src/specir` (lo comprueba `tests/test_imports.py`). Bajo tests/ importan spec2viz solo los oráculos de paridad que lista `tests/visual/test_visual_names.py` (ORACLES), al que se suma `tests/visual/test_catalog_parity.py`.
3. El cierre se verifica con spec2viz instalado (IR/.venv lo trae editable): las pruebas `parity` corren y pasan. Sin spec2viz se omiten y quedan las portadas (`tests/visual/test_catalog.py` y `tests/visual/test_catalog_annotations.py`), que no lo usan. El catálogo no tiene goldens: tras el retiro, la paridad queda acreditada por la corrida que cita el informe de la tarea.

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
